import requests
import json
from typing import List, Dict, Optional
from datetime import datetime
import logging
from functools import lru_cache
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hadith_chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class HadithChatbotAdvanced:
    def __init__(self, cache_enabled=True):
        self.base_url = "https://api.sunnah.com/v1"
        self.api_key = None
        self.conversation_history = []
        self.collections = {}
        self.cache_enabled = cache_enabled
        self.cache = {}
        
        logger.info("Initializing Hadith Chatbot Advanced")
        self.load_collections()
    
    def load_collections(self) -> None:
        try:
            logger.info("Loading collections from API...")
            response = requests.get(
                f"{self.base_url}/collections",
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            if isinstance(data, dict) and 'collections' in data:
                self.collections = {col['name']: col for col in data['collections']}
                logger.info(f"Successfully loaded {len(self.collections)} collections")
            else:
                self.collections = {}
                logger.warning("Unexpected API response format")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to load collections: {e}")
            self.collections = {}
        
        except Exception as e:
            logger.error(f"Unexpected error loading collections: {e}")
            self.collections = {}
    
    def _get_cache_key(self, query: str, collection: Optional[str] = None) -> str:
        """Generate cache key for search results"""
        return f"{query}:{collection}"
    
    def search_hadith(self, query: str, collection: Optional[str] = None) -> List[Dict]:
        # Check cache first
        if self.cache_enabled:
            cache_key = self._get_cache_key(query, collection)
            if cache_key in self.cache:
                logger.info(f"Cache hit for query: {query}")
                return self.cache[cache_key]
        
        try:
            logger.info(f"Searching for hadiths: query='{query}', collection='{collection}'")
            
            search_params = {
                'search': query,
                'limit': 10
            }
            
            if collection and collection in self.collections:
                search_params['collection'] = collection
                logger.info(f"Limiting search to collection: {collection}")
            
            response = requests.get(
                f"{self.base_url}/hadiths",
                params=search_params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            results = data.get('hadiths', []) if isinstance(data, dict) else []
            
            # Cache results
            if self.cache_enabled:
                cache_key = self._get_cache_key(query, collection)
                self.cache[cache_key] = results
                logger.info(f"Cached {len(results)} results for query: {query}")
            
            logger.info(f"Search returned {len(results)} results")
            return results
        
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return []
        
        except Exception as e:
            logger.error(f"Error during search: {e}")
            return []
    
    def search_by_narrator(self, narrator: str) -> List[Dict]:
        try:
            logger.info(f"Searching for hadiths by narrator: {narrator}")
            
            response = requests.get(
                f"{self.base_url}/hadiths",
                params={'narrator': narrator, 'limit': 10},
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            results = data.get('hadiths', []) if isinstance(data, dict) else []
            
            logger.info(f"Found {len(results)} hadiths by {narrator}")
            return results
        
        except Exception as e:
            logger.error(f"Error searching by narrator: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        stats = {
            'total_conversations': len(self.conversation_history),
            'total_collections': len(self.collections),
            'cache_size': len(self.cache),
            'collections': list(self.collections.keys())
        }
        
        logger.info(f"Statistics: {stats}")
        return stats
    
    def clear_cache(self) -> None:
        cache_size = len(self.cache)
        self.cache.clear()
        logger.info(f"Cache cleared (freed {cache_size} entries)")
    
    def export_history(self, filename: str = "conversation_history.json") -> bool:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Conversation history exported to {filename}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to export history: {e}")
            return False
    
    def import_history(self, filename: str = "conversation_history.json") -> bool:
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    self.conversation_history = json.load(f)
                
                logger.info(f"Conversation history imported from {filename}")
                return True
            else:
                logger.warning(f"History file not found: {filename}")
                return False
        
        except Exception as e:
            logger.error(f"Failed to import history: {e}")
            return False
    
    def log_search(self, query: str, results_count: int) -> None:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'results': results_count
        }
        
        logger.info(f"Search logged: {log_entry}")
    
    def format_hadith(self, hadith: Dict) -> str:
        output = []
        
        if 'text' in hadith:
            output.append(f" Hadith:\n{hadith['text']}\n")
        
        if 'narrator' in hadith:
            output.append(f" Narrator: {hadith['narrator']}")
        
        if 'collection' in hadith:
            output.append(f" Collection: {hadith['collection']}")
        
        if 'grade' in hadith:
            output.append(f" Grade: {hadith['grade']}")
        
        return "\n".join(output)
    
    def get_response(self, user_input: str) -> str:
        logger.info(f"Processing user input: {user_input[:50]}...")
        
        if 'search' in user_input.lower():
            query = user_input.lower().replace('search for ', '').replace('search ', '').strip()
            hadiths = self.search_hadith(query)
            self.log_search(query, len(hadiths))
            
            if hadiths:
                response = f"Found {len(hadiths)} hadith(s):\n\n"
                for i, hadith in enumerate(hadiths[:3], 1):
                    response += f"{i}. {self.format_hadith(hadith)}\n\n"
                return response
            else:
                return "No hadiths found."
        
        elif 'narrator' in user_input.lower() or 'by' in user_input.lower():
            narrator = user_input.lower().replace('narrator ', '').replace('by ', '').strip()
            hadiths = self.search_by_narrator(narrator)
            self.log_search(narrator, len(hadiths))
            
            if hadiths:
                response = f"Found {len(hadiths)} hadith(s) by {narrator}:\n\n"
                for i, hadith in enumerate(hadiths[:3], 1):
                    response += f"{i}. {self.format_hadith(hadith)}\n\n"
                return response
            else:
                return f"No hadiths found from {narrator}"
        
        else:
            hadiths = self.search_hadith(user_input)
            self.log_search(user_input, len(hadiths))
            
            if hadiths:
                return f"Found {len(hadiths)} hadith(s):\n\n" + "\n\n".join(
                    [self.format_hadith(h) for h in hadiths[:2]]
                )
            else:
                return "I couldn't find matching hadiths. Try 'search [keyword]'"
    
    def add_to_history(self, user_message: str, bot_response: str) -> None:
        entry = {
            'timestamp': datetime.now().isoformat(),
            'user': user_message,
            'bot': bot_response
        }
        self.conversation_history.append(entry)
        logger.info(f"Conversation logged: {len(self.conversation_history)} entries")


def main():
    chatbot = HadithChatbotAdvanced(cache_enabled=True)
    
    print("Advanced Hadith Chatbot with Logging and Caching")
    print("=" * 50)
    
    # Example searches
    searches = ["prayer", "mercy", "honesty"]
    
    for search_term in searches:
        results = chatbot.search_hadith(search_term)
        print(f"\nSearched: {search_term}")
        print(f"Found: {len(results)} results")
    
    # Show statistics
    stats = chatbot.get_statistics()
    print(f"\nStatistics: {stats}")
    
    # Export history
    chatbot.export_history()


if __name__ == "__main__":
    main()
