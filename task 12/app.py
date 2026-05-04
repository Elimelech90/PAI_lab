from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from hadith_chatbot import HadithChatbot
import json

app = Flask(__name__)
CORS(app)

# Initialize the chatbot
chatbot = HadithChatbot()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get response from chatbot
        response = chatbot.get_response(user_message)
        
        # Add to history
        chatbot.add_to_history(user_message, response)
        
        return jsonify({
            'message': response,
            'user': user_message,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500


@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.json
        query = data.get('query', '').strip()
        collection = data.get('collection')
        
        if not query:
            return jsonify({'error': 'Empty query'}), 400
        
        results = chatbot.search_hadith(query, collection)
        
        return jsonify({
            'results': results,
            'count': len(results),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500


@app.route('/api/collections', methods=['GET'])
def get_collections():
    try:
        collections = list(chatbot.collections.keys())
        return jsonify({
            'collections': collections,
            'count': len(collections),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500


@app.route('/api/narrator', methods=['POST'])
def search_narrator():
    try:
        data = request.json
        narrator = data.get('narrator', '').strip()
        
        if not narrator:
            return jsonify({'error': 'Empty narrator name'}), 400
        
        results = chatbot.search_by_narrator(narrator)
        
        return jsonify({
            'results': results,
            'narrator': narrator,
            'count': len(results),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500


@app.route('/api/help', methods=['GET'])
def get_help():
    return jsonify({
        'help': chatbot.get_help_message(),
        'status': 'success'
    })


@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify({
        'history': chatbot.conversation_history,
        'status': 'success'
    })


if __name__ == '__main__':
    print("Starting Hadith Chatbot Web Server...")
    print("Server running at http://localhost:5000")
    app.run(debug=True, port=5000)
