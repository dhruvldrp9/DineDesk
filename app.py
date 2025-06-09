from flask import Flask, render_template, Response, request, jsonify
from flask_socketio import SocketIO, emit
import time
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    message = data.get('message', '')
    
    # Simulate processing delay
    time.sleep(0.5)
    
    # For now, just echo "Thank you" for any message
    response = "Thank you"
    
    # Emit the response back to the client
    emit('response', {'message': response})

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True) 