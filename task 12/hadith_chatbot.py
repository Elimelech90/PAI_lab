"""
Hadith Chatbot using sunnah.com API
This chatbot allows users to search and discuss Islamic Hadiths
"""

import requests
import json
from typing import List, Dict, Optional
import re


class HadithChatbot:
    """A chatbot that interfaces with sunnah.com API to provide Hadith information"""
    
    def __init__(self):
        self.base_url = "https://api.sunnah.com/v1"
        self.api_key = None  # If needed for authentication
        self.conversation_history = []
        self.collections = {}
        self.load_collections()
    
    def load_collections(self) -> None:
        """Load available Hadith collections from the API"""
        try:
            response = requests.get(f"{self.base_url}/collections")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'collections' in data:
                    self.collections = {col['name']: col for col in data['collections']}
                    print("✓ Collections loaded successfully")
                    print(f"  Available collections: {', '.join(self.collections.keys())}")
                else:
                    self.collections = {}
        except Exception as e:
            print(f"Warning: Could not load collections: {e}")
    
    def search_hadith(self, query: str, collection: Optional[str] = None) -> List[Dict]:
        """
        Search for hadiths based on a query
        
        Args:
            query: Search query text
            collection: Optional specific collection to search in
            
        Returns:
            List of matching hadith records
        """
        try:
            search_params = {
                'search': query,
                'limit': 10
            }
            
            if collection and collection in self.collections:
                search_params['collection'] = collection
            
            response = requests.get(f"{self.base_url}/hadiths", params=search_params)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'hadiths' in data:
                    return data['hadiths']
                return []
            else:
                return []
                
        except Exception as e:
            print(f"Error searching hadiths: {e}")
            return []
    
    def get_hadith_by_id(self, hadith_id: str) -> Optional[Dict]:
        """Get a specific hadith by its ID"""
        try:
            response = requests.get(f"{self.base_url}/hadiths/{hadith_id}")
            if response.status_code == 200:
                data = response.json()
                return data.get('hadith') or data
            return None
        except Exception as e:
            print(f"Error retrieving hadith: {e}")
            return None
    
    def search_by_keyword(self, keyword: str) -> List[Dict]:
        """Search hadiths by keyword"""
        return self.search_hadith(keyword)
    
    def search_by_narrator(self, narrator: str) -> List[Dict]:
        """Search hadiths by narrator name"""
        try:
            response = requests.get(
                f"{self.base_url}/hadiths",
                params={'narrator': narrator, 'limit': 10}
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('hadiths', [])
            return []
        except Exception as e:
            print(f"Error searching by narrator: {e}")
            return []
    
    def format_hadith(self, hadith: Dict) -> str:
        """Format hadith for display"""
        output = []
        
        if 'text' in hadith:
            output.append(f"📖 Hadith:\n{hadith['text']}\n")
        
        if 'narrator' in hadith:
            output.append(f"👤 Narrator: {hadith['narrator']}")
        
        if 'collection' in hadith:
            output.append(f"📚 Collection: {hadith['collection']}")
        
        if 'grade' in hadith:
            output.append(f"✓ Grade: {hadith['grade']}")
        
        if 'book' in hadith and 'number' in hadith:
            output.append(f"📖 Book {hadith.get('book', '')}, Hadith #{hadith.get('number', '')}")
        
        return "\n".join(output)
    
    def add_to_history(self, user_message: str, bot_response: str) -> None:
        """Add conversation to history"""
        self.conversation_history.append({
            'user': user_message,
            'bot': bot_response
        })
    
    def get_response(self, user_input: str) -> str:
        """Generate chatbot response to user input"""
        user_input = user_input.strip()
        
        # Intent detection
        if any(keyword in user_input.lower() for keyword in ['search', 'find', 'look for']):
            query = user_input.lower().replace('search for ', '').replace('find ', '').strip()
            hadiths = self.search_hadith(query)
            
            if hadiths:
                response = f"Found {len(hadiths)} hadith(s):\n\n"
                for i, hadith in enumerate(hadiths[:3], 1):
                    response += f"{i}. {self.format_hadith(hadith)}\n\n"
                return response
            else:
                return "Sorry, I couldn't find any hadiths matching your search query."
        
        elif any(keyword in user_input.lower() for keyword in ['narrator', 'by']):
            narrator = user_input.lower().replace('narrator ', '').replace('by ', '').strip()
            hadiths = self.search_by_narrator(narrator)
            
            if hadiths:
                response = f"Found {len(hadiths)} hadith(s) by {narrator}:\n\n"
                for i, hadith in enumerate(hadiths[:3], 1):
                    response += f"{i}. {self.format_hadith(hadith)}\n\n"
                return response
            else:
                return f"No hadiths found from narrator: {narrator}"
        
        elif 'help' in user_input.lower():
            return self.get_help_message()
        
        elif 'collections' in user_input.lower():
            if self.collections:
                return "Available collections:\n" + "\n".join(f"- {name}" for name in self.collections.keys())
            else:
                return "No collections loaded. Please try again later."
        
        elif 'history' in user_input.lower():
            if self.conversation_history:
                response = "Conversation History:\n"
                for i, entry in enumerate(self.conversation_history[-5:], 1):
                    response += f"\n{i}. User: {entry['user']}\n   Bot: {entry['bot'][:100]}...\n"
                return response
            else:
                return "No conversation history yet."
        
        else:
            # General hadith search
            hadiths = self.search_hadith(user_input)
            if hadiths:
                response = f"Found {len(hadiths)} hadith(s) related to '{user_input}':\n\n"
                for i, hadith in enumerate(hadiths[:2], 1):
                    response += f"{i}. {self.format_hadith(hadith)}\n\n"
                return response
            else:
                return "I didn't find any matching hadiths. Try: 'search [keyword]', 'narrator [name]', or 'help'"
    
    def get_help_message(self) -> str:
        """Return help message with available commands"""
        return """
🤖 Hadith Chatbot - Available Commands:

1. Search Hadiths:
   - "search [keyword]" - Search for hadiths by keyword
   - "[any topic]" - Direct search

2. Search by Narrator:
   - "narrator [name]" - Find hadiths by a specific narrator
   - "by [narrator name]" - Alternative format

3. Information:
   - "collections" - Show available hadith collections
   - "history" - Show recent conversation history
   - "help" - Show this help message

4. Quit:
   - "exit" or "quit" - End the conversation

Examples:
- "search mercy"
- "narrator Abu Hurairah"
- "find hadiths about prayer"
        """
    
    def run_chat_loop(self) -> None:
        """Run the interactive chat loop"""
        print("\n" + "="*60)
        print("🕌 Welcome to the Hadith Chatbot 🕌")
        print("="*60)
        print("Type 'help' for available commands or 'exit' to quit.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit']:
                    print("\nBot: Jazakallah khair for using the Hadith Chatbot. As-salam alaikum! 🙏")
                    break
                
                response = self.get_response(user_input)
                print(f"\nBot: {response}\n")
                self.add_to_history(user_input, response)
                
            except KeyboardInterrupt:
                print("\n\nBot: Wa alaikum assalam wa rahmatullahi wa barakatuh 🙏")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main function to run the chatbot"""
    chatbot = HadithChatbot()
    chatbot.run_chat_loop()


if __name__ == "__main__":
    main()
