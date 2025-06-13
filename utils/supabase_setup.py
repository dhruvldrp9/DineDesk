from config_supabase import supabase
from models import db, Restaurant, Dish, AvailabilitySlot, Customer, Booking, ChatSession, ChatMessage
from datetime import datetime, date
import random

def create_supabase_tables():
    """Create tables in Supabase using SQL"""
    
    # Create restaurants table
    restaurants_sql = """
    CREATE TABLE IF NOT EXISTS restaurants (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        address VARCHAR(200) NOT NULL,
        city VARCHAR(100) NOT NULL,
        state VARCHAR(50) NOT NULL,
        postal_code VARCHAR(20) NOT NULL,
        phone VARCHAR(20),
        email VARCHAR(120),
        cuisine VARCHAR(50) NOT NULL,
        cuisine_types JSONB,
        price_level VARCHAR(10) NOT NULL,
        rating FLOAT NOT NULL,
        operating_hours JSONB,
        services_offered JSONB NOT NULL DEFAULT '["dine_in"]',
        delivery_radius FLOAT,
        delivery_fee FLOAT,
        minimum_order_amount FLOAT,
        average_preparation_time INTEGER,
        table_capacity INTEGER,
        special_features JSONB,
        payment_methods JSONB,
        is_active BOOLEAN DEFAULT TRUE,
        image_url VARCHAR(500) NOT NULL,
        description TEXT NOT NULL,
        distance VARCHAR(20) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Create dishes table
    dishes_sql = """
    CREATE TABLE IF NOT EXISTS dishes (
        id SERIAL PRIMARY KEY,
        restaurant_id INTEGER REFERENCES restaurants(id) ON DELETE CASCADE,
        name VARCHAR(100) NOT NULL,
        price FLOAT NOT NULL,
        description TEXT,
        category VARCHAR(50) NOT NULL,
        dietary_tags JSONB,
        is_available BOOLEAN DEFAULT TRUE,
        preparation_time INTEGER,
        customization_options JSONB,
        image_url VARCHAR(500) NOT NULL,
        is_popular BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Create availability_slots table
    availability_sql = """
    CREATE TABLE IF NOT EXISTS availability_slots (
        id SERIAL PRIMARY KEY,
        restaurant_id INTEGER REFERENCES restaurants(id) ON DELETE CASCADE,
        time_slot VARCHAR(20) NOT NULL,
        is_available BOOLEAN DEFAULT TRUE,
        date DATE DEFAULT CURRENT_DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Create customers table
    customers_sql = """
    CREATE TABLE IF NOT EXISTS customers (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        phone_number VARCHAR(20) NOT NULL UNIQUE,
        email VARCHAR(120),
        addresses JSONB,
        dietary_preferences JSONB,
        favorite_cuisines JSONB,
        preferred_restaurants JSONB,
        loyalty_points INTEGER DEFAULT 0,
        payment_methods JSONB,
        communication_preferences JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Create bookings table
    bookings_sql = """
    CREATE TABLE IF NOT EXISTS bookings (
        id SERIAL PRIMARY KEY,
        customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
        restaurant_id INTEGER REFERENCES restaurants(id) ON DELETE CASCADE,
        booking_type VARCHAR(20) NOT NULL,
        booking_date DATE NOT NULL,
        booking_time VARCHAR(20) NOT NULL,
        party_size INTEGER,
        special_requests TEXT,
        status VARCHAR(20) DEFAULT 'pending',
        total_amount FLOAT,
        items_ordered JSONB,
        delivery_address JSONB,
        payment_status VARCHAR(20) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Create chat_sessions table
    chat_sessions_sql = """
    CREATE TABLE IF NOT EXISTS chat_sessions (
        id VARCHAR(36) PRIMARY KEY,
        session_id VARCHAR(255) NOT NULL,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        message_count INTEGER DEFAULT 0,
        status VARCHAR(20) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Create chat_messages table
    chat_messages_sql = """
    CREATE TABLE IF NOT EXISTS chat_messages (
        id VARCHAR(36) PRIMARY KEY,
        chat_session_id VARCHAR(36) REFERENCES chat_sessions(id) ON DELETE CASCADE,
        message_type VARCHAR(20) NOT NULL,
        content TEXT NOT NULL,
        message_data JSONB,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Execute table creation
    tables = [
        restaurants_sql,
        dishes_sql,
        availability_sql,
        customers_sql,
        bookings_sql,
        chat_sessions_sql,
        chat_messages_sql
    ]
    
    for table_sql in tables:
        try:
            result = supabase.rpc('exec_sql', {'sql': table_sql}).execute()
            print(f"Table created successfully")
        except Exception as e:
            # Try direct SQL execution
            try:
                supabase.postgrest.rpc('exec_sql', {'sql': table_sql}).execute()
            except Exception as e2:
                print(f"Error creating table: {e2}")

def populate_supabase_restaurants():
    """Populate Supabase with restaurant data"""
    
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
    
    # Insert restaurants using Supabase client
    for restaurant_data in restaurants_data:
        try:
            result = supabase.table('restaurants').insert(restaurant_data).execute()
            restaurant_id = result.data[0]['id']
            
            # Add dishes for each restaurant
            if restaurant_data['cuisine'] == 'italian':
                dishes = [
                    {
                        'restaurant_id': restaurant_id,
                        'name': 'Margherita Pizza',
                        'price': 18.00,
                        'category': 'mains',
                        'dietary_tags': ['vegetarian'],
                        'preparation_time': 15,
                        'customization_options': ['extra_cheese', 'gluten_free_crust'],
                        'image_url': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=200&h=150&fit=crop',
                        'description': 'Classic pizza with fresh mozzarella, tomatoes, and basil',
                        'is_popular': True
                    },
                    {
                        'restaurant_id': restaurant_id,
                        'name': 'Fettuccine Alfredo',
                        'price': 16.00,
                        'category': 'mains',
                        'dietary_tags': ['vegetarian'],
                        'preparation_time': 12,
                        'customization_options': ['add_chicken', 'add_shrimp'],
                        'image_url': 'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=200&h=150&fit=crop',
                        'description': 'Creamy pasta with rich Alfredo sauce',
                        'is_popular': True
                    }
                ]
            else:  # Chinese
                dishes = [
                    {
                        'restaurant_id': restaurant_id,
                        'name': 'Sweet & Sour Pork',
                        'price': 14.00,
                        'category': 'mains',
                        'dietary_tags': [],
                        'preparation_time': 18,
                        'customization_options': ['spice_level', 'extra_vegetables'],
                        'image_url': 'https://images.unsplash.com/photo-1559847844-d721426d6edc?w=200&h=150&fit=crop',
                        'description': 'Tender pork in tangy sweet and sour sauce',
                        'is_popular': True
                    },
                    {
                        'restaurant_id': restaurant_id,
                        'name': 'Kung Pao Chicken',
                        'price': 13.00,
                        'category': 'mains',
                        'dietary_tags': ['gluten_free_option'],
                        'preparation_time': 15,
                        'customization_options': ['spice_level', 'extra_peanuts'],
                        'image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=200&h=150&fit=crop',
                        'description': 'Spicy stir-fried chicken with peanuts',
                        'is_popular': True
                    }
                ]
            
            # Insert dishes
            supabase.table('dishes').insert(dishes).execute()
            
            # Add availability slots
            time_slots = ['5:00 PM', '5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM']
            availability_data = []
            for time_slot in time_slots:
                availability_data.append({
                    'restaurant_id': restaurant_id,
                    'time_slot': time_slot,
                    'is_available': random.random() > 0.2,  # 80% chance available
                    'date': str(date.today())
                })
            
            supabase.table('availability_slots').insert(availability_data).execute()
            print(f"Added restaurant: {restaurant_data['name']}")
            
        except Exception as e:
            print(f"Error adding restaurant {restaurant_data['name']}: {e}")

if __name__ == "__main__":
    create_supabase_tables()
    populate_supabase_restaurants()