#!/usr/bin/env python3
"""
DineDesk Application Entry Point
Run this file to start the DineDesk AI Restaurant Assistant
"""

import os
import sys
from app_simple import app

if __name__ == '__main__':
    # Check for environment variables
    required_vars = ['GROQ_API_KEY', 'SUPABASE_URL', 'DATABASE_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Please check your .env file or environment configuration")
        print("   See .env.example for required variables")
        sys.exit(1)
    
    print("🚀 Starting DineDesk AI Restaurant Assistant...")
    print("📱 Access the application at: http://localhost:5000")
    print("🎤 Voice features require HTTPS or localhost")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Run the Flask application
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )