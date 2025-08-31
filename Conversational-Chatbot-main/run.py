#!/usr/bin/env python3
"""
Startup script for the College IT Support Chatbot

This script initializes and runs the Flask web application.
Make sure to set your OPENAI_API_KEY environment variable before running.

Usage:
    python run.py

For production deployment:
    gunicorn -w 4 -b 0.0.0.0:5000 app:app
"""

import os
import sys
from app import app, load_faq_data

def check_requirements():
    """Check if all required environment variables and files are present"""
    
    # Check OpenAI API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable is not set!")
        print("Please set your OpenAI API key:")
        print("   Windows: set OPENAI_API_KEY=your_api_key_here")
        print("   Linux/Mac: export OPENAI_API_KEY=your_api_key_here")
        return False
    
    # Check if CSV file exists
    csv_file = 'ICT Cell Common problems - Hardware issues.csv'
    if not os.path.exists(csv_file):
        print(f"❌ Error: FAQ data file '{csv_file}' not found!")
        print("Please make sure the CSV file is in the same directory as this script.")
        return False
    
    return True

def main():
    """Main function to start the application"""
    
    print("🤖 College IT Support Chatbot")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Load FAQ data
    print("📚 Loading FAQ data...")
    if load_faq_data():
        print("✅ FAQ data loaded successfully")
    else:
        print("❌ Warning: Could not load FAQ data")
        print("The chatbot will still work but with limited knowledge.")
    
    # Get configuration
    env = os.environ.get('FLASK_ENV', 'development')
    debug = env == 'development'
    
    print(f"🌍 Environment: {env}")
    print(f"🔧 Debug mode: {debug}")
    print("\n🚀 Starting server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        # Run the Flask app
        app.run(
            debug=debug,
            host='0.0.0.0',
            port=5000,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()