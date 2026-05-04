# Hadith Chatbot Configuration File
# Customize settings here

# API Configuration
API_BASE_URL = "https://api.sunnah.com/v1"
API_TIMEOUT = 30  # seconds

# Chat Configuration
MAX_RESULTS = 10  # Maximum hadiths to return per search
DISPLAY_LIMIT = 3  # Number of hadiths to show in chat by default

# Collections to prioritize in search
PRIORITY_COLLECTIONS = [
    "Sahih al-Bukhari",
    "Sahih Muslim",
    "Jami' at-Tirmidhi"
]

# Web Server Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

# Chat Behavior
ENABLE_CONVERSATION_HISTORY = True
MAX_HISTORY_LENGTH = 50  # Maximum conversation entries to keep

# Response Formatting
USE_EMOJIS = True
SHOW_NARRATOR = True
SHOW_COLLECTION = True
SHOW_GRADE = True

# Keywords for intent detection
SEARCH_KEYWORDS = ["search", "find", "look for", "find me"]
NARRATOR_KEYWORDS = ["narrator", "by", "from"]
COLLECTION_KEYWORDS = ["collection", "collections", "books"]

# Help message customization
CUSTOM_WELCOME_MESSAGE = " Welcome to the Hadith Chatbot! "

# Logging Configuration
LOG_ENABLED = False
LOG_FILE = "hadith_chatbot.log"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# Cache Configuration
ENABLE_CACHE = False
CACHE_TIMEOUT = 3600  # 1 hour

# Rate Limiting (for API calls)
RATE_LIMIT_ENABLED = True
RATE_LIMIT_REQUESTS = 30  # per minute
RATE_LIMIT_PERIOD = 60
