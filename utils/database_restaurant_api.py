import random
from datetime import datetime, timedelta, date
from config_supabase import supabase

class DatabaseRestaurantAPI:
    """Restaurant API that uses Supabase instead of SQLAlchemy models"""
    
    def __init__(self):
        pass
    
    def get_restaurants_for_booking(self):
        """Get restaurants suitable for table booking with availability"""
        try:
            result = supabase.table('restaurants').select('*').eq('is_active', True).limit(6).execute()
            restaurants = [r for r in result.data if 'dine_in' in r.get('services_offered', [])]
            
            return self._format_restaurant_cards(restaurants)
        except Exception as e:
            return {
                'type': 'error',
                'content': f"Error fetching restaurants: {str(e)}"
            }
    
    def get_restaurants_by_cuisine(self, cuisine):
        """Get restaurants filtered by cuisine type"""
        try:
            result = supabase.table('restaurants').select('*').eq('cuisine', cuisine.lower()).eq('is_active', True).limit(8).execute()
            
            return self._format_restaurant_cards(result.data)
        except Exception as e:
            return {
                'type': 'error',
                'content': f"Error fetching {cuisine} restaurants: {str(e)}"
            }
    
    def get_popular_restaurants(self):
        """Get popular restaurants for general recommendations"""
        try:
            result = supabase.table('restaurants').select('*').eq('is_active', True).order('rating', desc=True).limit(6).execute()
            
            return self._format_restaurant_cards(result.data)
        except Exception as e:
            return {
                'type': 'error', 
                'content': f"Error fetching popular restaurants: {str(e)}"
            }
    
    def search_restaurants(self, query=None, cuisine=None, max_price=None, min_rating=None):
        """Advanced restaurant search with filters"""
        try:
            # Start with base query
            query_builder = supabase.table('restaurants').select('*').eq('is_active', True)
            
            # Apply filters
            if cuisine:
                query_builder = query_builder.eq('cuisine', cuisine.lower())
            
            if max_price:
                price_mapping = {'$': 1, '$$': 2, '$$$': 3, '$$$$': 4}
                max_price_num = price_mapping.get(max_price, 4)
                # This is a simplified filter - in real implementation, you'd handle price comparison properly
                query_builder = query_builder.lte('price_level', max_price)
            
            if min_rating:
                query_builder = query_builder.gte('rating', min_rating)
            
            # Execute query
            result = query_builder.limit(10).execute()
            
            # Text search if query provided (simplified - in production use full-text search)
            if query:
                filtered_data = []
                query_lower = query.lower()
                for restaurant in result.data:
                    if (query_lower in restaurant.get('name', '').lower() or 
                        query_lower in restaurant.get('description', '').lower() or
                        query_lower in restaurant.get('cuisine', '').lower()):
                        filtered_data.append(restaurant)
                result.data = filtered_data
            
            return self._format_restaurant_cards(result.data)
        except Exception as e:
            return {
                'type': 'error',
                'content': f"Error searching restaurants: {str(e)}"
            }
    
    def get_restaurant_menu(self, restaurant_id):
        """Get full menu for a specific restaurant"""
        try:
            # Get restaurant details
            restaurant_result = supabase.table('restaurants').select('*').eq('id', restaurant_id).execute()
            if not restaurant_result.data:
                return {'type': 'error', 'content': 'Restaurant not found'}
            
            restaurant = restaurant_result.data[0]
            
            # Get dishes for this restaurant
            dishes_result = supabase.table('dishes').select('*').eq('restaurant_id', restaurant_id).eq('is_available', True).execute()
            
            # Group dishes by category
            menu_categories = {}
            for dish in dishes_result.data:
                category = dish.get('category', 'other')
                if category not in menu_categories:
                    menu_categories[category] = []
                
                dish_item = {
                    'id': dish['id'],
                    'name': dish['name'],
                    'price': f"${dish['price']:.2f}",
                    'description': dish.get('description', ''),
                    'dietary_tags': dish.get('dietary_tags', []),
                    'image': dish.get('image_url', ''),
                    'popular': dish.get('is_popular', False)
                }
                menu_categories[category].append(dish_item)
            
            return {
                'type': 'menu',
                'restaurant_name': restaurant['name'],
                'restaurant_id': restaurant_id,
                'categories': menu_categories,
                'content': f"Here's the menu for {restaurant['name']}:"
            }
        except Exception as e:
            return {
                'type': 'error',
                'content': f"Error fetching menu: {str(e)}"
            }
    
    def get_restaurant_details(self, restaurant_id):
        """Get detailed information about a restaurant"""
        try:
            result = supabase.table('restaurants').select('*').eq('id', restaurant_id).execute()
            if not result.data:
                return {'type': 'error', 'content': 'Restaurant not found'}
            
            restaurant = result.data[0]
            
            return {
                'type': 'restaurant_details',
                'restaurant': restaurant,
                'content': f"Here are the details for {restaurant['name']}:"
            }
        except Exception as e:
            return {
                'type': 'error',
                'content': f"Error fetching restaurant details: {str(e)}"
            }
    
    def get_available_cuisines(self):
        """Get list of available cuisines"""
        try:
            result = supabase.table('restaurants').select('cuisine').eq('is_active', True).execute()
            cuisines = list(set(r['cuisine'] for r in result.data if r.get('cuisine')))
            return sorted(cuisines)
        except Exception as e:
            return []
    
    def get_restaurants_near_location(self, location=None, radius_miles=5):
        """Get restaurants near a specific location (simplified)"""
        try:
            # Simplified implementation - in production, use PostGIS for geo queries
            result = supabase.table('restaurants').select('*').eq('is_active', True).limit(8).execute()
            
            return self._format_restaurant_cards(result.data)
        except Exception as e:
            return {
                'type': 'error',
                'content': f"Error fetching nearby restaurants: {str(e)}"
            }
    
    def _format_restaurant_cards(self, restaurants):
        """Helper method to format restaurant data as cards"""
        restaurant_cards = []
        
        for restaurant in restaurants:
            try:
                # Get availability slots for today from database
                availability_result = supabase.table('availability_slots').select('*').eq('restaurant_id', restaurant['id']).eq('date', str(date.today())).eq('is_available', True).limit(6).execute()
                
                availability = [
                    {'time': slot['time_slot'], 'available': slot['is_available']}
                    for slot in availability_result.data
                ]
                
                # If no availability data, generate some default slots
                if not availability:
                    default_times = ['6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM']
                    availability = [
                        {'time': time, 'available': random.random() > 0.3}
                        for time in default_times
                    ]
                
                restaurant_card = {
                    'type': 'restaurant',
                    'id': f'rest_{restaurant["id"]}',
                    'name': restaurant['name'],
                    'image': restaurant.get('image_url', ''),
                    'rating': restaurant.get('rating', 4.0),
                    'price_level': restaurant.get('price_level', '$$'),
                    'distance': restaurant.get('distance', '1.0 miles'),
                    'description': restaurant.get('description', ''),
                    'cuisine': restaurant.get('cuisine', ''),
                    'availability': availability,
                    'actions': [
                        {'text': 'Book Table', 'action': f"book_{restaurant['id']}"},
                        {'text': 'View Menu', 'action': f"menu_{restaurant['id']}"},
                        {'text': 'Get Directions', 'action': f"directions_{restaurant['id']}"}
                    ]
                }
                restaurant_cards.append(restaurant_card)
            except Exception as e:
                continue  # Skip this restaurant if there's an error formatting it
        
        return restaurant_cards