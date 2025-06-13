from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import time
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream_response', methods=['POST'])
def stream_response():
    user_message = request.json.get('message', '')
    
    # Generate response based on message
    response = generate_response(user_message)
    
    # Return response for streaming
    return jsonify({
        'response': response,
        'delay': 50  # milliseconds between characters
    })

def generate_response(message):
    """Generate contextual restaurant responses"""
    message_lower = message.lower()
    
    if 'book' in message_lower or 'table' in message_lower:
        return "I'd be happy to help you book a table! What date and time are you looking for, and how many people will be joining you?"
    elif 'order' in message_lower or 'food' in message_lower:
        return "Great! I can help you order food. Would you like to see restaurants near you, or do you have a specific cuisine in mind?"
    elif 'menu' in message_lower:
        return "I can show you menus from various restaurants. What type of food are you craving today?"
    else:
        return "Hello! I'm your DineDesk assistant. I can help you book tables, order food, or browse restaurant menus. What would you like to do today?"

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    message = data.get('message', '')
    response = generate_response(message)
    socketio.emit('response', {'message': response})

if __name__ == '__main__':
    socketio.run(app, debug=True) 