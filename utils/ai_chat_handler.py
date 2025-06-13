import os
import re
import json
import uuid
from datetime import datetime
from groq import Groq
from .database_restaurant_api import DatabaseRestaurantAPI

class AIChatHandler:
    """AI-powered chat handler using Groq API for restaurant assistant"""
    
    def __init__(self):
        self.client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
        self.restaurant_api = DatabaseRestaurantAPI()
        self.system_prompt = """You are DineDesk, a smart restaurant assistant. Track conversation context and NEVER repeat questions.

CRITICAL RULES:
- NEVER ask the same question twice
- NEVER ask for confirmation
- Extract ALL details from each user message
- Move to next needed info immediately
- If location not in database, suggest alternatives or end conversation

CONVERSATION TRACKING:
- Remember: location, cuisine, time, party size, service type
- Skip questions if info already provided
- Don't confirm details unless booking

LOCATION HANDLING:
- If city not recognized/not in database: "Sorry, we don't serve [city]. Try [nearby city] or [other city]?"
- If user says unclear location: Ask once for clarification
- If still unclear: End conversation politely

FLOW:
Need: Location → Cuisine → Show restaurants
- Only ask what's missing
- Don't repeat or confirm
- Maximum 15 words per response

EXAMPLES:
User: "Pizza in Ahmedabad" → Show pizza restaurants (have location + cuisine)
User: "Ahmedabad" → "What cuisine?" (have location, need cuisine)
User: "Italian" → "What city?" (have cuisine, need location)
"""
    
    def process_message(self, message, chat_history):
        """Process user message with AI and return appropriate response"""
        try:
            # Analyze if this is a restaurant search/booking request
            intent = self._analyze_intent(message)
            
            if intent in ['booking', 'search', 'menu']:
                return self._handle_restaurant_query(message, intent, chat_history)
            else:
                return self._handle_general_query(message, chat_history)
                
        except Exception as e:
            print(f"Error in AI chat handler: {e}")
            return self._get_fallback_response()
    
    def _analyze_intent(self, message):
        """Analyze user intent from message"""
        message_lower = message.lower()
        
        booking_keywords = ['book', 'table', 'reservation', 'reserve', 'seat']
        search_keywords = ['restaurant', 'find', 'search', 'near', 'cuisine']
        menu_keywords = ['menu', 'food', 'dish', 'order', 'popular', 'recommend']
        
        if any(keyword in message_lower for keyword in booking_keywords):
            return 'booking'
        elif any(keyword in message_lower for keyword in search_keywords):
            return 'search'
        elif any(keyword in message_lower for keyword in menu_keywords):
            return 'menu'
        else:
            return 'general'
    
    def _handle_restaurant_query(self, message, intent, chat_history):
        """Handle restaurant-specific queries with AI and real data"""
        try:
            # Get recent conversation context
            context = self._build_conversation_context(chat_history[-5:] if len(chat_history) > 5 else chat_history)
            
            # Create AI prompt for restaurant query
            prompt = f"""User message: "{message}"
Intent: {intent}
Previous context: {context}

Extract ALL details. Only ask for missing info. Never repeat questions. Check if location is valid."""
            
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_completion_tokens=50,  # Much shorter for concise responses
                top_p=0.9,
                stream=False
            )
            
            ai_response = getattr(completion.choices[0].message, 'content', '') or "I'm here to help with your restaurant needs!"
            ai_response = ai_response.strip()
            
            # Get relevant restaurant data based on intent
            restaurants = self._get_relevant_restaurants(message, intent)
            
            if restaurants is None:  # Invalid location detected
                return {
                    'id': str(uuid.uuid4()),
                    'type': 'bot',
                    'content': "Sorry, we don't serve that area. Try New York instead?",
                    'timestamp': datetime.now().isoformat(),
                    'message_type': 'text',
                    'quick_replies': [
                        {'text': 'New York restaurants', 'action': 'new_york'},
                        {'text': 'Browse all', 'action': 'browse'}
                    ]
                }
            elif restaurants:
                return {
                    'id': str(uuid.uuid4()),
                    'type': 'bot',
                    'content': ai_response,
                    'timestamp': datetime.now().isoformat(),
                    'message_type': 'card',
                    'cards': restaurants[:3],  # Show top 3 restaurants
                    'quick_replies': self._generate_quick_replies(intent)
                }
            else:
                return {
                    'id': str(uuid.uuid4()),
                    'type': 'bot',
                    'content': ai_response,
                    'timestamp': datetime.now().isoformat(),
                    'message_type': 'text',
                    'quick_replies': self._generate_quick_replies('general')
                }
                
        except Exception as e:
            print(f"Error handling restaurant query: {e}")
            return self._get_fallback_response()
    
    def _handle_general_query(self, message, chat_history):
        """Handle general queries with AI"""
        try:
            # Build conversation context
            context = self._build_conversation_context(chat_history[-5:] if len(chat_history) > 5 else chat_history)
            
            prompt = f"""User message: "{message}"
Previous context: {context}

Extract ALL details. Only ask for missing info. Never repeat questions. Under 15 words."""
            
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_completion_tokens=50,
                top_p=0.9,
                stream=False
            )
            
            ai_response = getattr(completion.choices[0].message, 'content', '') or "I'm here to help with your restaurant needs!"
            ai_response = ai_response.strip()
            
            return {
                'id': str(uuid.uuid4()),
                'type': 'bot',
                'content': ai_response,
                'timestamp': datetime.now().isoformat(),
                'message_type': 'text',
                'quick_replies': self._generate_quick_replies('general')
            }
            
        except Exception as e:
            print(f"Error handling general query: {e}")
            return self._get_fallback_response()
    
    def _build_conversation_context(self, recent_messages):
        """Build conversation context and extract collected information"""
        context_parts = []
        collected_info = {
            'location': None,
            'cuisine': None,
            'service_type': None,
            'time': None,
            'party_size': None
        }
        
        # Extract information from conversation history
        for msg in recent_messages:
            content = msg['content'].lower()
            
            # Location detection
            if any(loc in content for loc in ['new york', 'ny', 'manhattan', 'brooklyn']):
                collected_info['location'] = 'new_york'
            elif any(loc in content for loc in ['ahmedabad', 'mumbai', 'delhi', 'bangalore']):
                collected_info['location'] = 'invalid'
            
            # Cuisine detection
            cuisines = ['italian', 'chinese', 'mexican', 'indian', 'japanese', 'american', 'pizza', 'pasta']
            for cuisine in cuisines:
                if cuisine in content:
                    collected_info['cuisine'] = cuisine
                    break
            
            # Service type detection
            if any(word in content for word in ['delivery', 'order']):
                collected_info['service_type'] = 'delivery'
            elif any(word in content for word in ['reservation', 'book', 'table']):
                collected_info['service_type'] = 'reservation'
            
            if msg['type'] == 'user':
                context_parts.append(f"User: {msg['content']}")
            elif msg['type'] == 'bot':
                context_parts.append(f"Assistant: {msg['content'][:50]}...")
        
        context_str = " | ".join(context_parts[-2:])  # Last 2 exchanges
        
        # Add collected info summary
        info_summary = f"Known: location={collected_info['location']}, cuisine={collected_info['cuisine']}, service={collected_info['service_type']}"
        
        return f"{context_str} | {info_summary}"
    
    def _get_relevant_restaurants(self, message, intent):
        """Get relevant restaurant data based on message and intent"""
        message_lower = message.lower()
        
        # Check for invalid locations (not in our database)
        invalid_locations = ['ahmedabad', 'mumbai', 'delhi', 'bangalore', 'chennai', 'kolkata', 'hyderabad', 'pune', 'india']
        for invalid_loc in invalid_locations:
            if invalid_loc in message_lower:
                return None  # Signal invalid location
        
        # Extract cuisine type if mentioned
        cuisines = ['italian', 'chinese', 'mexican', 'indian', 'japanese', 'american']
        found_cuisine = None
        for cuisine in cuisines:
            if cuisine in message_lower:
                found_cuisine = cuisine
                break
        
        if intent == 'booking':
            return self.restaurant_api.get_restaurants_for_booking()
        elif found_cuisine:
            return self.restaurant_api.get_restaurants_by_cuisine(found_cuisine)
        else:
            return self.restaurant_api.get_popular_restaurants()
    
    def _generate_quick_replies(self, intent):
        """Generate contextual quick reply options"""
        if intent == 'booking':
            return [
                {'text': 'Book a table', 'action': 'booking'},
                {'text': 'See more restaurants', 'action': 'more_restaurants'},
                {'text': 'Different time', 'action': 'change_time'}
            ]
        elif intent == 'menu':
            return [
                {'text': 'View full menu', 'action': 'full_menu'},
                {'text': 'Order now', 'action': 'order'},
                {'text': 'See reviews', 'action': 'reviews'}
            ]
        elif intent == 'search':
            return [
                {'text': 'Book a table', 'action': 'booking'},
                {'text': 'Order delivery', 'action': 'delivery'},
                {'text': 'See more options', 'action': 'more_options'}
            ]
        else:
            return [
                {'text': 'Find restaurants', 'action': 'search'},
                {'text': 'Book a table', 'action': 'booking'},
                {'text': 'Order food', 'action': 'order'},
                {'text': 'Get help', 'action': 'help'}
            ]
    
    def _get_fallback_response(self):
        """Fallback response when AI is unavailable"""
        return {
            'id': str(uuid.uuid4()),
            'type': 'bot',
            'content': "I'm here to help you with restaurant bookings and food orders. How can I assist you today?",
            'timestamp': datetime.now().isoformat(),
            'message_type': 'text',
            'quick_replies': [
                {'text': 'Find restaurants', 'action': 'search'},
                {'text': 'Book a table', 'action': 'booking'},
                {'text': 'Order food', 'action': 'order'}
            ]
        }