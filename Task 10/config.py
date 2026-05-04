"""
Configuration File for Hostel Information Chatbot
Customize this file to match your hostel's information
"""

HOSTEL_CONFIG = {
    # Basic Information
    "name": "Campus Hostel",
    "description": "Your premier student hostel",
    "location": "123 University Road, City Center",
    
    # Contact Information
    "contact": {
        "phone": "+1-800-HOSTEL-1",
        "email": "info@campushostel.com",
        "hours": "8:00 AM - 10:00 PM",
        "website": "www.campushostel.com"
    },
    
    # Room Information
    "room_types": {
        "dormitory": {
            "name": "Dormitory",
            "price": 500,
            "beds": 8,
            "shared_bathroom": True,
            "ac": True,
            "features": [
                "Spacious room",
                "Shared bathroom",
                "WiFi included",
                "AC & Fan",
                "Lockers for valuables"
            ]
        },
        "semi_private": {
            "name": "Semi-Private",
            "price": 800,
            "beds": 4,
            "shared_bathroom": True,
            "ac": True,
            "features": [
                "Smaller group",
                "More privacy",
                "Shared bathroom",
                "WiFi included",
                "AC & Fan"
            ]
        },
        "private": {
            "name": "Private",
            "price": 1200,
            "beds": 2,
            "attached_bathroom": True,
            "ac": True,
            "features": [
                "Private room",
                "Attached bathroom",
                "WiFi included",
                "AC",
                "Premium amenities"
            ]
        }
    },
    
    # Timing Information
    "timings": {
        "check_in": "2:00 PM",
        "check_out": "11:00 AM",
        "quiet_hours_start": "10:00 PM",
        "quiet_hours_end": "7:00 AM"
    },
    
    # Facilities
    "facilities": {
        "wifi": {
            "available": True,
            "speed": "High-speed (50 Mbps)"
        },
        "ac": {
            "available": True,
            "type": "Central cooling"
        },
        "hot_water": {
            "available": True,
            "timing": "24/7"
        },
        "parking": {
            "available": True,
            "cost": "Free"
        },
        "laundry": {
            "available": True,
            "cost": "Complimentary"
        },
        "gym": {
            "available": True,
            "cost": "Included"
        },
        "dining": {
            "available": True,
            "type": "In-house cafeteria"
        },
        "security": {
            "available": True,
            "type": "24/7 CCTV & Security Staff"
        },
        "power_backup": {
            "available": True,
            "type": "Diesel generator"
        }
    },
    
    # Amenities
    "amenities": {
        "breakfast": "Complimentary daily breakfast (7-9 AM)",
        "common_area": "Large common room with TV & streaming",
        "kitchen": "Fully equipped self-catering kitchen",
        "study_room": "Dedicated quiet study area",
        "recreation": "Board games, books, and entertainment",
        "medical": "First-aid kit and doctor on call",
        "luggage": "Luggage storage facility"
    },
    
    # Rules & Regulations
    "rules": [
        "No smoking in rooms or common areas",
        "No alcohol or drugs in premises",
        "Respect quiet hours (10:00 PM - 7:00 AM)",
        "Keep rooms clean and tidy",
        "No parties or gatherings after 10 PM",
        "Guests must have valid ID",
        "No pets allowed",
        "Report any damage immediately",
        "Use facilities responsibly",
        "Respect other guests' privacy"
    ],
    
    # Pricing for Extensions
    "extensions": {
        "late_checkout_2pm": 300,
        "late_checkout_5pm": 500,
        "full_day_extension": 800
    },
    
    # Additional Information
    "about": {
        "established": "2020",
        "capacity": "150 guests",
        "average_rating": "4.8/5",
        "reviews": "500+ verified reviews"
    },
    
    # Booking Information
    "booking": {
        "minimum_stay": 1,
        "maximum_stay": 90,
        "cancellation_policy": "Free cancellation up to 24 hours before check-in",
        "payment_methods": ["Cash", "Card", "UPI", "Bank Transfer"]
    },
    
    # Special Offers
    "offers": {
        "weekly_discount": "10% off for 7+ nights",
        "monthly_discount": "20% off for 30+ nights",
        "group_discount": "15% off for groups of 4+"
    },
    
    # Nearby Attractions
    "nearby": [
        "University Campus (500m)",
        "Shopping Mall (1km)",
        "Railway Station (2km)",
        "Bus Terminal (1.5km)",
        "Hospital (800m)",
        "Parks & Gardens (1km)"
    ],
    
    # FAQ
    "faq": {
        "deposit": "₹500 refundable security deposit",
        "electricity": "Included in room price",
        "internet": "Included in room price",
        "luggage": "Free storage before check-in and after check-out",
        "visitors": "Allowed until 8 PM in common areas",
        "cooking": "Only in designated kitchen area"
    }
}

# Chatbot Settings
CHATBOT_SETTINGS = {
    "debug_mode": False,
    "show_intent": False,
    "max_conversation_history": 100,
    "response_time_limit": 5  # seconds
}

# Web Interface Settings
WEB_SETTINGS = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": True,
    "theme": "modern",  # modern, classic, dark
    "max_message_length": 1000
}
