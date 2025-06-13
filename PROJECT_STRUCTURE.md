# Project Structure

## Core Application Files

```
dinedesk/
├── app_simple.py              # Main Flask application
├── run.py                     # Application entry point
├── auth.py                    # User authentication system
├── models.py                  # Database models
├── config_supabase.py         # Supabase configuration
└── setup_supabase_direct.py   # Database setup script
```

## Frontend Assets

```
static/
├── css/
│   └── style.css              # Custom styles
└── js/
    ├── main_simple.js         # Text chat interface
    ├── voice_assistant.js     # Voice interaction handling
    └── chat_history.js        # Chat history management
```

## Templates

```
templates/
├── index_simple.html          # Main chat interface
├── voice_assistant.html       # Voice assistant page
└── auth/
    ├── login.html            # Login page
    └── signup.html           # Registration page
```

## Utility Modules

```
utils/
├── __init__.py
├── ai_chat_handler.py         # AI conversation processing
├── simple_chat_storage.py     # Chat persistence
├── database_restaurant_api.py # Restaurant data API
├── database_setup_simple.py   # Sample data population
└── chat_handler.py            # Message processing
```

## Configuration & Documentation

```
├── .env.example               # Environment variables template
├── .gitignore                # Git ignore patterns
├── requirements-production.txt # Python dependencies
├── README.md                  # Project documentation
├── DEPLOYMENT.md              # Deployment instructions
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # MIT license
└── PROJECT_STRUCTURE.md       # This file
```

## Data Files

```
├── users.json                 # User account storage
├── supabase_schema.sql        # Database schema
└── chat_history/              # Chat session files (auto-created)
```

## Key Features by File

### app_simple.py
- Flask routes and API endpoints
- Session management
- Chat message processing
- Voice assistant endpoints

### voice_assistant.js
- Speech recognition integration
- Text-to-speech functionality
- Continuous conversation flow
- Visual wave animations

### ai_chat_handler.py
- Groq API integration
- Natural language processing
- Restaurant query handling
- Context-aware responses

### database_restaurant_api.py
- Supabase database queries
- Restaurant search and filtering
- Menu and booking data
- Error handling and validation

## Entry Points

1. **Development**: `python run.py`
2. **Production**: `gunicorn app_simple:app`
3. **Database Setup**: `python setup_supabase_direct.py`

## Dependencies

All Python dependencies are listed in `requirements-production.txt` with pinned versions for reproducible builds.