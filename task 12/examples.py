
from hadith_chatbot import HadithChatbot
import json


def example_1_basic_search():
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Hadith Search")
    print("="*60)
    
    chatbot = HadithChatbot()
    
    # Search for hadiths about prayer
    results = chatbot.search_hadith("prayer")
    print(f"\nFound {len(results)} hadith(s) about prayer:\n")
    
    for i, hadith in enumerate(results[:3], 1):
        print(f"{i}. {chatbot.format_hadith(hadith)}\n")


def example_2_narrator_search():
    print("\n" + "="*60)
    print("EXAMPLE 2: Search by Narrator")
    print("="*60)
    
    chatbot = HadithChatbot()
    
    # Search for hadiths by Abu Hurairah
    results = chatbot.search_by_narrator("Abu Hurairah")
    print(f"\nFound {len(results)} hadith(s) by Abu Hurairah:\n")
    
    for i, hadith in enumerate(results[:3], 1):
        print(f"{i}. {chatbot.format_hadith(hadith)}\n")


def example_3_collections():
    print("\n" + "="*60)
    print("EXAMPLE 3: Available Collections")
    print("="*60)
    
    chatbot = HadithChatbot()
    
    if chatbot.collections:
        print("\nAvailable hadith collections:")
        for i, name in enumerate(chatbot.collections.keys(), 1):
            print(f"{i}. {name}")
    else:
        print("No collections loaded. Check API connectivity.")


def example_4_multiple_searches():
    print("\n" + "="*60)
    print("EXAMPLE 4: Multiple Searches")
    print("="*60)
    
    chatbot = HadithChatbot()
    
    keywords = ["patience", "honesty", "charity", "wisdom"]
    
    for keyword in keywords:
        results = chatbot.search_hadith(keyword)
        print(f"\n🔍 Searching for: '{keyword}'")
        print(f"   Found: {len(results)} hadith(s)")
        
        if results:
            print(f"   First result: {results[0].get('text', 'N/A')[:100]}...")


def example_5_conversation_simulation():
    print("\n" + "="*60)
    print("EXAMPLE 5: Conversation Simulation")
    print("="*60)
    
    chatbot = HadithChatbot()
    
    # Simulate user queries
    queries = [
        "search kindness",
        "narrator Aisha",
        "find hadiths about knowledge",
        "collections",
        "help"
    ]
    
    for query in queries:
        print(f"\n👤 User: {query}")
        response = chatbot.get_response(query)
        print(f"🤖 Bot: {response[:200]}...\n")
        print("-" * 40)


def example_6_export_to_json():
    print("\n" + "="*60)
    print("EXAMPLE 6: Export to JSON")
    print("="*60)
    
    chatbot = HadithChatbot()
    
    # Search and export
    results = chatbot.search_hadith("mercy", limit=5)
    
    export_data = {
        "query": "mercy",
        "total_results": len(results),
        "hadiths": results
    }
    
    # Save to file
    filename = "hadith_results.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n Results exported to {filename}")
    print(f"  Total hadiths: {len(results)}")


def example_7_interactive_menu():
    print("\n" + "="*60)
    print("EXAMPLE 7: Interactive Menu")
    print("="*60)
    
    chatbot = HadithChatbot()
    
    while True:
        print("\n Hadith Chatbot Menu:")
        print("1. Search by keyword")
        print("2. Search by narrator")
        print("3. View collections")
        print("4. View help")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            query = input("Enter search keyword: ").strip()
            results = chatbot.search_hadith(query)
            print(f"\nFound {len(results)} result(s):")
            for i, hadith in enumerate(results[:3], 1):
                print(f"{i}. {chatbot.format_hadith(hadith)}\n")
        
        elif choice == '2':
            narrator = input("Enter narrator name: ").strip()
            results = chatbot.search_by_narrator(narrator)
            print(f"\nFound {len(results)} result(s):")
            for i, hadith in enumerate(results[:3], 1):
                print(f"{i}. {chatbot.format_hadith(hadith)}\n")
        
        elif choice == '3':
            if chatbot.collections:
                print("\nAvailable collections:")
                for name in chatbot.collections.keys():
                    print(f"• {name}")
            else:
                print("No collections available.")
        
        elif choice == '4':
            print(chatbot.get_help_message())
        
        elif choice == '5':
            print("Wa alaikum assalam wa rahmatullahi wa barakatuh! 🙏")
            break
        
        else:
            print("Invalid option. Please try again.")


def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║           Hadith Chatbot - Usage Examples                  ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    print("Select an example to run:")
    print("1. Basic Hadith Search")
    print("2. Search by Narrator")
    print("3. View Available Collections")
    print("4. Multiple Searches")
    print("5. Conversation Simulation")
    print("6. Export Results to JSON")
    print("7. Interactive Menu (full experience)")
    print("8. Run All Examples")
    print("0. Exit")
    
    choice = input("\nSelect example (0-8): ").strip()
    
    examples = {
        '1': example_1_basic_search,
        '2': example_2_narrator_search,
        '3': example_3_collections,
        '4': example_4_multiple_searches,
        '5': example_5_conversation_simulation,
        '6': example_6_export_to_json,
        '7': example_7_interactive_menu,
    }
    
    if choice == '8':
        for func in examples.values():
            try:
                func()
            except Exception as e:
                print(f"Error running example: {e}")
    elif choice in examples:
        examples[choice]()
    elif choice == '0':
        print("Goodbye! As-salam alaikum 🕌")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
