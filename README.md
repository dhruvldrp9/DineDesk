# DineDesk - AI Restaurant Assistant

An intelligent restaurant discovery and booking platform that leverages AI, voice interactions, and real-time data integration to provide a seamless dining exploration experience.

![DineDesk Logo](https://via.placeholder.com/200x80/2563eb/ffffff?text=DineDesk)

## Features

### 🤖 AI-Powered Chat Assistant
- Natural language processing for restaurant queries
- Intelligent recommendations based on cuisine preferences
- Real-time conversation with context awareness
- Menu browsing and restaurant details

### 🎤 Voice Assistant
- Voice-to-text recognition for hands-free interaction
- Text-to-speech responses from the AI assistant
- Continuous conversation mode until completion
- Dynamic visual feedback with wave animations

### 📱 User Experience
- Modern, responsive web interface
- User authentication (login/signup)
- Persistent chat history across sessions
- Seamless navigation between text and voice modes

### 🍽️ Restaurant Features
- Comprehensive restaurant database
- Cuisine-based filtering and search
- Table booking capabilities
- Menu exploration with detailed descriptions

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: Supabase PostgreSQL
- **AI**: Groq API for natural language processing
- **Frontend**: HTML5, CSS3 (Tailwind), JavaScript
- **Voice**: Web Speech API (SpeechRecognition & SpeechSynthesis)
- **Authentication**: Session-based with JSON file storage

## Prerequisites

Before running DineDesk, ensure you have:

1. **Python 3.8+** installed
2. **Supabase account** with a project created
3. **Groq API key** for AI functionality

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/dinedesk.git
cd dinedesk
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the root directory:
```bash
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
DATABASE_URL=your_supabase_postgresql_connection_string

# AI Configuration
GROQ_API_KEY=your_groq_api_key

# Flask Configuration
SESSION_SECRET=your_secret_key_for_sessions
```

### 4. Database Setup

Run the database schema setup:
```bash
python setup_supabase_direct.py
```

This will create all necessary tables and populate sample restaurant data.

### 5. User Data Initialization

Create an initial `users.json` file:
```json
{}
```

## Running the Application

### Development Mode
```bash
python app_simple.py
```

### Production Mode
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload app_simple:app
```

The application will be available at `http://localhost:5000`

## API Keys Setup

### Supabase Setup
1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Create a new project
3. Go to Settings → API
4. Copy your project URL and anon key
5. Go to Settings → Database
6. Copy your connection string

### Groq API Setup
1. Visit [Groq Console](https://console.groq.com/)
2. Create an account and generate an API key
3. Add the key to your environment variables

## Usage

### Text Chat Interface
1. Register/Login to your account
2. Start typing messages to interact with the AI assistant
3. Ask about restaurants, cuisines, or make reservations
4. Access chat history from the user menu

### Voice Assistant
1. Click "Voice Assistant" from the main interface
2. Tap the microphone button to start conversation
3. Speak naturally - the assistant will respond audibly
4. Say "thank you" or "goodbye" to end the conversation

## Project Structure

```
dinedesk/
├── static/
│   ├── css/
│   └── js/
│       ├── main_simple.js
│       ├── voice_assistant.js
│       └── chat_history.js
├── templates/
│   ├── index_simple.html
│   ├── voice_assistant.html
│   └── auth/
├── utils/
│   ├── ai_chat_handler.py
│   ├── simple_chat_storage.py
│   └── database_restaurant_api.py
├── app_simple.py
├── auth.py
├── models.py
├── config_supabase.py
└── requirements.txt
```

## API Endpoints

- `GET /` - Main chat interface
- `GET /voice` - Voice assistant interface
- `POST /api/send_message` - Process chat messages
- `POST /api/new_chat` - Start new conversation
- `GET /api/chat_history` - Retrieve chat sessions
- `POST /auth/signup` - User registration
- `POST /auth/login` - User authentication

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

**Voice Recognition Not Working:**
- Ensure you're using HTTPS or localhost
- Grant microphone permissions in browser
- Check browser compatibility (Chrome/Edge recommended)

**Database Connection Errors:**
- Verify Supabase credentials in `.env`
- Run database setup script again
- Check Supabase project status

**AI Responses Not Working:**
- Verify Groq API key is valid
- Check API rate limits
- Ensure internet connectivity

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email contact@dhruv.at or create an issue in the GitHub repository.

## Acknowledgments

- Groq for AI language processing
- Supabase for database and backend services
- Web Speech API for voice functionality
- Tailwind CSS for styling framework
