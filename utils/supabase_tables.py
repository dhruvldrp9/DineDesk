from config_supabase import supabase
import logging
import random
from datetime import date

def create_tables_if_not_exist():
    """Verify Supabase tables exist and are accessible"""
    try:
        # Try to access restaurants table to verify connection
        result = supabase.table('restaurants').select('id').limit(1).execute()
        logging.info("Supabase connection verified")
        return True
    except Exception as e:
        logging.error(f"Supabase connection error: {e}")
        # Tables need to be created manually via Supabase dashboard
        return False

def populate_initial_data():
    """Populate initial restaurant data directly via Supabase client"""
    try:
        # Check if restaurants table has data
        result = supabase.table('restaurants').select('id').limit(1).execute()
        
        if len(result.data) == 0:
            logging.info("Populating initial restaurant data...")
            
            # Restaurant data
            restaurants = [
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
                    'is_active': True,
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
                    'is_active': True,
                    'image_url': 'https://images.unsplash.com/photo-1525755662778-989d0524087e?w=300&h=200&fit=crop',
                    'description': 'Traditional Chinese dishes with modern presentation',
                    'distance': '0.5 miles'
                },
                {
                    'name': "Spice Garden",
                    'address': '321 Curry Lane',
                    'city': 'New York',
                    'state': 'NY',
                    'postal_code': '10015',
                    'phone': '(212) 555-0321',
                    'email': 'info@spicegarden.com',
                    'cuisine': 'indian',
                    'cuisine_types': ['indian', 'asian'],
                    'price_level': '$$',
                    'rating': 4.6,
                    'operating_hours': {
                        'monday': {'open': '11:30', 'close': '22:30'},
                        'tuesday': {'open': '11:30', 'close': '22:30'},
                        'wednesday': {'open': '11:30', 'close': '22:30'},
                        'thursday': {'open': '11:30', 'close': '22:30'},
                        'friday': {'open': '11:30', 'close': '23:00'},
                        'saturday': {'open': '11:30', 'close': '23:00'},
                        'sunday': {'open': '12:00', 'close': '22:30'}
                    },
                    'services_offered': ['dine_in', 'takeout', 'delivery'],
                    'delivery_radius': 2.8,
                    'delivery_fee': 3.49,
                    'minimum_order_amount': 18.00,
                    'average_preparation_time': 22,
                    'table_capacity': 65,
                    'special_features': ['outdoor_seating', 'wheelchair_accessible'],
                    'payment_methods': ['credit_card', 'debit_card', 'cash', 'digital_wallet'],
                    'is_active': True,
                    'image_url': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=300&h=200&fit=crop',
                    'description': 'Aromatic Indian dishes with traditional spices',
                    'distance': '0.7 miles'
                }
            ]
            
            # Insert restaurants and get their IDs
            for restaurant_data in restaurants:
                result = supabase.table('restaurants').insert(restaurant_data).execute()
                restaurant_id = result.data[0]['id']
                
                # Add dishes for each restaurant
                if restaurant_data['cuisine'] == 'italian':
                    dishes = [
                        {
                            'restaurant_id': restaurant_id,
                            'name': 'Margherita Pizza',
                            'price': 18.00,
                            'description': 'Classic pizza with fresh mozzarella, tomatoes, and basil',
                            'category': 'mains',
                            'dietary_tags': ['vegetarian'],
                            'is_available': True,
                            'preparation_time': 15,
                            'customization_options': ['extra_cheese', 'gluten_free_crust'],
                            'image_url': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=200&h=150&fit=crop',
                            'is_popular': True
                        },
                        {
                            'restaurant_id': restaurant_id,
                            'name': 'Fettuccine Alfredo',
                            'price': 16.00,
                            'description': 'Creamy pasta with rich Alfredo sauce and fresh herbs',
                            'category': 'mains',
                            'dietary_tags': ['vegetarian'],
                            'is_available': True,
                            'preparation_time': 12,
                            'customization_options': ['add_chicken', 'add_shrimp', 'extra_parmesan'],
                            'image_url': 'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=200&h=150&fit=crop',
                            'is_popular': True
                        }
                    ]
                elif restaurant_data['cuisine'] == 'chinese':
                    dishes = [
                        {
                            'restaurant_id': restaurant_id,
                            'name': 'Sweet & Sour Pork',
                            'price': 14.00,
                            'description': 'Tender pork in tangy sweet and sour sauce with pineapple',
                            'category': 'mains',
                            'dietary_tags': [],
                            'is_available': True,
                            'preparation_time': 18,
                            'customization_options': ['spice_level', 'extra_vegetables', 'brown_rice'],
                            'image_url': 'https://images.unsplash.com/photo-1559847844-d721426d6edc?w=200&h=150&fit=crop',
                            'is_popular': True
                        },
                        {
                            'restaurant_id': restaurant_id,
                            'name': 'Kung Pao Chicken',
                            'price': 13.00,
                            'description': 'Spicy stir-fried chicken with peanuts and vegetables',
                            'category': 'mains',
                            'dietary_tags': ['gluten_free_option'],
                            'is_available': True,
                            'preparation_time': 15,
                            'customization_options': ['spice_level', 'extra_peanuts', 'no_peanuts'],
                            'image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=200&h=150&fit=crop',
                            'is_popular': True
                        }
                    ]
                else:  # indian
                    dishes = [
                        {
                            'restaurant_id': restaurant_id,
                            'name': 'Butter Chicken',
                            'price': 15.00,
                            'description': 'Creamy tomato-based curry with tender chicken',
                            'category': 'mains',
                            'dietary_tags': ['gluten_free'],
                            'is_available': True,
                            'preparation_time': 20,
                            'customization_options': ['spice_level', 'extra_rice', 'vegan_option'],
                            'image_url': 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=200&h=150&fit=crop',
                            'is_popular': True
                        },
                        {
                            'restaurant_id': restaurant_id,
                            'name': 'Chicken Biryani',
                            'price': 14.00,
                            'description': 'Fragrant basmati rice with spiced chicken and vegetables',
                            'category': 'mains',
                            'dietary_tags': ['gluten_free'],
                            'is_available': True,
                            'preparation_time': 25,
                            'customization_options': ['meat_choice', 'spice_level', 'extra_raita'],
                            'image_url': 'https://images.unsplash.com/photo-1563379091339-03246963d7d3?w=200&h=150&fit=crop',
                            'is_popular': True
                        }
                    ]
                
                # Insert dishes
                supabase.table('dishes').insert(dishes).execute()
                
                # Add availability slots
                time_slots = ['5:00 PM', '5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM', '9:00 PM']
                availability_data = []
                for time_slot in time_slots:
                    availability_data.append({
                        'restaurant_id': restaurant_id,
                        'time_slot': time_slot,
                        'is_available': random.random() > 0.2,  # 80% chance available
                        'date': str(date.today())
                    })
                
                supabase.table('availability_slots').insert(availability_data).execute()
                logging.info(f"Added restaurant: {restaurant_data['name']}")
                
        else:
            logging.info("Restaurant data already exists in Supabase")
            
    except Exception as e:
        logging.error(f"Error populating data: {e}")

def initialize_supabase():
    """Main function to initialize Supabase tables and data"""
    logging.info("Initializing Supabase database...")
    if create_tables_if_not_exist():
        populate_initial_data()
    else:
        logging.error("Tables need to be created manually in Supabase dashboard")
    logging.info("Supabase initialization complete")

if __name__ == "__main__":
    initialize_supabase()