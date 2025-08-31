# api/index.py - Vercel serverless function entry point
from __future__ import annotations

import os
import sys

# Add the parent directory to the path so we can import from the root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app from the main app.py
from app import app, load_faq_data, log

# Initialize FAQ data when the serverless function starts
try:
    if load_faq_data():
        log.info("FAQ data loaded successfully in serverless function")
    else:
        log.warning("Warning: Could not load FAQ data in serverless function")
except Exception as e:
    log.error(f"Error loading FAQ data: {e}")

# Export the Flask app as a handler for Vercel
def handler(request, response):
    """Vercel serverless function handler"""
    return app(request.environ, response)

# Alternative export for Vercel
app_handler = app

# For compatibility with different Vercel configurations
if __name__ == "__main__":
    app.run()