from models import db, Restaurant, Dish, AvailabilitySlot
from datetime import datetime, date
import random

def populate_restaurants():
    """Populate the database with 25 restaurants and their data"""
    
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
        },
        {
            'name': "Taco Fiesta",
            'cuisine': 'mexican',
            'rating': 4.2,
            'price_level': '$',
            'distance': '0.2 miles',
            'image_url': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200&fit=crop',
            'description': 'Fresh Mexican flavors with authentic ingredients',
            'address': '789 Mexican Quarter, New York, NY 10014',
            'phone': '(212) 555-0789',
            'hours': 'Mon-Sun: 10:00 AM - 11:00 PM'
        },
        {
            'name': "Spice Garden",
            'cuisine': 'indian',
            'rating': 4.6,
            'price_level': '$$',
            'distance': '0.7 miles',
            'image_url': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=300&h=200&fit=crop',
            'description': 'Aromatic Indian dishes with traditional spices',
            'address': '321 Curry Lane, New York, NY 10015',
            'phone': '(212) 555-0321',
            'hours': 'Mon-Sun: 11:30 AM - 10:30 PM'
        },
        {
            'name': "Sakura Sushi",
            'cuisine': 'japanese',
            'rating': 4.7,
            'price_level': '$$$',
            'distance': '0.4 miles',
            'image_url': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=300&h=200&fit=crop',
            'description': 'Fresh sushi and traditional Japanese dishes',
            'address': '654 Sushi Row, New York, NY 10016',
            'phone': '(212) 555-0654',
            'hours': 'Mon-Sun: 5:00 PM - 11:00 PM'
        },
        {
            'name': "Burger Junction",
            'cuisine': 'american',
            'rating': 4.1,
            'price_level': '$',
            'distance': '0.1 miles',
            'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop',
            'description': 'Classic American burgers and comfort food',
            'address': '987 Burger Blvd, New York, NY 10017',
            'phone': '(212) 555-0987',
            'hours': 'Mon-Sun: 11:00 AM - 12:00 AM'
        },
        {
            'name': "Le Petit Café",
            'cuisine': 'french',
            'rating': 4.8,
            'price_level': '$$$',
            'distance': '0.6 miles',
            'image_url': 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=300&h=200&fit=crop',
            'description': 'Elegant French cuisine with wine pairings',
            'address': '159 French Quarter, New York, NY 10018',
            'phone': '(212) 555-0159',
            'hours': 'Tue-Sun: 6:00 PM - 10:00 PM'
        },
        {
            'name': "Bangkok Street",
            'cuisine': 'thai',
            'rating': 4.4,
            'price_level': '$$',
            'distance': '0.8 miles',
            'image_url': 'https://images.unsplash.com/photo-1559847844-d721426d6edc?w=300&h=200&fit=crop',
            'description': 'Authentic Thai street food and curries',
            'address': '753 Thai Town, New York, NY 10019',
            'phone': '(212) 555-0753',
            'hours': 'Mon-Sun: 11:00 AM - 10:00 PM'
        },
        {
            'name': "Mediterranean Breeze",
            'cuisine': 'mediterranean',
            'rating': 4.5,
            'price_level': '$$',
            'distance': '0.9 miles',
            'image_url': 'https://images.unsplash.com/photo-1544025162-d76694265947?w=300&h=200&fit=crop',
            'description': 'Fresh Mediterranean dishes with olive oil and herbs',
            'address': '852 Mediterranean Ave, New York, NY 10020',
            'phone': '(212) 555-0852',
            'hours': 'Mon-Sun: 12:00 PM - 9:00 PM'
        },
        {
            'name': "Seoul Kitchen",
            'cuisine': 'korean',
            'rating': 4.3,
            'price_level': '$$',
            'distance': '1.1 miles',
            'image_url': 'https://images.unsplash.com/photo-1498654896293-37aacf113fd9?w=300&h=200&fit=crop',
            'description': 'Korean BBQ and traditional dishes',
            'address': '741 Korea Way, New York, NY 10021',
            'phone': '(212) 555-0741',
            'hours': 'Mon-Sun: 5:00 PM - 11:00 PM'
        },
        {
            'name': "The Steakhouse",
            'cuisine': 'steakhouse',
            'rating': 4.9,
            'price_level': '$$$$',
            'distance': '0.5 miles',
            'image_url': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=300&h=200&fit=crop',
            'description': 'Premium steaks and fine dining experience',
            'address': '963 Steakhouse Row, New York, NY 10022',
            'phone': '(212) 555-0963',
            'hours': 'Mon-Sun: 5:30 PM - 11:00 PM'
        },
        {
            'name': "Pasta Paradise",
            'cuisine': 'italian',
            'rating': 4.4,
            'price_level': '$$',
            'distance': '0.7 miles',
            'image_url': 'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=300&h=200&fit=crop',
            'description': 'Homemade pasta and Italian comfort food',
            'address': '147 Pasta Lane, New York, NY 10023',
            'phone': '(212) 555-0147',
            'hours': 'Mon-Sun: 11:30 AM - 10:00 PM'
        },
        {
            'name': "Golden Wok",
            'cuisine': 'chinese',
            'rating': 4.0,
            'price_level': '$',
            'distance': '0.3 miles',
            'image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=300&h=200&fit=crop',
            'description': 'Quick Chinese takeout and delivery',
            'address': '258 Wok Street, New York, NY 10024',
            'phone': '(212) 555-0258',
            'hours': 'Mon-Sun: 11:00 AM - 10:30 PM'
        },
        {
            'name': "Aztec Grill",
            'cuisine': 'mexican',
            'rating': 4.6,
            'price_level': '$$',
            'distance': '0.4 miles',
            'image_url': 'https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=300&h=200&fit=crop',
            'description': 'Modern Mexican cuisine with craft cocktails',
            'address': '369 Aztec Plaza, New York, NY 10025',
            'phone': '(212) 555-0369',
            'hours': 'Mon-Sun: 4:00 PM - 12:00 AM'
        },
        {
            'name': "Bombay Express",
            'cuisine': 'indian',
            'rating': 4.2,
            'price_level': '$',
            'distance': '0.6 miles',
            'image_url': 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=300&h=200&fit=crop',
            'description': 'Fast Indian food with traditional flavors',
            'address': '456 Bombay Street, New York, NY 10026',
            'phone': '(212) 555-0456',
            'hours': 'Mon-Sun: 11:00 AM - 9:30 PM'
        },
        {
            'name': "Tokyo Nights",
            'cuisine': 'japanese',
            'rating': 4.5,
            'price_level': '$$',
            'distance': '0.8 miles',
            'image_url': 'https://images.unsplash.com/photo-1580822184713-fc5400e7fe10?w=300&h=200&fit=crop',
            'description': 'Ramen, sushi, and Japanese street food',
            'address': '789 Tokyo Avenue, New York, NY 10027',
            'phone': '(212) 555-0789',
            'hours': 'Mon-Sun: 12:00 PM - 11:00 PM'
        },
        {
            'name': "All-American Diner",
            'cuisine': 'american',
            'rating': 4.3,
            'price_level': '$',
            'distance': '0.2 miles',
            'image_url': 'https://images.unsplash.com/photo-1576107232684-1279f390859f?w=300&h=200&fit=crop',
            'description': 'Classic American diner food 24/7',
            'address': '123 Diner Drive, New York, NY 10028',
            'phone': '(212) 555-0123',
            'hours': 'Open 24 Hours'
        },
        {
            'name': "Café de Paris",
            'cuisine': 'french',
            'rating': 4.4,
            'price_level': '$$',
            'distance': '0.5 miles',
            'image_url': 'https://images.unsplash.com/photo-1551218808-94e220e084d2?w=300&h=200&fit=crop',
            'description': 'French bistro with outdoor seating',
            'address': '456 Paris Boulevard, New York, NY 10029',
            'phone': '(212) 555-0456',
            'hours': 'Mon-Sun: 7:00 AM - 10:00 PM'
        },
        {
            'name': "Spicy Elephant",
            'cuisine': 'thai',
            'rating': 4.7,
            'price_level': '$$',
            'distance': '0.6 miles',
            'image_url': 'https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=300&h=200&fit=crop',
            'description': 'Authentic Thai cuisine with adjustable spice levels',
            'address': '789 Elephant Lane, New York, NY 10030',
            'phone': '(212) 555-0789',
            'hours': 'Mon-Sun: 11:30 AM - 10:30 PM'
        },
        {
            'name': "Santorini Sunset",
            'cuisine': 'mediterranean',
            'rating': 4.8,
            'price_level': '$$$',
            'distance': '0.9 miles',
            'image_url': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=300&h=200&fit=crop',
            'description': 'Greek and Mediterranean specialties',
            'address': '321 Santorini Street, New York, NY 10031',
            'phone': '(212) 555-0321',
            'hours': 'Mon-Sun: 5:00 PM - 11:00 PM'
        },
        {
            'name': "K-Town BBQ",
            'cuisine': 'korean',
            'rating': 4.6,
            'price_level': '$$',
            'distance': '1.0 miles',
            'image_url': 'https://images.unsplash.com/photo-1551218808-94e220e084d2?w=300&h=200&fit=crop',
            'description': 'All-you-can-eat Korean BBQ experience',
            'address': '654 K-Town Plaza, New York, NY 10032',
            'phone': '(212) 555-0654',
            'hours': 'Mon-Sun: 5:00 PM - 12:00 AM'
        },
        {
            'name': "Prime Cut",
            'cuisine': 'steakhouse',
            'rating': 4.7,
            'price_level': '$$$$',
            'distance': '0.8 miles',
            'image_url': 'https://images.unsplash.com/photo-1558030006-450675393462?w=300&h=200&fit=crop',
            'description': 'Aged steaks and wine selection',
            'address': '987 Prime Avenue, New York, NY 10033',
            'phone': '(212) 555-0987',
            'hours': 'Mon-Sun: 6:00 PM - 11:00 PM'
        },
        {
            'name': "Nonna's Kitchen",
            'cuisine': 'italian',
            'rating': 4.9,
            'price_level': '$$$',
            'distance': '0.4 miles',
            'image_url': 'https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=300&h=200&fit=crop',
            'description': 'Family recipes passed down through generations',
            'address': '159 Nonna Lane, New York, NY 10034',
            'phone': '(212) 555-0159',
            'hours': 'Tue-Sun: 5:00 PM - 10:00 PM'
        },
        {
            'name': "Dim Sum Palace",
            'cuisine': 'chinese',
            'rating': 4.5,
            'price_level': '$$',
            'distance': '0.7 miles',
            'image_url': 'https://images.unsplash.com/photo-1563379091339-03246963d7d3?w=300&h=200&fit=crop',
            'description': 'Traditional dim sum and Cantonese cuisine',
            'address': '753 Dim Sum Drive, New York, NY 10035',
            'phone': '(212) 555-0753',
            'hours': 'Mon-Sun: 10:00 AM - 9:00 PM'
        },
        {
            'name': "Casa Miguel",
            'cuisine': 'mexican',
            'rating': 4.4,
            'price_level': '$$',
            'distance': '0.5 miles',
            'image_url': 'https://images.unsplash.com/photo-1553909489-cd47e0ef937f?w=300&h=200&fit=crop',
            'description': 'Traditional Mexican home cooking',
            'address': '852 Casa Street, New York, NY 10036',
            'phone': '(212) 555-0852',
            'hours': 'Mon-Sun: 11:00 AM - 10:00 PM'
        }
    ]
    
    # Dish data for popular items
    dishes_data = {
        'italian': [
            {'name': 'Margherita Pizza', 'price': '$18', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=200&h=150&fit=crop'},
            {'name': 'Fettuccine Alfredo', 'price': '$16', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=200&h=150&fit=crop'},
            {'name': 'Tiramisu', 'price': '$8', 'category': 'dessert', 'image_url': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=200&h=150&fit=crop'}
        ],
        'chinese': [
            {'name': 'Sweet & Sour Pork', 'price': '$14', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1559847844-d721426d6edc?w=200&h=150&fit=crop'},
            {'name': 'Kung Pao Chicken', 'price': '$13', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=200&h=150&fit=crop'},
            {'name': 'Fried Rice', 'price': '$10', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=200&h=150&fit=crop'}
        ],
        'mexican': [
            {'name': 'Beef Tacos', 'price': '$12', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=200&h=150&fit=crop'},
            {'name': 'Chicken Burrito', 'price': '$11', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=200&h=150&fit=crop'},
            {'name': 'Guacamole & Chips', 'price': '$7', 'category': 'appetizer', 'image_url': 'https://images.unsplash.com/photo-1553909489-cd47e0ef937f?w=200&h=150&fit=crop'}
        ],
        'indian': [
            {'name': 'Butter Chicken', 'price': '$15', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=200&h=150&fit=crop'},
            {'name': 'Biryani', 'price': '$14', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1563379091339-03246963d7d3?w=200&h=150&fit=crop'},
            {'name': 'Naan Bread', 'price': '$4', 'category': 'side', 'image_url': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=200&h=150&fit=crop'}
        ],
        'japanese': [
            {'name': 'Salmon Roll', 'price': '$12', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=200&h=150&fit=crop'},
            {'name': 'Chicken Teriyaki', 'price': '$16', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1580822184713-fc5400e7fe10?w=200&h=150&fit=crop'},
            {'name': 'Miso Soup', 'price': '$5', 'category': 'appetizer', 'image_url': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=200&h=150&fit=crop'}
        ],
        'american': [
            {'name': 'Classic Cheeseburger', 'price': '$9', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=200&h=150&fit=crop'},
            {'name': 'Loaded Fries', 'price': '$6', 'category': 'side', 'image_url': 'https://images.unsplash.com/photo-1576107232684-1279f390859f?w=200&h=150&fit=crop'},
            {'name': 'Milkshake', 'price': '$5', 'category': 'dessert', 'image_url': 'https://images.unsplash.com/photo-1541658016709-82535e94bc69?w=200&h=150&fit=crop'}
        ]
    }
    
    # Generic dishes for other cuisines
    generic_dishes = [
        {'name': 'House Special', 'price': '$15', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=200&h=150&fit=crop'},
        {'name': 'Chef\'s Choice', 'price': '$18', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=200&h=150&fit=crop'},
        {'name': 'Daily Special', 'price': '$12', 'category': 'main', 'image_url': 'https://images.unsplash.com/photo-1551218808-94e220e084d2?w=200&h=150&fit=crop'}
    ]
    
    # Create restaurants
    for rest_data in restaurants_data:
        restaurant = Restaurant(**rest_data)
        db.session.add(restaurant)
        db.session.flush()  # To get the ID
        
        # Add dishes
        cuisine_dishes = dishes_data.get(rest_data['cuisine'], generic_dishes)
        for i, dish_data in enumerate(cuisine_dishes):
            dish = Dish(
                restaurant_id=restaurant.id,
                name=dish_data['name'],
                price=dish_data['price'],
                category=dish_data['category'],
                image_url=dish_data['image_url'],
                is_popular=i < 2,  # First 2 dishes are popular
                description=f"Delicious {dish_data['name'].lower()} prepared with fresh ingredients"
            )
            db.session.add(dish)
        
        # Add availability slots
        time_slots = ['5:00 PM', '5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM', '8:00 PM', '8:30 PM']
        for time_slot in time_slots:
            # Random availability (70% chance of being available)
            is_available = random.random() > 0.3
            availability = AvailabilitySlot(
                restaurant_id=restaurant.id,
                time_slot=time_slot,
                is_available=is_available,
                date=date.today()
            )
            db.session.add(availability)
    
    db.session.commit()
    print("Database populated with 25 restaurants and their data!")