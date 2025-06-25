import os
from dotenv import load_dotenv
import secrets

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the Flask application"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # Google OAuth settings
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'your-client-id')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'your-client-secret')
    
    # Google API scopes
    GOOGLE_SCOPES = [
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/documents.readonly',
        'https://www.googleapis.com/auth/spreadsheets.readonly'
    ]
    
    # OAuth redirect URI
    OAUTH_REDIRECT_URI = "http://localhost:3000/auth/callback"
    
    # Optional: OpenAI API for LLM integration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Search settings
    MAX_SEARCH_RESULTS = 20
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def init_app(app):
        """Initialize app with configuration"""
        pass 

print(secrets.token_hex(32)) 