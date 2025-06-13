import os
import logging
import json
from flask import Flask, render_template, session, request, jsonify, redirect, url_for
from datetime import datetime
import uuid
from utils.ai_chat_handler import AIChatHandler
from utils.database_restaurant_api import DatabaseRestaurantAPI
from utils.simple_chat_storage import SimpleChatStorage
from config import Config
# Remove SQLAlchemy models - using Supabase directly
from config_supabase import supabase
from auth import auth_bp, login_required

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")

# Register authentication blueprint
app.register_blueprint(auth_bp)

# Remove local database - use Supabase only
# No SQLAlchemy setup needed since we're using Supabase client directly

# Initialize handlers
chat_handler = AIChatHandler()
restaurant_api = DatabaseRestaurantAPI()
chat_storage = SimpleChatStorage()

# Supabase setup - tables created manually via SQL schema
try:
    # Test Supabase connection
    test_result = supabase.table('restaurants').select('id').limit(1).execute()
    logging.info("Supabase connection successful")
except Exception as e:
    logging.info(f"Supabase connection pending - run supabase_schema.sql in dashboard: {e}")

@app.route('/')
@login_required
def index():
    """Main chat interface route - requires authentication"""
    user_email = session.get('user_id', '')
    
    # Get or create current chat session
    if 'current_chat_id' not in session:
        # Create new chat session
        chat_id = chat_storage.create_chat_session(user_email)
        session['current_chat_id'] = chat_id
        session['chat_history'] = []
        
        # Add personalized welcome message
        user_name = session.get('user_name', 'there')
        welcome_message = {
            'id': str(uuid.uuid4()),
            'type': 'bot',
            'content': f"Welcome back, {user_name}! I'm your AI restaurant assistant. I can help you book tables, browse menus, and order food. How can I assist you today?",
            'timestamp': datetime.now().isoformat(),
            'message_type': 'text'
        }
        
        # Save welcome message to database
        if chat_id:
            chat_storage.save_message(chat_id, user_email, 'bot', welcome_message['content'], welcome_message)
        
        session['chat_history'] = [welcome_message]
    else:
        # Load existing chat history from database
        chat_id = session['current_chat_id']
        if chat_id:
            messages = chat_storage.get_chat_messages(chat_id, user_email)
            session['chat_history'] = chat_storage.convert_session_messages(messages)
    
    return render_template('index_simple.html')

@app.route('/voice')
@login_required
def voice_assistant():
    """Voice assistant interface route"""
    return render_template('voice_assistant.html')

@app.route('/api/send_message', methods=['POST'])
@login_required
def send_message():
    """Handle message sending via AJAX"""
    try:
        data = request.get_json()
        message_content = data.get('message', '').strip()
        
        if not message_content:
            return jsonify({'error': 'Empty message'}), 400
        
        # Create user message
        user_message = {
            'id': str(uuid.uuid4()),
            'type': 'user',
            'content': message_content,
            'timestamp': datetime.now().isoformat(),
            'message_type': 'text'
        }
        
        # Save user message to database
        chat_id = session.get('current_chat_id')
        user_email = session.get('user_id', '')
        if chat_id and user_email:
            chat_storage.save_message(chat_id, user_email, 'user', message_content, user_message)
        
        # Add to session history
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        session['chat_history'].append(user_message)
        session.modified = True
        
        # Process message and get bot response
        bot_response = chat_handler.process_message(message_content, session['chat_history'])
        
        # Save bot response to database
        if chat_id and user_email:
            chat_storage.save_message(chat_id, user_email, 'bot', bot_response['content'], bot_response)
        
        # Add bot response to session history
        session['chat_history'].append(bot_response)
        session.modified = True
        
        return jsonify({
            'user_message': user_message,
            'bot_response': bot_response
        })
        
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/get_history', methods=['GET'])
@login_required
def get_history():
    """Get chat history"""
    return jsonify(session.get('chat_history', []))

@app.route('/api/quick_reply', methods=['POST'])
@login_required
def quick_reply():
    """Handle quick reply button clicks"""
    try:
        data = request.get_json()
        reply_text = data.get('text', '')
        
        if reply_text:
            # Treat as regular message
            return send_message_internal(reply_text)
        
        return jsonify({'error': 'Empty reply'}), 400
        
    except Exception as e:
        logging.error(f"Error processing quick reply: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/new-chat', methods=['POST'])
@login_required
def new_chat():
    """Start a new chat session using Supabase"""
    try:
        user_email = session.get('user_id', '')
        
        # End current chat session if exists
        if 'current_chat_id' in session:
            chat_storage.end_chat_session(session['current_chat_id'], user_email)
        
        # Create new chat session
        new_chat_id = chat_storage.create_chat_session(user_email)
        
        if new_chat_id:
            # Update session with new chat ID
            session['current_chat_id'] = new_chat_id
            session['chat_history'] = []
            
            # Add welcome message to new chat
            user_name = session.get('user_name', 'there')
            welcome_message = {
                'id': str(uuid.uuid4()),
                'type': 'bot',
                'content': f"Hello {user_name}! I'm ready to help you with restaurant recommendations, bookings, and more. What can I do for you?",
                'timestamp': datetime.now().isoformat(),
                'message_type': 'text'
            }
            
            # Save welcome message
            chat_storage.save_message(new_chat_id, user_email, 'bot', welcome_message['content'], welcome_message)
            session['chat_history'] = [welcome_message]
            
            return jsonify({
                'success': True,
                'message': 'New chat started',
                'chat_id': new_chat_id,
                'welcome_message': welcome_message
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create new chat session'
            })
        
    except Exception as e:
        logging.error(f"New chat error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to start new chat'
        })

def send_message_internal(message_content):
    """Internal method to process messages"""
    user_email = session.get('user_id', '')
    chat_id = session.get('current_chat_id')
    
    # Create user message
    user_message = {
        'id': str(uuid.uuid4()),
        'type': 'user',
        'content': message_content,
        'timestamp': datetime.now().isoformat(),
        'message_type': 'text'
    }
    
    # Add to chat history
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    session['chat_history'].append(user_message)
    session.modified = True
    
    # Save user message to storage
    if chat_id:
        chat_storage.save_message(chat_id, user_email, 'user', message_content, user_message)
    
    # Process message and get bot response
    bot_response = chat_handler.process_message(message_content, session['chat_history'])
    
    # Add bot response to history
    session['chat_history'].append(bot_response)
    session.modified = True
    
    # Save bot response to storage
    if chat_id:
        chat_storage.save_message(chat_id, user_email, 'bot', bot_response['content'], bot_response)
    
    return jsonify({
        'user_message': user_message,
        'bot_response': bot_response
    })

@app.route('/api/chat-history', methods=['GET'])
@login_required
def get_chat_history():
    """Get all chat sessions for the current user"""
    try:
        user_email = session.get('user_id', '')
        chat_sessions = chat_storage.get_user_chat_sessions(user_email)
        
        return jsonify({
            'success': True,
            'chat_sessions': chat_sessions
        })
        
    except Exception as e:
        logging.error(f"Error fetching chat history: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch chat history'
        }), 500

@app.route('/api/load-chat/<chat_id>', methods=['POST'])
@login_required
def load_chat(chat_id):
    """Load a specific chat session"""
    try:
        user_email = session.get('user_id', '')
        
        # Verify chat belongs to user
        chat_sessions = chat_storage.get_user_chat_sessions(user_email)
        valid_chat = any(chat['id'] == chat_id for chat in chat_sessions)
        
        if not valid_chat:
            return jsonify({
                'success': False,
                'error': 'Chat session not found'
            }), 404
        
        # End current chat session
        if 'current_chat_id' in session:
            chat_storage.end_chat_session(session['current_chat_id'], user_email)
        
        # Load messages from selected chat
        messages = chat_storage.get_chat_messages(chat_id, user_email)
        session['current_chat_id'] = chat_id
        session['chat_history'] = chat_storage.convert_session_messages(messages)
        
        return jsonify({
            'success': True,
            'messages': session['chat_history'],
            'chat_id': chat_id
        })
        
    except Exception as e:
        logging.error(f"Error loading chat: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to load chat'
        }), 500

@app.route('/api/delete-chat/<chat_id>', methods=['DELETE'])
@login_required
def delete_chat(chat_id):
    """Delete a specific chat session"""
    try:
        user_email = session.get('user_id', '')
        
        # Delete the chat session
        success = chat_storage.delete_chat_session(chat_id, user_email)
        
        if success:
            # If this was the current chat, clear session
            if session.get('current_chat_id') == chat_id:
                session.pop('current_chat_id', None)
                session['chat_history'] = []
            
            return jsonify({
                'success': True,
                'message': 'Chat deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete chat'
            }), 400
            
    except Exception as e:
        logging.error(f"Error deleting chat: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to delete chat'
        }), 500

@app.route('/dashboard')
@login_required
def dashboard():
    """Alternative route to main chat interface"""
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index_simple.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logging.error(f'Server Error: {error}')
    return render_template('index_simple.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)