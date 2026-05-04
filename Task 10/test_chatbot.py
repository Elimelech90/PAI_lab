"""
Unit tests for Hostel Information Chatbot
"""

import unittest
from hostel_chatbot import HostelChatbot

class TestHostelChatbot(unittest.TestCase):
    """Test cases for the HostelChatbot"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.chatbot = HostelChatbot()
    
    def test_greeting_detection(self):
        """Test greeting intent detection"""
        response = self.chatbot.respond("Hello")
        self.assertIn("Welcome", response)
    
    def test_pricing_response(self):
        """Test pricing inquiry"""
        response = self.chatbot.respond("What is the price?")
        self.assertIn("Room Pricing", response)
        self.assertIn("Dormitory", response)
    
    def test_facilities_response(self):
        """Test facilities inquiry"""
        response = self.chatbot.respond("What facilities do you have?")
        self.assertIn("Facilities", response)
        self.assertIn("WiFi", response)
    
    def test_booking_response(self):
        """Test booking inquiry"""
        response = self.chatbot.respond("How do I book?")
        self.assertIn("Booking", response)
        self.assertIn("Check-in", response)
    
    def test_rules_response(self):
        """Test rules inquiry"""
        response = self.chatbot.respond("What are the rules?")
        self.assertIn("Rules", response)
        self.assertIn("No smoking", response)
    
    def test_contact_response(self):
        """Test contact inquiry"""
        response = self.chatbot.respond("How can I contact you?")
        self.assertIn("Contact", response)
        self.assertIn("Phone", response)
        self.assertIn("Email", response)
    
    def test_checkout_response(self):
        """Test checkout inquiry"""
        response = self.chatbot.respond("What is checkout time?")
        self.assertIn("Checkout", response)
        self.assertIn("11:00 AM", response)
    
    def test_amenities_response(self):
        """Test amenities inquiry"""
        response = self.chatbot.respond("What amenities do you have?")
        self.assertIn("Amenities", response)
    
    def test_help_response(self):
        """Test help inquiry"""
        response = self.chatbot.respond("help")
        self.assertIn("How Can I Help", response)
    
    def test_unknown_intent(self):
        """Test handling of unknown intent"""
        response = self.chatbot.respond("xyzabc random text")
        self.assertIn("not sure", response)
    
    def test_conversation_history(self):
        """Test conversation history tracking"""
        self.chatbot.respond("Hello")
        self.chatbot.respond("What is the price?")
        history = self.chatbot.get_conversation_history()
        self.assertEqual(len(history), 4)  # 2 user + 2 bot messages
    
    def test_reset_conversation(self):
        """Test conversation reset"""
        self.chatbot.respond("Hello")
        self.chatbot.reset_conversation()
        history = self.chatbot.get_conversation_history()
        self.assertEqual(len(history), 0)
    
    def test_case_insensitivity(self):
        """Test case-insensitive intent detection"""
        response1 = self.chatbot.respond("HELLO")
        response2 = self.chatbot.respond("hello")
        response3 = self.chatbot.respond("Hello")
        # All should detect greeting intent
        self.assertIn("Welcome", response1)
        self.assertIn("Welcome", response2)
        self.assertIn("Welcome", response3)
    
    def test_multiple_keywords_in_message(self):
        """Test handling of messages with multiple keywords"""
        response = self.chatbot.respond("Hi, what is the pricing for facilities?")
        # Should handle multiple intents appropriately
        self.assertTrue(len(response) > 0)
    
    def test_hostel_info_availability(self):
        """Test that hostel information is accessible"""
        info = self.chatbot.hostel_info
        self.assertIn("name", info)
        self.assertIn("contact", info)
        self.assertIn("facilities", info)
        self.assertIn("room_types", info)
    
    def test_room_types_exist(self):
        """Test that all room types are defined"""
        room_types = self.chatbot.hostel_info["room_types"]
        self.assertIn("dormitory", room_types)
        self.assertIn("semi_private", room_types)
        self.assertIn("private", room_types)
    
    def test_room_type_details(self):
        """Test that room types have required details"""
        for room_type, details in self.chatbot.hostel_info["room_types"].items():
            self.assertIn("price", details)
            self.assertIn("beds", details)
            self.assertIn("ac", details)

class TestIntentDetection(unittest.TestCase):
    """Test cases for intent detection"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.chatbot = HostelChatbot()
    
    def test_detect_greeting(self):
        """Test greeting detection"""
        intent = self.chatbot._detect_intent("hello")
        self.assertEqual(intent, "greeting")
    
    def test_detect_pricing(self):
        """Test pricing detection"""
        intent = self.chatbot._detect_intent("how much does it cost?")
        self.assertEqual(intent, "pricing")
    
    def test_detect_facilities(self):
        """Test facilities detection"""
        intent = self.chatbot._detect_intent("what amenities do you have?")
        self.assertEqual(intent, "facilities")
    
    def test_detect_booking(self):
        """Test booking detection"""
        intent = self.chatbot._detect_intent("I want to book a room")
        self.assertEqual(intent, "booking")
    
    def test_detect_none(self):
        """Test unknown intent detection"""
        intent = self.chatbot._detect_intent("random gibberish xyz")
        self.assertIsNone(intent)

class TestResponseQuality(unittest.TestCase):
    """Test cases for response quality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.chatbot = HostelChatbot()
    
    def test_response_not_empty(self):
        """Test that responses are not empty"""
        response = self.chatbot.respond("Hello")
        self.assertTrue(len(response) > 0)
    
    def test_response_is_string(self):
        """Test that response is a string"""
        response = self.chatbot.respond("Hello")
        self.assertIsInstance(response, str)
    
    def test_response_contains_useful_info(self):
        """Test that pricing response contains actual data"""
        response = self.chatbot.respond("Tell me about pricing")
        self.assertIn("₹", response)
    
    def test_contact_info_in_response(self):
        """Test that contact info is in responses when relevant"""
        response = self.chatbot.respond("contact")
        self.assertIn("@", response)  # Email should be present

def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestHostelChatbot))
    suite.addTests(loader.loadTestsFromTestCase(TestIntentDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestResponseQuality))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
