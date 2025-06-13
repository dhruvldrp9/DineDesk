import json
import os
import uuid
import logging
from datetime import datetime
from typing import List, Dict, Optional

class SimpleChatStorage:
    """Simple file-based chat storage system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.chat_dir = "chat_history"
        self.ensure_directory()
    
    def ensure_directory(self):
        """Create chat history directory if it doesn't exist"""
        if not os.path.exists(self.chat_dir):
            os.makedirs(self.chat_dir)
    
    def get_user_file_path(self, user_email: str) -> str:
        """Get the file path for a user's chat history"""
        safe_email = user_email.replace('@', '_at_').replace('.', '_dot_')
        return os.path.join(self.chat_dir, f"{safe_email}_chats.json")
    
    def load_user_chats(self, user_email: str) -> Dict:
        """Load all chats for a user"""
        file_path = self.get_user_file_path(user_email)
        
        if not os.path.exists(file_path):
            return {"user_email": user_email, "chats": []}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Error loading user chats: {e}")
            return {"user_email": user_email, "chats": []}
    
    def save_user_chats(self, user_email: str, chat_data: Dict):
        """Save all chats for a user"""
        file_path = self.get_user_file_path(user_email)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(chat_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            self.logger.error(f"Error saving user chats: {e}")
    
    def create_chat_session(self, user_email: str, title: Optional[str] = None) -> str:
        """Create a new chat session"""
        chat_id = str(uuid.uuid4())
        session_title = title or f"Chat {datetime.now().strftime('%b %d, %Y at %I:%M %p')}"
        
        user_data = self.load_user_chats(user_email)
        
        new_chat = {
            'id': chat_id,
            'user_email': user_email,
            'session_title': session_title,
            'started_at': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat(),
            'status': 'active',
            'message_count': 0,
            'messages': []
        }
        
        user_data['chats'].append(new_chat)
        self.save_user_chats(user_email, user_data)
        
        self.logger.info(f"Created chat session {chat_id} for user {user_email}")
        return chat_id
    
    def save_message(self, chat_session_id: str, user_email: str, message_type: str, content: str, message_data: Optional[Dict] = None) -> str:
        """Save a message to a chat session"""
        message_id = str(uuid.uuid4())
        
        user_data = self.load_user_chats(user_email)
        
        # Find the chat session
        chat_session = None
        for chat in user_data['chats']:
            if chat['id'] == chat_session_id:
                chat_session = chat
                break
        
        if not chat_session:
            self.logger.error(f"Chat session {chat_session_id} not found")
            return ""
        
        # Create message
        message = {
            'id': message_id,
            'chat_session_id': chat_session_id,
            'message_type': message_type,
            'content': content,
            'message_data': message_data or {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Add message to chat
        chat_session['messages'].append(message)
        chat_session['message_count'] = len(chat_session['messages'])
        chat_session['last_activity'] = datetime.now().isoformat()
        chat_session['status'] = 'active'
        
        # Save updated data
        self.save_user_chats(user_email, user_data)
        
        return message_id
    
    def get_user_chat_sessions(self, user_email: str, limit: int = 50) -> List[Dict]:
        """Get all chat sessions for a user"""
        user_data = self.load_user_chats(user_email)
        
        # Sort by last activity (most recent first)
        chats = sorted(user_data['chats'], key=lambda x: x['last_activity'], reverse=True)
        
        # Remove messages from the list view for performance and add formatted timestamps
        chat_list = []
        for chat in chats[:limit]:
            # Format timestamps for display
            last_activity_dt = datetime.fromisoformat(chat['last_activity'])
            now = datetime.now()
            
            # Calculate time differences
            time_diff = now - last_activity_dt
            
            # Format relative time
            if time_diff.days > 0:
                if time_diff.days == 1:
                    relative_time = "1 day ago"
                else:
                    relative_time = f"{time_diff.days} days ago"
            elif time_diff.seconds > 3600:
                hours = time_diff.seconds // 3600
                if hours == 1:
                    relative_time = "1 hour ago"
                else:
                    relative_time = f"{hours} hours ago"
            elif time_diff.seconds > 60:
                minutes = time_diff.seconds // 60
                if minutes == 1:
                    relative_time = "1 minute ago"
                else:
                    relative_time = f"{minutes} minutes ago"
            else:
                relative_time = "Just now"
            
            # Format date and time
            date_str = last_activity_dt.strftime("%B %d, %Y")
            time_str = last_activity_dt.strftime("%I:%M %p")
            
            chat_summary = {k: v for k, v in chat.items() if k != 'messages'}
            chat_summary['formatted_date'] = date_str
            chat_summary['formatted_time'] = time_str
            chat_summary['relative_time'] = relative_time
            chat_list.append(chat_summary)
        
        return chat_list
    
    def get_chat_messages(self, chat_session_id: str, user_email: str) -> List[Dict]:
        """Get all messages for a chat session"""
        user_data = self.load_user_chats(user_email)
        
        # Find the chat session
        for chat in user_data['chats']:
            if chat['id'] == chat_session_id:
                return chat.get('messages', [])
        
        return []
    
    def end_chat_session(self, chat_session_id: str, user_email: str) -> bool:
        """Mark a chat session as ended"""
        user_data = self.load_user_chats(user_email)
        
        # Find and update the chat session
        for chat in user_data['chats']:
            if chat['id'] == chat_session_id:
                chat['status'] = 'ended'
                chat['last_activity'] = datetime.now().isoformat()
                self.save_user_chats(user_email, user_data)
                return True
        
        return False
    
    def delete_chat_session(self, chat_session_id: str, user_email: str) -> bool:
        """Delete a chat session"""
        user_data = self.load_user_chats(user_email)
        
        # Remove the chat session
        original_count = len(user_data['chats'])
        user_data['chats'] = [chat for chat in user_data['chats'] if chat['id'] != chat_session_id]
        
        if len(user_data['chats']) < original_count:
            self.save_user_chats(user_email, user_data)
            return True
        
        return False
    
    def format_message_for_display(self, message: Dict) -> Dict:
        """Convert stored message to display format"""
        return {
            'id': message['id'],
            'type': message['message_type'],
            'content': message['content'],
            'timestamp': message['timestamp'],
            'message_type': 'text',
            'message_data': message.get('message_data', {})
        }
    
    def convert_session_messages(self, messages: List[Dict]) -> List[Dict]:
        """Convert stored messages to session format"""
        return [self.format_message_for_display(msg) for msg in messages]