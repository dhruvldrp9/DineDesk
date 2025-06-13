#!/usr/bin/env python3
"""
Script to create tables in Supabase using direct SQL execution via REST API
"""
import os
import requests

def create_supabase_tables_via_api():
    """Create tables in Supabase using SQL API"""
    
    supabase_url = os.environ.get('SUPABASE_URL')
    service_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    
    if not supabase_url or not service_key:
        print("Missing Supabase credentials")
        return False
    
    # SQL to create all tables
    create_tables_sql = """
-- Create restaurants table
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
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create dishes table
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
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create availability_slots table
CREATE TABLE IF NOT EXISTS availability_slots (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants(id) ON DELETE CASCADE,
    time_slot VARCHAR(20) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create customers table
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
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create bookings table
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
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create chat_sessions table
CREATE TABLE IF NOT EXISTS chat_sessions (
    id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    started_at TIMESTAMP DEFAULT NOW(),
    last_activity TIMESTAMP DEFAULT NOW(),
    message_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create chat_messages table
CREATE TABLE IF NOT EXISTS chat_messages (
    id VARCHAR(36) PRIMARY KEY,
    chat_session_id VARCHAR(36) REFERENCES chat_sessions(id) ON DELETE CASCADE,
    message_type VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    message_data JSONB,
    timestamp TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);
"""
    
    try:
        # Execute SQL via Supabase REST API
        headers = {
            'apikey': service_key,
            'Authorization': f'Bearer {service_key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }
        
        # Use the SQL RPC endpoint
        response = requests.post(
            f"{supabase_url}/rest/v1/rpc/exec_sql",
            headers=headers,
            json={'query': create_tables_sql}
        )
        
        if response.status_code == 200:
            print("Tables created successfully via Supabase API")
            return populate_restaurant_data(supabase_url, service_key)
        else:
            print(f"Failed to create tables: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error creating tables via API: {e}")
        return False

def populate_restaurant_data(supabase_url, service_key):
    """Populate restaurant data using Supabase REST API"""
    
    headers = {
        'apikey': service_key,
        'Authorization': f'Bearer {service_key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    
    try:
        # Check if restaurants already exist
        response = requests.get(
            f"{supabase_url}/rest/v1/restaurants?select=id&limit=1",
            headers=headers
        )
        
        if response.status_code == 200 and len(response.json()) > 0:
            print("Restaurant data already exists")
            return True
        
        # Sample restaurant data
        restaurants = [
            {
                "name": "Mario's Italian Bistro",
                "address": "123 Little Italy St",
                "city": "New York",
                "state": "NY",
                "postal_code": "10012",
                "phone": "(212) 555-0123",
                "email": "info@mariositalian.com",
                "cuisine": "italian",
                "cuisine_types": ["italian", "mediterranean"],
                "price_level": "$$",
                "rating": 4.5,
                "operating_hours": {
                    "monday": {"open": "11:00", "close": "22:00"},
                    "tuesday": {"open": "11:00", "close": "22:00"},
                    "wednesday": {"open": "11:00", "close": "22:00"},
                    "thursday": {"open": "11:00", "close": "22:00"},
                    "friday": {"open": "11:00", "close": "23:00"},
                    "saturday": {"open": "11:00", "close": "23:00"},
                    "sunday": {"open": "12:00", "close": "22:00"}
                },
                "services_offered": ["dine_in", "takeout", "delivery"],
                "delivery_radius": 3.0,
                "delivery_fee": 3.99,
                "minimum_order_amount": 15.00,
                "average_preparation_time": 25,
                "table_capacity": 80,
                "special_features": ["outdoor_seating", "wheelchair_accessible", "parking"],
                "payment_methods": ["credit_card", "debit_card", "cash", "digital_wallet"],
                "is_active": True,
                "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=300&h=200&fit=crop",
                "description": "Authentic Italian cuisine with handmade pasta and wood-fired pizza",
                "distance": "0.3 miles"
            },
            {
                "name": "Dragon Palace",
                "address": "456 Chinatown Ave",
                "city": "New York",
                "state": "NY",
                "postal_code": "10013",
                "phone": "(212) 555-0456",
                "email": "info@dragonpalace.com",
                "cuisine": "chinese",
                "cuisine_types": ["chinese", "asian"],
                "price_level": "$$",
                "rating": 4.3,
                "operating_hours": {
                    "monday": {"open": "12:00", "close": "21:30"},
                    "tuesday": {"open": "12:00", "close": "21:30"},
                    "wednesday": {"open": "12:00", "close": "21:30"},
                    "thursday": {"open": "12:00", "close": "21:30"},
                    "friday": {"open": "12:00", "close": "22:00"},
                    "saturday": {"open": "12:00", "close": "22:00"},
                    "sunday": {"open": "12:00", "close": "21:30"}
                },
                "services_offered": ["dine_in", "takeout", "delivery"],
                "delivery_radius": 2.5,
                "delivery_fee": 2.99,
                "minimum_order_amount": 20.00,
                "average_preparation_time": 20,
                "table_capacity": 60,
                "special_features": ["wheelchair_accessible", "parking"],
                "payment_methods": ["credit_card", "debit_card", "cash", "digital_wallet"],
                "is_active": True,
                "image_url": "https://images.unsplash.com/photo-1525755662778-989d0524087e?w=300&h=200&fit=crop",
                "description": "Traditional Chinese dishes with modern presentation",
                "distance": "0.5 miles"
            },
            {
                "name": "Spice Garden",
                "address": "321 Curry Lane",
                "city": "New York",
                "state": "NY",
                "postal_code": "10015",
                "phone": "(212) 555-0321",
                "email": "info@spicegarden.com",
                "cuisine": "indian",
                "cuisine_types": ["indian", "asian"],
                "price_level": "$$",
                "rating": 4.6,
                "operating_hours": {
                    "monday": {"open": "11:30", "close": "22:30"},
                    "tuesday": {"open": "11:30", "close": "22:30"},
                    "wednesday": {"open": "11:30", "close": "22:30"},
                    "thursday": {"open": "11:30", "close": "22:30"},
                    "friday": {"open": "11:30", "close": "23:00"},
                    "saturday": {"open": "11:30", "close": "23:00"},
                    "sunday": {"open": "12:00", "close": "22:30"}
                },
                "services_offered": ["dine_in", "takeout", "delivery"],
                "delivery_radius": 2.8,
                "delivery_fee": 3.49,
                "minimum_order_amount": 18.00,
                "average_preparation_time": 22,
                "table_capacity": 65,
                "special_features": ["outdoor_seating", "wheelchair_accessible"],
                "payment_methods": ["credit_card", "debit_card", "cash", "digital_wallet"],
                "is_active": True,
                "image_url": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=300&h=200&fit=crop",
                "description": "Aromatic Indian dishes with traditional spices",
                "distance": "0.7 miles"
            }
        ]
        
        # Insert restaurants
        response = requests.post(
            f"{supabase_url}/rest/v1/restaurants",
            headers=headers,
            json=restaurants
        )
        
        if response.status_code in [201, 200]:
            restaurant_data = response.json()
            print(f"Inserted {len(restaurant_data)} restaurants")
            
            # Add dishes for each restaurant
            for i, restaurant in enumerate(restaurant_data):
                restaurant_id = restaurant['id']
                
                if i == 0:  # Mario's Italian
                    dishes = [
                        {
                            "restaurant_id": restaurant_id,
                            "name": "Margherita Pizza",
                            "price": 18.00,
                            "description": "Classic pizza with fresh mozzarella, tomatoes, and basil",
                            "category": "mains",
                            "dietary_tags": ["vegetarian"],
                            "is_available": True,
                            "preparation_time": 15,
                            "customization_options": ["extra_cheese", "gluten_free_crust"],
                            "image_url": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=200&h=150&fit=crop",
                            "is_popular": True
                        },
                        {
                            "restaurant_id": restaurant_id,
                            "name": "Fettuccine Alfredo",
                            "price": 16.00,
                            "description": "Creamy pasta with rich Alfredo sauce and fresh herbs",
                            "category": "mains",
                            "dietary_tags": ["vegetarian"],
                            "is_available": True,
                            "preparation_time": 12,
                            "customization_options": ["add_chicken", "add_shrimp", "extra_parmesan"],
                            "image_url": "https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=200&h=150&fit=crop",
                            "is_popular": True
                        }
                    ]
                elif i == 1:  # Dragon Palace
                    dishes = [
                        {
                            "restaurant_id": restaurant_id,
                            "name": "Sweet & Sour Pork",
                            "price": 14.00,
                            "description": "Tender pork in tangy sweet and sour sauce with pineapple",
                            "category": "mains",
                            "dietary_tags": [],
                            "is_available": True,
                            "preparation_time": 18,
                            "customization_options": ["spice_level", "extra_vegetables", "brown_rice"],
                            "image_url": "https://images.unsplash.com/photo-1559847844-d721426d6edc?w=200&h=150&fit=crop",
                            "is_popular": True
                        },
                        {
                            "restaurant_id": restaurant_id,
                            "name": "Kung Pao Chicken",
                            "price": 13.00,
                            "description": "Spicy stir-fried chicken with peanuts and vegetables",
                            "category": "mains",
                            "dietary_tags": ["gluten_free_option"],
                            "is_available": True,
                            "preparation_time": 15,
                            "customization_options": ["spice_level", "extra_peanuts", "no_peanuts"],
                            "image_url": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=200&h=150&fit=crop",
                            "is_popular": True
                        }
                    ]
                else:  # Spice Garden
                    dishes = [
                        {
                            "restaurant_id": restaurant_id,
                            "name": "Butter Chicken",
                            "price": 15.00,
                            "description": "Creamy tomato-based curry with tender chicken",
                            "category": "mains",
                            "dietary_tags": ["gluten_free"],
                            "is_available": True,
                            "preparation_time": 20,
                            "customization_options": ["spice_level", "extra_rice", "vegan_option"],
                            "image_url": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=200&h=150&fit=crop",
                            "is_popular": True
                        },
                        {
                            "restaurant_id": restaurant_id,
                            "name": "Chicken Biryani",
                            "price": 14.00,
                            "description": "Fragrant basmati rice with spiced chicken and vegetables",
                            "category": "mains",
                            "dietary_tags": ["gluten_free"],
                            "is_available": True,
                            "preparation_time": 25,
                            "customization_options": ["meat_choice", "spice_level", "extra_raita"],
                            "image_url": "https://images.unsplash.com/photo-1563379091339-03246963d7d3?w=200&h=150&fit=crop",
                            "is_popular": True
                        }
                    ]
                
                # Insert dishes
                requests.post(
                    f"{supabase_url}/rest/v1/dishes",
                    headers=headers,
                    json=dishes
                )
                
                # Add availability slots
                time_slots = ['5:00 PM', '5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM', '9:00 PM']
                availability_data = []
                
                for time_slot in time_slots:
                    import random
                    availability_data.append({
                        "restaurant_id": restaurant_id,
                        "time_slot": time_slot,
                        "is_available": random.random() > 0.2  # 80% chance available
                    })
                
                requests.post(
                    f"{supabase_url}/rest/v1/availability_slots",
                    headers=headers,
                    json=availability_data
                )
            
            print("Successfully populated all restaurant data")
            return True
        else:
            print(f"Failed to insert restaurants: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error populating restaurant data: {e}")
        return False

if __name__ == "__main__":
    success = create_supabase_tables_via_api()
    if success:
        print("Supabase setup completed successfully!")
    else:
        print("Supabase setup failed")