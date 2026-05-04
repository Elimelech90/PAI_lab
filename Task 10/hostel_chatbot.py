"""
Hostel Information Chatbot
A comprehensive chatbot system for answering hostel-related queries
"""

import re
from datetime import datetime
from collections import defaultdict

class HostelChatbot:
    def __init__(self):
        # Hostel Information Database
        self.hostel_info = {
            "name": "Campus Hostel",
            "location": "123 University Road, City Center",
            "contact": {
                "phone": "+1-800-HOSTEL-1",
                "email": "info@campushostel.com",
                "hours": "8:00 AM - 10:00 PM"
            },
            "facilities": {
                "wifi": True,
                "ac": True,
                "hot_water": True,
                "parking": True,
                "laundry": True,
                "gym": True,
                "dining": True,
                "security": True,
                "power_backup": True
            },
            "room_types": {
                "dormitory": {
                    "price": 500,
                    "beds": 8,
                    "shared_bathroom": True,
                    "ac": True
                },
                "semi_private": {
                    "price": 800,
                    "beds": 4,
                    "shared_bathroom": True,
                    "ac": True
                },
                "private": {
                    "price": 1200,
                    "beds": 2,
                    "attached_bathroom": True,
                    "ac": True
                }
            },
            "timings": {
                "check_in": "2:00 PM",
                "check_out": "11:00 AM",
                "quiet_hours": "10:00 PM - 7:00 AM"
            },
            "rules": [
                "No smoking in rooms",
                "No alcohol in premises",
                "Respect quiet hours",
                "Keep rooms clean",
                "No parties or gatherings after 10 PM",
                "Guests must have valid ID",
                "No pets allowed"
            ],
            "amenities": {
                "breakfast": "Complimentary daily breakfast",
                "common_area": "Large common room with TV",
                "kitchen": "Self-catering kitchen available",
                "study_room": "Dedicated study area",
                "recreation": "Board games and books available"
            }
        }
        
        # Intent patterns and responses
        self.intents = {
            "greeting": self._handle_greeting,
            "pricing": self._handle_pricing,
            "facilities": self._handle_facilities,
            "booking": self._handle_booking,
            "rules": self._handle_rules,
            "contact": self._handle_contact,
            "checkout": self._handle_checkout,
            "amenities": self._handle_amenities,
            "help": self._handle_help
        }
        
        # Conversation history
        self.conversation_history = []
    
    def _detect_intent(self, user_input):
        """Detect user intent from input"""
        user_input_lower = user_input.lower()
        
        greeting_keywords = ["hello", "hi", "hey", "greetings", "welcome"]
        pricing_keywords = ["price", "cost", "rate", "how much", "fee", "payment"]
        facilities_keywords = ["facility", "facilities", "amenities", "what do you have", "available"]
        booking_keywords = ["book", "reservation", "reserve", "check-in", "checkin", "available rooms"]
        rules_keywords = ["rules", "policy", "policies", "regulations", "guidelines", "allowed", "not allowed"]
        contact_keywords = ["contact", "phone", "email", "address", "location", "hours", "open"]
        checkout_keywords = ["checkout", "check out", "checkout time", "leave", "departure"]
        amenities_keywords = ["breakfast", "kitchen", "study", "recreation", "common area", "amenities"]
        help_keywords = ["help", "assist", "support", "how can", "what can", "options", "menu"]
        
        for keyword in greeting_keywords:
            if keyword in user_input_lower:
                return "greeting"
        
        for keyword in pricing_keywords:
            if keyword in user_input_lower:
                return "pricing"
        
        for keyword in facilities_keywords:
            if keyword in user_input_lower:
                return "facilities"
        
        for keyword in booking_keywords:
            if keyword in user_input_lower:
                return "booking"
        
        for keyword in rules_keywords:
            if keyword in user_input_lower:
                return "rules"
        
        for keyword in contact_keywords:
            if keyword in user_input_lower:
                return "contact"
        
        for keyword in checkout_keywords:
            if keyword in user_input_lower:
                return "checkout"
        
        for keyword in amenities_keywords:
            if keyword in user_input_lower:
                return "amenities"
        
        for keyword in help_keywords:
            if keyword in user_input_lower:
                return "help"
        
        return None
    
    def _handle_greeting(self, user_input):
        """Handle greeting"""
        responses = [
            "Hello! Welcome to Campus Hostel. How can I help you today?",
            "Hi there! Thanks for reaching out. What information do you need?",
            "Greetings! I'm here to help with any questions about our hostel.",
            "Hello! Happy to assist. What would you like to know?"
        ]
        return responses[len(self.conversation_history) % len(responses)]
    
    def _handle_pricing(self, user_input):
        """Handle pricing inquiries"""
        response = "🏠 **Room Pricing**\n\n"
        for room_type, details in self.hostel_info["room_types"].items():
            response += f"**{room_type.replace('_', ' ').title()}**\n"
            response += f"  • Price: ₹{details['price']}/night\n"
            response += f"  • Beds: {details['beds']}\n"
            response += f"  • Bathroom: {'Attached' if details.get('attached_bathroom') else 'Shared'}\n"
            response += f"  • AC: {'Yes' if details['ac'] else 'No'}\n\n"
        response += "Would you like to book a room? Contact us for special discounts!"
        return response
    
    def _handle_facilities(self, user_input):
        """Handle facilities inquiries"""
        response = "✨ **Our Facilities**\n\n"
        facilities = self.hostel_info["facilities"]
        for facility, available in facilities.items():
            status = "✓ Available" if available else "✗ Not Available"
            response += f"• {facility.replace('_', ' ').title()}: {status}\n"
        return response
    
    def _handle_booking(self, user_input):
        """Handle booking inquiries"""
        response = """📅 **Booking Information**

**Check-in:** """ + self.hostel_info["timings"]["check_in"] + """
**Check-out:** """ + self.hostel_info["timings"]["check_out"] + """

To book a room:
1. Choose your room type (Dormitory, Semi-Private, or Private)
2. Select your dates
3. Contact us for confirmation

**Contact Details:**
📞 Phone: """ + self.hostel_info["contact"]["phone"] + """
📧 Email: """ + self.hostel_info["contact"]["email"] + """

Available rooms are shown on our website. Early booking is recommended!"""
        return response
    
    def _handle_rules(self, user_input):
        """Handle rules inquiries"""
        response = "📋 **Hostel Rules & Regulations**\n\n"
        for i, rule in enumerate(self.hostel_info["rules"], 1):
            response += f"{i}. {rule}\n"
        response += f"\n**Quiet Hours:** {self.hostel_info['timings']['quiet_hours']}\n"
        response += "We appreciate your cooperation in maintaining a pleasant environment for all guests!"
        return response
    
    def _handle_contact(self, user_input):
        """Handle contact inquiries"""
        contact = self.hostel_info["contact"]
        response = f"""📞 **Contact Us**

**Hostel Name:** {self.hostel_info['name']}
**Location:** {self.hostel_info['location']}

**Phone:** {contact['phone']}
**Email:** {contact['email']}
**Hours:** {contact['hours']}

We're available 7 days a week. Feel free to reach out with any questions!"""
        return response
    
    def _handle_checkout(self, user_input):
        """Handle checkout inquiries"""
        response = f"""🔑 **Checkout Information**

**Standard Checkout Time:** {self.hostel_info['timings']['check_out']}

Late checkout is available at the following rates:
• Till 2:00 PM: +₹300
• Till 5:00 PM: +₹500
• Full day: ₹800

Please inform the reception 24 hours in advance if you need late checkout.
Contact: {self.hostel_info['contact']['phone']}"""
        return response
    
    def _handle_amenities(self, user_input):
        """Handle amenities inquiries"""
        response = "🎯 **Amenities & Services**\n\n"
        for amenity, description in self.hostel_info["amenities"].items():
            response += f"• **{amenity.replace('_', ' ').title()}:** {description}\n"
        return response
    
    def _handle_help(self, user_input):
        """Handle help/options"""
        response = """ℹ️ **How Can I Help You?**

I can provide information about:
1. **Pricing** - Room rates and types
2. **Facilities** - What amenities we offer
3. **Booking** - How to reserve a room
4. **Rules** - Hostel policies
5. **Contact** - Phone, email, address
6. **Checkout** - Late checkout options
7. **Amenities** - Services available

Just ask me anything about Campus Hostel!"""
        return response
    
    def respond(self, user_input):
        """Generate response to user input"""
        # Store in conversation history
        self.conversation_history.append({
            "user": user_input,
            "timestamp": datetime.now()
        })
        
        # Detect intent
        intent = self._detect_intent(user_input)
        
        if intent and intent in self.intents:
            response = self.intents[intent](user_input)
        else:
            # Default response for unrecognized input
            response = f"""I'm not sure I understood that correctly. Let me help you find what you're looking for!

You can ask me about:
• Room pricing and availability
• Facilities and amenities
• Booking information
• Hostel rules
• Contact details
• Checkout procedures

What would you like to know?"""
        
        self.conversation_history.append({
            "bot": response,
            "timestamp": datetime.now()
        })
        
        return response
    
    def get_conversation_history(self):
        """Return conversation history"""
        return self.conversation_history
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []


class ChatbotUI:
    """Simple command-line interface for the chatbot"""
    
    def __init__(self):
        self.chatbot = HostelChatbot()
        self.running = True
    
    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*60)
        print("    CAMPUS HOSTEL - INFORMATION CHATBOT")
        print("="*60)
        print("\n👋 Welcome! I'm your hostel information assistant.")
        print("Type 'help' to see what I can assist with.")
        print("Type 'exit' or 'quit' to end the conversation.\n")
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "-"*60)
        print("Options:")
        print("1. Ask a question")
        print("2. View conversation history")
        print("3. Reset conversation")
        print("4. Exit")
        print("-"*60)
    
    def run(self):
        """Run the chatbot interface"""
        self.display_welcome()
        
        while self.running:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print("\n👋 Thank you for using Campus Hostel Chatbot!")
                    print("Have a great stay! 🏡\n")
                    break
                
                # Check for history command
                if user_input.lower() == 'history':
                    self._display_history()
                    continue
                
                # Check for reset command
                if user_input.lower() == 'reset':
                    self.chatbot.reset_conversation()
                    print("✓ Conversation history cleared.\n")
                    continue
                
                # Get and display response
                response = self.chatbot.respond(user_input)
                print(f"\n🤖 Assistant: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")
    
    def _display_history(self):
        """Display conversation history"""
        history = self.chatbot.get_conversation_history()
        if not history:
            print("\n📝 No conversation history yet.\n")
            return
        
        print("\n" + "="*60)
        print("CONVERSATION HISTORY")
        print("="*60)
        
        for entry in history:
            if "user" in entry:
                print(f"\nYou: {entry['user']}")
            elif "bot" in entry:
                print(f"\nAssistant: {entry['bot']}")
        
        print("\n" + "="*60 + "\n")


def main():
    """Main entry point"""
    ui = ChatbotUI()
    ui.run()


if __name__ == "__main__":
    main()
