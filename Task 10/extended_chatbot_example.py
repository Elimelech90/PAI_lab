"""
Example: Extending the Hostel Chatbot
This file shows how to customize and extend the chatbot with additional features
"""

from hostel_chatbot import HostelChatbot

class ExtendedHostelChatbot(HostelChatbot):
    """Extended chatbot with additional features"""
    
    def __init__(self):
        super().__init__()
        
        # Add new intents
        self.intents.update({
            "reviews": self._handle_reviews,
            "nearby": self._handle_nearby,
            "special_offers": self._handle_special_offers,
            "faq": self._handle_faq,
            "emergency": self._handle_emergency,
            "feedback": self._handle_feedback
        })
        
        # Add extended hostel information
        self.hostel_info.update({
            "reviews": {
                "rating": 4.8,
                "total_reviews": 500,
                "highlights": [
                    "Clean and comfortable rooms",
                    "Friendly and helpful staff",
                    "Great location",
                    "Value for money"
                ]
            },
            "nearby_attractions": {
                "shopping": "Shopping Mall (1km)",
                "transport": "Railway Station (2km)",
                "medical": "Hospital (800m)",
                "recreation": "Parks & Gardens (1km)"
            },
            "special_offers": {
                "weekly": "10% off for 7+ nights",
                "monthly": "20% off for 30+ nights",
                "group": "15% off for groups of 4+"
            },
            "faq": {
                "deposit": "₹500 refundable security deposit",
                "electricity": "Included in room price",
                "internet": "Included in room price",
                "luggage": "Free storage available"
            }
        })
    
    def _detect_intent(self, user_input):
        """Enhanced intent detection"""
        user_input_lower = user_input.lower()
        
        # Call parent's detect_intent first
        intent = super()._detect_intent(user_input)
        
        if intent:
            return intent
        
        # Additional intent keywords
        reviews_keywords = ["review", "rating", "feedback", "experience", "opinion"]
        nearby_keywords = ["nearby", "attraction", "location", "nearby places", "around"]
        offers_keywords = ["discount", "offer", "promotion", "deal", "special"]
        faq_keywords = ["faq", "frequently asked", "common question"]
        emergency_keywords = ["emergency", "urgent", "help", "sos"]
        feedback_keywords = ["suggest", "suggestion", "improve", "complaint"]
        
        for keyword in reviews_keywords:
            if keyword in user_input_lower:
                return "reviews"
        
        for keyword in nearby_keywords:
            if keyword in user_input_lower:
                return "nearby"
        
        for keyword in offers_keywords:
            if keyword in user_input_lower:
                return "special_offers"
        
        for keyword in faq_keywords:
            if keyword in user_input_lower:
                return "faq"
        
        for keyword in emergency_keywords:
            if keyword in user_input_lower:
                return "emergency"
        
        for keyword in feedback_keywords:
            if keyword in user_input_lower:
                return "feedback"
        
        return None
    
    def _handle_reviews(self, user_input):
        """Handle review inquiries"""
        reviews = self.hostel_info["reviews"]
        response = f"""⭐ **Guest Reviews & Ratings**

**Overall Rating:** {reviews['rating']}/5 ({reviews['total_reviews']} reviews)

**What Guests Love:**
"""
        for i, highlight in enumerate(reviews['highlights'], 1):
            response += f"{i}. {highlight}\n"
        
        response += "\n**Would you like to share your feedback?**"
        return response
    
    def _handle_nearby(self, user_input):
        """Handle nearby attractions inquiries"""
        nearby = self.hostel_info["nearby_attractions"]
        response = "📍 **Nearby Attractions & Services**\n\n"
        for category, location in nearby.items():
            response += f"• **{category.title()}:** {location}\n"
        response += "\nGreat location for exploring the city!"
        return response
    
    def _handle_special_offers(self, user_input):
        """Handle special offers inquiries"""
        offers = self.hostel_info["special_offers"]
        response = "🎉 **Special Offers & Discounts**\n\n"
        response += f"• **Weekly Rate:** {offers['weekly']}\n"
        response += f"• **Monthly Rate:** {offers['monthly']}\n"
        response += f"• **Group Rate:** {offers['group']}\n\n"
        response += "Contact us for more information:\n"
        response += f"📞 {self.hostel_info['contact']['phone']}\n"
        response += f"📧 {self.hostel_info['contact']['email']}"
        return response
    
    def _handle_faq(self, user_input):
        """Handle FAQ inquiries"""
        faq = self.hostel_info["faq"]
        response = "❓ **Frequently Asked Questions**\n\n"
        for question, answer in faq.items():
            response += f"**{question.replace('_', ' ').title()}:**\n"
            response += f"{answer}\n\n"
        return response
    
    def _handle_emergency(self, user_input):
        """Handle emergency inquiries"""
        response = """🚨 **EMERGENCY ASSISTANCE**

**For emergencies, please:**
1. Call 911 (or local emergency number)
2. Contact our front desk immediately

**Our Contact:**
📞 Emergency Line: +1-800-HOSTEL-1
📞 24/7 Front Desk Support

**In-Hostel Support:**
- First-aid kit available at reception
- Doctor on call 24/7
- Security team always available

**We're here to help!**"""
        return response
    
    def _handle_feedback(self, user_input):
        """Handle feedback inquiries"""
        response = """💬 **Send Us Your Feedback**

We'd love to hear from you! Your feedback helps us improve.

**How to give feedback:**
1. Visit: www.campushostel.com/feedback
2. Email: feedback@campushostel.com
3. Call: +1-800-HOSTEL-1
4. Speak with staff at the front desk

**What we'd like to know:**
• Your overall experience
• Facility and cleanliness
• Staff service quality
• Suggestions for improvement

**Thank you for helping us serve you better!**"""
        return response


def demo_extended_features():
    """Demonstrate extended chatbot features"""
    
    print("\n" + "="*60)
    print("  EXTENDED HOSTEL CHATBOT FEATURES DEMO")
    print("="*60)
    
    chatbot = ExtendedHostelChatbot()
    
    # Demo queries for extended features
    demo_queries = [
        "What do guests say about you?",
        "What's nearby?",
        "Do you have any special offers?",
        "I have some common questions",
        "This is an emergency!",
        "I'd like to give feedback"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n[Query {i}] You: {query}")
        response = chatbot.respond(query)
        print(f"\n🤖 Assistant:\n{response}")
        print("-" * 60)
    
    print("\n" + "="*60)
    print("  EXTENDED FEATURES DEMO COMPLETE")
    print("="*60)
    print("\n✅ New features demonstrated:")
    print("  ✓ Guest reviews and ratings")
    print("  ✓ Nearby attractions")
    print("  ✓ Special offers and discounts")
    print("  ✓ FAQ section")
    print("  ✓ Emergency assistance")
    print("  ✓ Feedback collection")


def demo_customization():
    """Show how to customize the chatbot"""
    
    print("\n" + "="*60)
    print("  CUSTOMIZATION EXAMPLES")
    print("="*60)
    
    print("\n1. CREATE CUSTOM INTENT:")
    print("""
    # Add new intent keywords
    weather_keywords = ["weather", "forecast", "rain"]
    
    # Create handler method
    def _handle_weather(self, user_input):
        return "Check local weather forecast for current conditions."
    
    # Register intent
    self.intents["weather"] = self._handle_weather
    """)
    
    print("\n2. ADD CUSTOM INFORMATION:")
    print("""
    # Update hostel info dictionary
    self.hostel_info.update({
        "custom_field": "custom_value",
        "nested_info": {
            "detail1": "value1",
            "detail2": "value2"
        }
    })
    """)
    
    print("\n3. EXTEND RESPONSE HANDLING:")
    print("""
    # Override existing handler
    def _handle_pricing(self, user_input):
        response = super()._handle_pricing(user_input)
        # Add custom logic
        response += "\\n\\nBook now and get 20% off!"
        return response
    """)
    
    print("\n4. ADD MULTI-LANGUAGE SUPPORT:")
    print("""
    # Detect language
    def detect_language(self, user_input):
        # Use language detection library
        return language
    
    # Translate response
    def translate_response(self, text, target_language):
        # Use translation API
        return translated_text
    """)
    
    print("\n" + "="*60)


if __name__ == "__main__":
    # Run demonstrations
    demo_extended_features()
    print("\n")
    demo_customization()
    
    print("\n📝 To use the extended chatbot:")
    print("1. Import: from extended_chatbot import ExtendedHostelChatbot")
    print("2. Create: chatbot = ExtendedHostelChatbot()")
    print("3. Use: response = chatbot.respond(user_input)")
    print("\n")
