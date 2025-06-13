import uuid
import logging
from datetime import datetime
from config_supabase import supabase

class ChatStorage:
    """Handle chat session and message storage in Supabase"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_chat_session(self, user_email, title=None):
        """Create a new chat session for user"""
        try:
            chat_id = str(uuid.uuid4())
            session_title = title or f"Chat {datetime.now().strftime('%b %d, %Y at %I:%M %p')}"
            
            chat_data = {
                'id': chat_id,
                'user_email': user_email,
                'session_title': session_title,
                'started_at': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat(),
                'status': 'active',
                'message_count': 0
            }
            
            result = supabase.table('chat_sessions').insert(chat_data).execute()
            self.logger.info(f"Supabase insert result: {result}")
            
            if result.data:
                self.logger.info(f"Created chat session {chat_id} for user {user_email}")
                return chat_id
            else:
                self.logger.error(f"Failed to create chat session: {result}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error creating chat session: {e}")
            return None
    
    def save_message(self, chat_session_id, message_type, content, message_data=None):
        """Save a message to the chat session"""
        try:
            message_id = str(uuid.uuid4())
            
            message = {
                'id': message_id,
                'chat_session_id': chat_session_id,
                'message_type': message_type,
                'content': content,
                'message_data': message_data,
                'timestamp': datetime.now().isoformat()
            }
            
            # Save message
            result = supabase.table('chat_messages').insert(message).execute()
            
            if result.data:
                # Update session message count and last activity
                self.update_session_activity(chat_session_id)
                return message_id
            else:
                self.logger.error(f"Failed to save message: {result}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error saving message: {e}")
            return None
    
    def update_session_activity(self, chat_session_id):
        """Update session last activity and message count"""
        try:
            # Get current message count
            messages = supabase.table('chat_messages').select('id').eq('chat_session_id', chat_session_id).execute()
            message_count = len(messages.data) if messages.data else 0
            
            # Update session
            update_data = {
                'last_activity': datetime.now().isoformat(),
                'message_count': message_count
            }
            
            supabase.table('chat_sessions').update(update_data).eq('id', chat_session_id).execute()
            
        except Exception as e:
            self.logger.error(f"Error updating session activity: {e}")
    
    def get_user_chat_sessions(self, user_email, limit=50):
        """Get all chat sessions for a user"""
        try:
            result = supabase.table('chat_sessions').select('*').eq('user_email', user_email).order('last_activity', desc=True).limit(limit).execute()
            
            if result.data:
                return result.data
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Error fetching user chat sessions: {e}")
            return []
    
    def get_chat_messages(self, chat_session_id):
        """Get all messages for a chat session"""
        try:
            result = supabase.table('chat_messages').select('*').eq('chat_session_id', chat_session_id).order('timestamp', desc=False).execute()
            
            if result.data:
                return result.data
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Error fetching chat messages: {e}")
            return []
    
    def end_chat_session(self, chat_session_id):
        """Mark a chat session as ended"""
        try:
            update_data = {
                'status': 'ended',
                'last_activity': datetime.now().isoformat()
            }
            
            result = supabase.table('chat_sessions').update(update_data).eq('id', chat_session_id).execute()
            return result.data is not None
            
        except Exception as e:
            self.logger.error(f"Error ending chat session: {e}")
            return False
    
    def delete_chat_session(self, chat_session_id, user_email):
        """Delete a chat session and all its messages"""
        try:
            # Verify session belongs to user
            session = supabase.table('chat_sessions').select('user_email').eq('id', chat_session_id).single().execute()
            
            if not session.data or session.data['user_email'] != user_email:
                self.logger.warning(f"Unauthorized delete attempt for session {chat_session_id}")
                return False
            
            # Delete messages first (cascade should handle this, but being explicit)
            supabase.table('chat_messages').delete().eq('chat_session_id', chat_session_id).execute()
            
            # Delete session
            result = supabase.table('chat_sessions').delete().eq('id', chat_session_id).execute()
            return result.data is not None
            
        except Exception as e:
            self.logger.error(f"Error deleting chat session: {e}")
            return False
    
    def format_message_for_display(self, message):
        """Convert database message to display format"""
        return {
            'id': message['id'],
            'type': message['message_type'],
            'content': message['content'],
            'timestamp': message['timestamp'],
            'message_type': 'text',
            'message_data': message.get('message_data', {})
        }
    
    def convert_session_messages(self, messages):
        """Convert database messages to session format"""
        return [self.format_message_for_display(msg) for msg in messages]