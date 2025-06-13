import re
import random
from datetime import datetime, timedelta
import uuid
from .restaurant_api import RestaurantAPI

class ChatHandler:
    """Handles chat message processing and response generation"""
    
    def __init__(self):
        self.restaurant_api = RestaurantAPI()
        self.context_keywords = {
            'booking': ['book', 'table', 'reservation', 'reserve', 'seat'],
            'menu': ['menu', 'food', 'dish', 'eat', 'order', 'popular', 'recommend'],
            'location': ['near', 'nearby', 'location', 'address', 'where'],
            'cuisine': ['italian', 'chinese', 'mexican', 'indian', 'american', 'japanese', 'thai', 'pizza', 'burger'],
            'time': ['tonight', 'today', 'tomorrow', 'lunch', 'dinner', 'breakfast'],
            'party_size': ['people', 'person', 'party', 'group']
        }
    
    def process_message(self, message, chat_history):
        """Process user message and return appropriate bot response"""
        message_lower = message.lower()
        
        # Extract context from message
        context = self._extract_context(message_lower)
        
        # Determine intent
        if self._has_keywords(message_lower, self.context_keywords['booking']):
            return self._handle_booking_request(message, context)
        elif self._has_keywords(message_lower, self.context_keywords['menu']):
            return self._handle_menu_request(message, context)
        elif any(cuisine in message_lower for cuisine in self.context_keywords['cuisine']):
            return self._handle_cuisine_search(message, context)
        elif 'help' in message_lower or 'what can you do' in message_lower:
            return self._handle_help_request()
        else:
            return self._handle_general_query(message)
    
    def _extract_context(self, message):
        """Extract relevant context from message"""
        context = {}
        
        # Extract party size
        party_match = re.search(r'(\d+)\s*(people|person)', message)
        if party_match:
            context['party_size'] = int(party_match.group(1))
        
        # Extract time references
        if 'tonight' in message:
            context['time'] = 'tonight'
        elif 'today' in message:
            context['time'] = 'today'
        elif 'tomorrow' in message:
            context['time'] = 'tomorrow'
        
        # Extract cuisine preferences
        for cuisine in self.context_keywords['cuisine']:
            if cuisine in message:
                context['cuisine'] = cuisine
                break
        
        return context
    
    def _has_keywords(self, message, keywords):
        """Check if message contains any of the given keywords"""
        return any(keyword in message for keyword in keywords)
    
    def _handle_booking_request(self, message, context):
        """Handle table booking requests"""
        party_size = context.get('party_size', 2)
        time_pref = context.get('time', 'tonight')
        
        # Get available restaurants
        restaurants = self.restaurant_api.get_restaurants_for_booking()
        
        response_text = f"I'd be happy to help you book a table for {party_size} people {time_pref}! "
        response_text += "Here are some great restaurants with availability:"
        
        return {
            'id': str(uuid.uuid4()),
            'type': 'bot',
            'content': response_text,
            'timestamp': datetime.now().isoformat(),
            'message_type': 'card',
            'cards': restaurants[:3],  # Show top 3 restaurants
            'quick_replies': [
                {'text': 'Book a table', 'action': 'booking'},
                {'text': 'See more restaurants', 'action': 'more_restaurants'},
                {'text': 'Different time', 'action': 'change_time'}
            ]
        }
    
    def _handle_menu_request(self, message, context):
        """Handle menu and food-related requests"""
        cuisine = context.get('cuisine')
        
        if cuisine:
            restaurants = self.restaurant_api.get_restaurants_by_cuisine(cuisine)
            response_text = f"Here are some great {cuisine.title()} restaurants with their popular dishes:"
        else:
            restaurants = self.restaurant_api.get_popular_restaurants()
            response_text = "Here are some popular restaurants and their signature dishes:"
        
        return {
            'id': str(uuid.uuid4()),
            'type': 'bot',
            'content': response_text,
            'timestamp': datetime.now().isoformat(),
            'message_type': 'card',
            'cards': restaurants[:3],
            'quick_replies': [
                {'text': 'View full menu', 'action': 'full_menu'},
                {'text': 'Order now', 'action': 'order'},
                {'text': 'See reviews', 'action': 'reviews'}
            ]
        }
    
    def _handle_cuisine_search(self, message, context):
        """Handle cuisine-specific searches"""
        cuisine = context.get('cuisine')
        restaurants = self.restaurant_api.get_restaurants_by_cuisine(cuisine)
        
        response_text = f"I found some excellent {cuisine.title()} restaurants for you:"
        
        return {
            'id': str(uuid.uuid4()),
            'type': 'bot',
            'content': response_text,
            'timestamp': datetime.now().isoformat(),
            'message_type': 'card',
            'cards': restaurants[:4],
            'quick_replies': [
                {'text': 'Book a table', 'action': 'booking'},
                {'text': 'Order delivery', 'action': 'delivery'},
                {'text': 'See more options', 'action': 'more_cuisine'}
            ]
        }
    
    def _handle_help_request(self):
        """Handle help and general capability requests"""
        response_text = """I'm your AI restaurant assistant! Here's what I can help you with:

🍽️ **Table Reservations** - Find and book tables at restaurants
📋 **Menu Browsing** - Explore menus and popular dishes
🚚 **Food Delivery** - Order food for delivery
🔍 **Restaurant Search** - Find restaurants by cuisine or location
⭐ **Reviews & Ratings** - Check restaurant reviews and ratings

Just tell me what you're looking for, like:
• "Book a table for 4 tonight"
• "Show me Italian restaurants nearby"
• "What's popular at Mario's Pizza?"

How can I assist you today?"""
        
        return {
            'id': str(uuid.uuid4()),
            'type': 'bot',
            'content': response_text,
            'timestamp': datetime.now().isoformat(),
            'message_type': 'text',
            'quick_replies': [
                {'text': 'Find restaurants', 'action': 'search'},
                {'text': 'Book a table', 'action': 'booking'},
                {'text': 'Order food', 'action': 'order'}
            ]
        }
    
    def _handle_general_query(self, message):
        """Handle general queries and provide helpful responses"""
        responses = [
            "I'd be happy to help you with that! Could you tell me more about what you're looking for?",
            "That's interesting! Are you looking to book a table, order food, or browse restaurant menus?",
            "I'm here to help with all your restaurant needs. What specific assistance would you like?",
            "Let me help you find what you're looking for. Are you interested in dining in or ordering delivery?"
        ]
        
        response_text = random.choice(responses)
        
        return {
            'id': str(uuid.uuid4()),
            'type': 'bot',
            'content': response_text,
            'timestamp': datetime.now().isoformat(),
            'message_type': 'text',
            'quick_replies': [
                {'text': 'Book a table', 'action': 'booking'},
                {'text': 'Browse menus', 'action': 'menu'},
                {'text': 'Find restaurants', 'action': 'search'},
                {'text': 'Get help', 'action': 'help'}
            ]
        }
