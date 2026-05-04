#!/usr/bin/env python3
"""
Quick Start Guide - Hostel Information Chatbot
Run this file to see a quick demonstration of the chatbot
"""

from hostel_chatbot import HostelChatbot

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def demo_chat():
    """Run a quick demonstration of the chatbot"""
    
    print_section("🏨 CAMPUS HOSTEL CHATBOT - QUICK DEMO")
    
    chatbot = HostelChatbot()
    
    # Demo queries
    demo_queries = [
        ("Hello!", "greeting"),
        ("What are your facilities?", "facilities"),
        ("How much does a room cost?", "pricing"),
        ("How do I book?", "booking"),
        ("What are the rules?", "rules"),
        ("What's the checkout time?", "checkout"),
        ("How can I contact you?", "contact"),
        ("What amenities do you have?", "amenities"),
    ]
    
    for i, (query, intent) in enumerate(demo_queries, 1):
        print(f"\n[Query {i}] You: {query}")
        print(f"Intent Detected: {intent}")
        response = chatbot.respond(query)
        print(f"\n🤖 Assistant:\n{response}")
        print("-" * 60)
    
    print_section("DEMO COMPLETE")
    
    print("\n✅ Features demonstrated:")
    print("  ✓ Intent detection")
    print("  ✓ Pricing information")
    print("  ✓ Facilities overview")
    print("  ✓ Booking procedures")
    print("  ✓ Rules & regulations")
    print("  ✓ Contact information")
    print("  ✓ Amenities listing")
    print("  ✓ Checkout procedures")
    
    print("\n\n📱 How to use the chatbot:\n")
    print("1. COMMAND-LINE INTERFACE:")
    print("   python hostel_chatbot.py")
    print("\n2. WEB INTERFACE:")
    print("   python web_chatbot.py")
    print("   Then open: http://localhost:5000")
    print("\n3. RUN TESTS:")
    print("   python test_chatbot.py")
    
    print("\n\n💡 Try asking:")
    print("  - 'What's the price of a private room?'")
    print("  - 'Do you have WiFi and parking?'")
    print("  - 'What time is check-in?'")
    print("  - 'What are the quiet hours?'")
    print("  - 'How do I make a reservation?'")
    
    print("\n" + "="*60)
    print("  For more information, see README.md")
    print("="*60 + "\n")

if __name__ == "__main__":
    demo_chat()
