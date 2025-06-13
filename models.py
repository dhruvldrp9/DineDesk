import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    cuisine = db.Column(db.String(50), nullable=False)  # Primary cuisine
    cuisine_types = db.Column(db.JSON, nullable=True)  # Array of all cuisines
    price_level = db.Column(db.String(10), nullable=False)  # $, $$, $$$, $$$$
    rating = db.Column(db.Float, nullable=False)
    operating_hours = db.Column(db.JSON, nullable=True)  # {day: {open, close}}
    services_offered = db.Column(db.JSON, nullable=False, default=['dine_in'])  # Array
    delivery_radius = db.Column(db.Float, nullable=True)  # In miles
    delivery_fee = db.Column(db.Float, nullable=True)
    minimum_order_amount = db.Column(db.Float, nullable=True)
    average_preparation_time = db.Column(db.Integer, nullable=True)  # Minutes
    table_capacity = db.Column(db.Integer, nullable=True)
    special_features = db.Column(db.JSON, nullable=True)  # Array
    payment_methods = db.Column(db.JSON, nullable=True)  # Array
    is_active = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    distance = db.Column(db.String(20), nullable=False)  # Legacy field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    dishes = db.relationship('Dish', backref='restaurant', lazy=True, cascade='all, delete-orphan')
    availability_slots = db.relationship('AvailabilitySlot', backref='restaurant', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='restaurant', lazy=True)

class Dish(db.Model):
    __tablename__ = 'dishes'
    
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)  # appetizers, mains, desserts, beverages
    dietary_tags = db.Column(db.JSON, nullable=True)  # veg, vegan, gluten-free, etc.
    is_available = db.Column(db.Boolean, default=True)
    preparation_time = db.Column(db.Integer, nullable=True)  # Minutes
    customization_options = db.Column(db.JSON, nullable=True)
    image_url = db.Column(db.String(500), nullable=False)
    is_popular = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AvailabilitySlot(db.Model):
    __tablename__ = 'availability_slots'
    
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)  # e.g., "6:00 PM"
    is_available = db.Column(db.Boolean, default=True)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=True)
    addresses = db.Column(db.JSON, nullable=True)  # Array of delivery addresses
    dietary_preferences = db.Column(db.JSON, nullable=True)  # Array
    favorite_cuisines = db.Column(db.JSON, nullable=True)  # Array
    preferred_restaurants = db.Column(db.JSON, nullable=True)  # Array of restaurant IDs
    loyalty_points = db.Column(db.Integer, default=0)
    payment_methods = db.Column(db.JSON, nullable=True)  # Array
    communication_preferences = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='customer', lazy=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    booking_type = db.Column(db.String(20), nullable=False)  # "reservation" or "delivery"
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.String(20), nullable=False)
    party_size = db.Column(db.Integer, nullable=True)  # For reservations
    special_requests = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    total_amount = db.Column(db.Float, nullable=True)  # For orders
    items_ordered = db.Column(db.JSON, nullable=True)  # For delivery orders
    delivery_address = db.Column(db.JSON, nullable=True)  # For delivery
    payment_status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.String(36), primary_key=True)  # UUID
    session_id = db.Column(db.String(255), nullable=False)  # Flask session ID
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    message_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='active')  # active, ended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('ChatMessage', backref='chat_session', lazy=True, cascade='all, delete-orphan')

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.String(36), primary_key=True)  # UUID
    chat_session_id = db.Column(db.String(36), db.ForeignKey('chat_sessions.id'), nullable=False)
    message_type = db.Column(db.String(20), nullable=False)  # user, bot
    content = db.Column(db.Text, nullable=False)
    message_data = db.Column(db.JSON, nullable=True)  # For cards, quick replies, etc.
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)