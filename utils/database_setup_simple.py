from models import db, Restaurant, Dish, AvailabilitySlot
from datetime import datetime, date
import random

def populate_restaurants():
    """Populate the database with comprehensive restaurant data"""
    
    restaurants_data = [
        {
            'name': "Mario's Italian Bistro",
            'address': '123 Little Italy St',
            'city': 'New York',
            'state': 'NY',
            'postal_code': '10012',
            'phone': '(212) 555-0123',
            'email': 'info@mariositalian.com',
            'cuisine': 'italian',
            'cuisine_types': ['italian', 'mediterranean'],
            'price_level': '$$',
            'rating': 4.5,
            'operating_hours': {
                'monday': {'open': '11:00', 'close': '22:00'},
                'tuesday': {'open': '11:00', 'close': '22:00'},
                'wednesday': {'open': '11:00', 'close': '22:00'},
                'thursday': {'open': '11:00', 'close': '22:00'},
                'friday': {'open': '11:00', 'close': '23:00'},
                'saturday': {'open': '11:00', 'close': '23:00'},
                'sunday': {'open': '12:00', 'close': '22:00'}
            },
            'services_offered': ['dine_in', 'takeout', 'delivery'],
            'delivery_radius': 3.0,
            'delivery_fee': 3.99,
            'minimum_order_amount': 15.00,
            'average_preparation_time': 25,
            'table_capacity': 80,
            'special_features': ['outdoor_seating', 'wheelchair_accessible', 'parking'],
            'payment_methods': ['credit_card', 'debit_card', 'cash', 'digital_wallet'],
            'image_url': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=300&h=200&fit=crop',
            'description': 'Authentic Italian cuisine with handmade pasta and wood-fired pizza',
            'distance': '0.3 miles'
        },
        {
            'name': "Dragon Palace",
            'address': '456 Chinatown Ave',
            'city': 'New York',
            'state': 'NY',
            'postal_code': '10013',
            'phone': '(212) 555-0456',
            'email': 'info@dragonpalace.com',
            'cuisine': 'chinese',
            'cuisine_types': ['chinese', 'asian'],
            'price_level': '$$',
            'rating': 4.3,
            'operating_hours': {
                'monday': {'open': '12:00', 'close': '21:30'},
                'tuesday': {'open': '12:00', 'close': '21:30'},
                'wednesday': {'open': '12:00', 'close': '21:30'},
                'thursday': {'open': '12:00', 'close': '21:30'},
                'friday': {'open': '12:00', 'close': '22:00'},
                'saturday': {'open': '12:00', 'close': '22:00'},
                'sunday': {'open': '12:00', 'close': '21:30'}
            },
            'services_offered': ['dine_in', 'takeout', 'delivery'],
            'delivery_radius': 2.5,
            'delivery_fee': 2.99,
            'minimum_order_amount': 20.00,
            'average_preparation_time': 20,
            'table_capacity': 60,
            'special_features': ['wheelchair_accessible', 'parking'],
            'payment_methods': ['credit_card', 'debit_card', 'cash', 'digital_wallet'],
            'image_url': 'https://images.unsplash.com/photo-1525755662778-989d0524087e?w=300&h=200&fit=crop',
            'description': 'Traditional Chinese dishes with modern presentation',
            'distance': '0.5 miles'
        }
    ]
    
    # Enhanced dish data with proper dietary tags and customization
    dishes_data = {
        'italian': [
            {
                'name': 'Margherita Pizza',
                'price': 18.00,
                'category': 'mains',
                'dietary_tags': ['vegetarian'],
                'preparation_time': 15,
                'customization_options': ['extra_cheese', 'gluten_free_crust', 'vegan_cheese'],
                'image_url': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=200&h=150&fit=crop',
                'description': 'Classic pizza with fresh mozzarella, tomatoes, and basil'
            },
            {
                'name': 'Fettuccine Alfredo',
                'price': 16.00,
                'category': 'mains',
                'dietary_tags': ['vegetarian'],
                'preparation_time': 12,
                'customization_options': ['add_chicken', 'add_shrimp', 'extra_parmesan'],
                'image_url': 'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=200&h=150&fit=crop',
                'description': 'Creamy pasta with rich Alfredo sauce and fresh herbs'
            },
            {
                'name': 'Tiramisu',
                'price': 8.00,
                'category': 'desserts',
                'dietary_tags': ['vegetarian'],
                'preparation_time': 5,
                'customization_options': ['extra_espresso', 'sugar_free'],
                'image_url': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=200&h=150&fit=crop',
                'description': 'Traditional Italian dessert with coffee-soaked ladyfingers'
            }
        ],
        'chinese': [
            {
                'name': 'Sweet & Sour Pork',
                'price': 14.00,
                'category': 'mains',
                'dietary_tags': [],
                'preparation_time': 18,
                'customization_options': ['spice_level', 'extra_vegetables', 'brown_rice'],
                'image_url': 'https://images.unsplash.com/photo-1559847844-d721426d6edc?w=200&h=150&fit=crop',
                'description': 'Tender pork in tangy sweet and sour sauce with pineapple'
            },
            {
                'name': 'Kung Pao Chicken',
                'price': 13.00,
                'category': 'mains',
                'dietary_tags': ['gluten_free_option'],
                'preparation_time': 15,
                'customization_options': ['spice_level', 'extra_peanuts', 'no_peanuts'],
                'image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=200&h=150&fit=crop',
                'description': 'Spicy stir-fried chicken with peanuts and vegetables'
            },
            {
                'name': 'Vegetable Fried Rice',
                'price': 10.00,
                'category': 'mains',
                'dietary_tags': ['vegetarian', 'vegan_option'],
                'preparation_time': 10,
                'customization_options': ['brown_rice', 'extra_vegetables', 'add_tofu'],
                'image_url': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=200&h=150&fit=crop',
                'description': 'Wok-fried rice with fresh vegetables and soy sauce'
            }
        ]
    }
    
    # Create restaurants with comprehensive data
    for rest_data in restaurants_data:
        restaurant = Restaurant(**rest_data)
        db.session.add(restaurant)
        db.session.flush()  # To get the ID
        
        # Add enhanced dishes
        cuisine_dishes = dishes_data.get(rest_data['cuisine'], [])
        for i, dish_data in enumerate(cuisine_dishes):
            dish = Dish(
                restaurant_id=restaurant.id,
                name=dish_data['name'],
                price=dish_data['price'],
                category=dish_data['category'],
                dietary_tags=dish_data['dietary_tags'],
                preparation_time=dish_data['preparation_time'],
                customization_options=dish_data['customization_options'],
                image_url=dish_data['image_url'],
                description=dish_data['description'],
                is_popular=i < 2,  # First 2 dishes are popular
                is_available=True
            )
            db.session.add(dish)
        
        # Add availability slots for reservations
        time_slots = ['5:00 PM', '5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM', '9:00 PM']
        for time_slot in time_slots:
            # 80% chance of being available
            is_available = random.random() > 0.2
            availability = AvailabilitySlot(
                restaurant_id=restaurant.id,
                time_slot=time_slot,
                is_available=is_available,
                date=date.today()
            )
            db.session.add(availability)
    
    db.session.commit()
    print(f"Database populated with {len(restaurants_data)} restaurants and comprehensive data!")