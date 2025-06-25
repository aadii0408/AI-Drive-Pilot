"""
Test configuration for development
Use this to test the app without Google OAuth verification
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TestConfig:
    """Test configuration for development"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')
    DEBUG = True
    
    # Mock Google OAuth for testing
    GOOGLE_CLIENT_ID = 'test-client-id'
    GOOGLE_CLIENT_SECRET = 'test-client-secret'
    
    # Google API scopes
    GOOGLE_SCOPES = [
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/documents.readonly',
        'https://www.googleapis.com/auth/spreadsheets.readonly'
    ]
    
    # OAuth redirect URI
    OAUTH_REDIRECT_URI = "http://localhost:3000/auth/callback"
    
    # Mock data for testing
    MOCK_FILES = {
        'folders': [
            {'id': 'folder1', 'name': 'Test Folder 1', 'mimeType': 'application/vnd.google-apps.folder'},
            {'id': 'folder2', 'name': 'Test Folder 2', 'mimeType': 'application/vnd.google-apps.folder'}
        ],
        'documents': [
            {'id': 'doc1', 'name': 'Sample Document', 'mimeType': 'application/vnd.google-apps.document'},
            {'id': 'doc2', 'name': 'Project Report', 'mimeType': 'application/vnd.google-apps.document'}
        ],
        'spreadsheets': [
            {'id': 'sheet1', 'name': 'Budget Sheet', 'mimeType': 'application/vnd.google-apps.spreadsheet'}
        ]
    }
    
    @staticmethod
    def init_app(app):
        """Initialize app with test configuration"""
        pass 

def strip_extension(filename):
    return os.path.splitext(filename)[0]

# In your search loop:
if is_image_file(file['mimeType']):
    name_no_ext = strip_extension(file['name']).lower()
    if query.lower() in name_no_ext:
        # ... (append to results) 