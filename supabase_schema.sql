-- DineDesk Restaurant Database Schema for Supabase
-- Run this SQL in your Supabase SQL Editor

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

-- Insert sample restaurant data
INSERT INTO restaurants (name, address, city, state, postal_code, phone, email, cuisine, cuisine_types, price_level, rating, operating_hours, services_offered, delivery_radius, delivery_fee, minimum_order_amount, average_preparation_time, table_capacity, special_features, payment_methods, is_active, image_url, description, distance) VALUES
('Mario''s Italian Bistro', '123 Little Italy St', 'New York', 'NY', '10012', '(212) 555-0123', 'info@mariositalian.com', 'italian', '["italian", "mediterranean"]', '$$', 4.5, '{"monday": {"open": "11:00", "close": "22:00"}, "tuesday": {"open": "11:00", "close": "22:00"}, "wednesday": {"open": "11:00", "close": "22:00"}, "thursday": {"open": "11:00", "close": "22:00"}, "friday": {"open": "11:00", "close": "23:00"}, "saturday": {"open": "11:00", "close": "23:00"}, "sunday": {"open": "12:00", "close": "22:00"}}', '["dine_in", "takeout", "delivery"]', 3.0, 3.99, 15.00, 25, 80, '["outdoor_seating", "wheelchair_accessible", "parking"]', '["credit_card", "debit_card", "cash", "digital_wallet"]', true, 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=300&h=200&fit=crop', 'Authentic Italian cuisine with handmade pasta and wood-fired pizza', '0.3 miles'),

('Dragon Palace', '456 Chinatown Ave', 'New York', 'NY', '10013', '(212) 555-0456', 'info@dragonpalace.com', 'chinese', '["chinese", "asian"]', '$$', 4.3, '{"monday": {"open": "12:00", "close": "21:30"}, "tuesday": {"open": "12:00", "close": "21:30"}, "wednesday": {"open": "12:00", "close": "21:30"}, "thursday": {"open": "12:00", "close": "21:30"}, "friday": {"open": "12:00", "close": "22:00"}, "saturday": {"open": "12:00", "close": "22:00"}, "sunday": {"open": "12:00", "close": "21:30"}}', '["dine_in", "takeout", "delivery"]', 2.5, 2.99, 20.00, 20, 60, '["wheelchair_accessible", "parking"]', '["credit_card", "debit_card", "cash", "digital_wallet"]', true, 'https://images.unsplash.com/photo-1525755662778-989d0524087e?w=300&h=200&fit=crop', 'Traditional Chinese dishes with modern presentation', '0.5 miles'),

('Spice Garden', '321 Curry Lane', 'New York', 'NY', '10015', '(212) 555-0321', 'info@spicegarden.com', 'indian', '["indian", "asian"]', '$$', 4.6, '{"monday": {"open": "11:30", "close": "22:30"}, "tuesday": {"open": "11:30", "close": "22:30"}, "wednesday": {"open": "11:30", "close": "22:30"}, "thursday": {"open": "11:30", "close": "22:30"}, "friday": {"open": "11:30", "close": "23:00"}, "saturday": {"open": "11:30", "close": "23:00"}, "sunday": {"open": "12:00", "close": "22:30"}}', '["dine_in", "takeout", "delivery"]', 2.8, 3.49, 18.00, 22, 65, '["outdoor_seating", "wheelchair_accessible"]', '["credit_card", "debit_card", "cash", "digital_wallet"]', true, 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=300&h=200&fit=crop', 'Aromatic Indian dishes with traditional spices', '0.7 miles');

-- Insert sample dishes (will need restaurant IDs from above)
-- Mario's Italian Bistro dishes (assuming restaurant_id = 1)
INSERT INTO dishes (restaurant_id, name, price, description, category, dietary_tags, is_available, preparation_time, customization_options, image_url, is_popular) VALUES
(1, 'Margherita Pizza', 18.00, 'Classic pizza with fresh mozzarella, tomatoes, and basil', 'mains', '["vegetarian"]', true, 15, '["extra_cheese", "gluten_free_crust"]', 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=200&h=150&fit=crop', true),
(1, 'Fettuccine Alfredo', 16.00, 'Creamy pasta with rich Alfredo sauce and fresh herbs', 'mains', '["vegetarian"]', true, 12, '["add_chicken", "add_shrimp", "extra_parmesan"]', 'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=200&h=150&fit=crop', true),
(1, 'Caesar Salad', 12.00, 'Crisp romaine lettuce with classic Caesar dressing', 'appetizers', '["vegetarian"]', true, 8, '["add_chicken", "extra_croutons"]', 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=200&h=150&fit=crop', false),

-- Dragon Palace dishes (assuming restaurant_id = 2)
(2, 'Sweet & Sour Pork', 14.00, 'Tender pork in tangy sweet and sour sauce with pineapple', 'mains', '[]', true, 18, '["spice_level", "extra_vegetables", "brown_rice"]', 'https://images.unsplash.com/photo-1559847844-d721426d6edc?w=200&h=150&fit=crop', true),
(2, 'Kung Pao Chicken', 13.00, 'Spicy stir-fried chicken with peanuts and vegetables', 'mains', '["gluten_free_option"]', true, 15, '["spice_level", "extra_peanuts", "no_peanuts"]', 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=200&h=150&fit=crop', true),
(2, 'Spring Rolls', 8.00, 'Crispy vegetable spring rolls with sweet chili sauce', 'appetizers', '["vegetarian"]', true, 10, '["extra_sauce"]', 'https://images.unsplash.com/photo-1544025162-d76694265947?w=200&h=150&fit=crop', false),

-- Spice Garden dishes (assuming restaurant_id = 3)
(3, 'Butter Chicken', 15.00, 'Creamy tomato-based curry with tender chicken', 'mains', '["gluten_free"]', true, 20, '["spice_level", "extra_rice", "vegan_option"]', 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=200&h=150&fit=crop', true),
(3, 'Chicken Biryani', 14.00, 'Fragrant basmati rice with spiced chicken and vegetables', 'mains', '["gluten_free"]', true, 25, '["meat_choice", "spice_level", "extra_raita"]', 'https://images.unsplash.com/photo-1563379091339-03246963d7d3?w=200&h=150&fit=crop', true),
(3, 'Samosas', 6.00, 'Crispy pastries filled with spiced potatoes and peas', 'appetizers', '["vegetarian", "vegan_option"]', true, 12, '["extra_chutney"]', 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=200&h=150&fit=crop', false);

-- Insert availability slots for all restaurants
INSERT INTO availability_slots (restaurant_id, time_slot, is_available, date) VALUES
-- Mario's Italian Bistro (restaurant_id = 1)
(1, '5:00 PM', true, CURRENT_DATE),
(1, '5:30 PM', true, CURRENT_DATE),
(1, '6:00 PM', true, CURRENT_DATE),
(1, '6:30 PM', false, CURRENT_DATE),
(1, '7:00 PM', true, CURRENT_DATE),
(1, '7:30 PM', true, CURRENT_DATE),
(1, '8:00 PM', false, CURRENT_DATE),
(1, '8:30 PM', true, CURRENT_DATE),
(1, '9:00 PM', true, CURRENT_DATE),

-- Dragon Palace (restaurant_id = 2)
(2, '5:00 PM', true, CURRENT_DATE),
(2, '5:30 PM', false, CURRENT_DATE),
(2, '6:00 PM', true, CURRENT_DATE),
(2, '6:30 PM', true, CURRENT_DATE),
(2, '7:00 PM', false, CURRENT_DATE),
(2, '7:30 PM', true, CURRENT_DATE),
(2, '8:00 PM', true, CURRENT_DATE),
(2, '8:30 PM', true, CURRENT_DATE),
(2, '9:00 PM', false, CURRENT_DATE),

-- Spice Garden (restaurant_id = 3)
(3, '5:00 PM', false, CURRENT_DATE),
(3, '5:30 PM', true, CURRENT_DATE),
(3, '6:00 PM', true, CURRENT_DATE),
(3, '6:30 PM', true, CURRENT_DATE),
(3, '7:00 PM', true, CURRENT_DATE),
(3, '7:30 PM', false, CURRENT_DATE),
(3, '8:00 PM', true, CURRENT_DATE),
(3, '8:30 PM', true, CURRENT_DATE),
(3, '9:00 PM', true, CURRENT_DATE);