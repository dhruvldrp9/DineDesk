import random
from datetime import datetime, timedelta

class RestaurantAPI:
    """Handles restaurant data and operations"""
    
    def __init__(self):
        # Sample restaurant data for demonstration
        self.restaurants_data = [
            {
                'id': 'rest_001',
                'name': "Mario's Italian Bistro",
                'cuisine': 'italian',
                'rating': 4.5,
                'price_level': '$$',
                'distance': '0.3 miles',
                'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=300&h=200&fit=crop',
                'description': 'Authentic Italian cuisine with handmade pasta and wood-fired pizza',
                'popular_dishes': [
                    {'name': 'Margherita Pizza', 'price': '$18', 'image': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=200&h=150&fit=crop'},
                    {'name': 'Fettuccine Alfredo', 'price': '$16', 'image': 'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=200&h=150&fit=crop'},
                    {'name': 'Tiramisu', 'price': '$8', 'image': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=200&h=150&fit=crop'}
                ]
            },
            {
                'id': 'rest_002',
                'name': "Dragon Palace",
                'cuisine': 'chinese',
                'rating': 4.3,
                'price_level': '$$',
                'distance': '0.5 miles',
                'image': 'https://images.unsplash.com/photo-1525755662778-989d0524087e?w=300&h=200&fit=crop',
                'description': 'Traditional Chinese dishes with modern presentation',
                'popular_dishes': [
                    {'name': 'Sweet & Sour Pork', 'price': '$14', 'image': 'https://images.unsplash.com/photo-1559847844-d721426d6edc?w=200&h=150&fit=crop'},
                    {'name': 'Kung Pao Chicken', 'price': '$13', 'image': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=200&h=150&fit=crop'},
                    {'name': 'Fried Rice', 'price': '$10', 'image': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=200&h=150&fit=crop'}
                ]
            },
            {
                'id': 'rest_003',
                'name': "Taco Fiesta",
                'cuisine': 'mexican',
                'rating': 4.2,
                'price_level': '$',
                'distance': '0.2 miles',
                'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop',
                'description': 'Fresh Mexican flavors with authentic ingredients',
                'popular_dishes': [
                    {'name': 'Beef Tacos', 'price': '$12', 'image': 'https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=200&h=150&fit=crop'},
                    {'name': 'Chicken Burrito', 'price': '$11', 'image': 'https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=200&h=150&fit=crop'},
                    {'name': 'Guacamole & Chips', 'price': '$7', 'image': 'https://images.unsplash.com/photo-1553909489-cd47e0ef937f?w=200&h=150&fit=crop'}
                ]
            },
            {
                'id': 'rest_004',
                'name': "Spice Garden",
                'cuisine': 'indian',
                'rating': 4.6,
                'price_level': '$$',
                'distance': '0.7 miles',
                'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=300&h=200&fit=crop',
                'description': 'Aromatic Indian dishes with traditional spices',
                'popular_dishes': [
                    {'name': 'Butter Chicken', 'price': '$15', 'image': 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=200&h=150&fit=crop'},
                    {'name': 'Biryani', 'price': '$14', 'image': 'https://images.unsplash.com/photo-1563379091339-03246963d7d3?w=200&h=150&fit=crop'},
                    {'name': 'Naan Bread', 'price': '$4', 'image': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=200&h=150&fit=crop'}
                ]
            },
            {
                'id': 'rest_005',
                'name': "Sakura Sushi",
                'cuisine': 'japanese',
                'rating': 4.7,
                'price_level': '$$$',
                'distance': '0.4 miles',
                'image': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=300&h=200&fit=crop',
                'description': 'Fresh sushi and traditional Japanese dishes',
                'popular_dishes': [
                    {'name': 'Salmon Roll', 'price': '$12', 'image': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=200&h=150&fit=crop'},
                    {'name': 'Chicken Teriyaki', 'price': '$16', 'image': 'https://images.unsplash.com/photo-1580822184713-fc5400e7fe10?w=200&h=150&fit=crop'},
                    {'name': 'Miso Soup', 'price': '$5', 'image': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=200&h=150&fit=crop'}
                ]
            },
            {
                'id': 'rest_006',
                'name': "Burger Junction",
                'cuisine': 'american',
                'rating': 4.1,
                'price_level': '$',
                'distance': '0.1 miles',
                'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop',
                'description': 'Classic American burgers and comfort food',
                'popular_dishes': [
                    {'name': 'Classic Cheeseburger', 'price': '$9', 'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=200&h=150&fit=crop'},
                    {'name': 'Loaded Fries', 'price': '$6', 'image': 'https://images.unsplash.com/photo-1576107232684-1279f390859f?w=200&h=150&fit=crop'},
                    {'name': 'Milkshake', 'price': '$5', 'image': 'https://images.unsplash.com/photo-1541658016709-82535e94bc69?w=200&h=150&fit=crop'}
                ]
            }
        ]
    
    def get_restaurants_for_booking(self):
        """Get restaurants suitable for table booking"""
        restaurants = []
        for rest in self.restaurants_data:
            restaurant_card = {
                'type': 'restaurant',
                'id': rest['id'],
                'name': rest['name'],
                'image': rest['image'],
                'rating': rest['rating'],
                'price_level': rest['price_level'],
                'distance': rest['distance'],
                'description': rest['description'],
                'availability': self._get_random_availability(),
                'actions': [
                    {'text': 'Book Table', 'action': f"book_{rest['id']}"},
                    {'text': 'View Menu', 'action': f"menu_{rest['id']}"},
                    {'text': 'Reviews', 'action': f"reviews_{rest['id']}"}
                ]
            }
            restaurants.append(restaurant_card)
        
        # Sort by rating
        restaurants.sort(key=lambda x: x['rating'], reverse=True)
        return restaurants
    
    def get_restaurants_by_cuisine(self, cuisine):
        """Get restaurants filtered by cuisine type"""
        filtered_restaurants = [r for r in self.restaurants_data if r['cuisine'] == cuisine]
        
        restaurants = []
        for rest in filtered_restaurants:
            restaurant_card = {
                'type': 'restaurant',
                'id': rest['id'],
                'name': rest['name'],
                'image': rest['image'],
                'rating': rest['rating'],
                'price_level': rest['price_level'],
                'distance': rest['distance'],
                'description': rest['description'],
                'popular_dishes': rest['popular_dishes'][:2],  # Show top 2 dishes
                'actions': [
                    {'text': 'Order Now', 'action': f"order_{rest['id']}"},
                    {'text': 'Full Menu', 'action': f"menu_{rest['id']}"},
                    {'text': 'Book Table', 'action': f"book_{rest['id']}"}
                ]
            }
            restaurants.append(restaurant_card)
        
        return restaurants
    
    def get_popular_restaurants(self):
        """Get popular restaurants for general recommendations"""
        restaurants = []
        for rest in self.restaurants_data:
            restaurant_card = {
                'type': 'restaurant',
                'id': rest['id'],
                'name': rest['name'],
                'image': rest['image'],
                'rating': rest['rating'],
                'price_level': rest['price_level'],
                'distance': rest['distance'],
                'description': rest['description'],
                'popular_dishes': rest['popular_dishes'][:1],  # Show top dish
                'actions': [
                    {'text': 'View Menu', 'action': f"menu_{rest['id']}"},
                    {'text': 'Order Now', 'action': f"order_{rest['id']}"},
                    {'text': 'Book Table', 'action': f"book_{rest['id']}"}
                ]
            }
            restaurants.append(restaurant_card)
        
        # Sort by rating and return top 4
        restaurants.sort(key=lambda x: x['rating'], reverse=True)
        return restaurants[:4]
    
    def _get_random_availability(self):
        """Generate random availability slots for booking"""
        time_slots = []
        base_time = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)  # Start at 5 PM
        
        for i in range(6):  # 6 time slots
            slot_time = base_time + timedelta(minutes=30 * i)
            if random.random() > 0.3:  # 70% chance of availability
                time_slots.append({
                    'time': slot_time.strftime('%I:%M %p'),
                    'available': True
                })
        
        return time_slots
    
    def get_restaurant_menu(self, restaurant_id):
        """Get full menu for a specific restaurant"""
        restaurant = next((r for r in self.restaurants_data if r['id'] == restaurant_id), None)
        if restaurant:
            return restaurant['popular_dishes']
        return []
