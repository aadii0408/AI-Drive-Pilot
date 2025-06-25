import streamlit as st
import os
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import json
from datetime import datetime
import time
import urllib.parse
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

# Allow insecure transport for local development
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Page configuration
st.set_page_config(
    page_title="Drive Copilot",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    .auth-button {
        background: #4285f4;
        color: white;
        padding: 15px 30px;
        border: none;
        border-radius: 8px;
        font-size: 18px;
        cursor: pointer;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

# Initialize session state
if "credentials" not in st.session_state:
    st.session_state.credentials = None
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "auth_step" not in st.session_state:
    st.session_state.auth_step = "start"

def get_file_type_icon(mime_type):
    """Get appropriate icon for file type"""
    icons = {
        "application/vnd.google-apps.folder": "📁",
        "application/vnd.google-apps.document": "📄",
        "application/vnd.google-apps.spreadsheet": "📊",
        "application/vnd.google-apps.presentation": "📈",
        "application/pdf": "📕",
        "image/": "🖼",
        "video/": "🎥"
    }
    
    for key, icon in icons.items():
        if key in mime_type:
            return icon
    return "📎"

def is_image_file(mime_type):
    return mime_type.startswith("image/")

def is_document_file(mime_type):
    return (
        mime_type == "application/vnd.google-apps.document" or
        mime_type == "application/pdf"
    )

def is_spreadsheet_file(mime_type):
    return mime_type == "application/vnd.google-apps.spreadsheet"

def handle_oauth_callback():
    """Handle OAuth callback from URL parameters"""
    query_params = st.query_params
    
    if "code" in query_params and "state" in query_params:
        try:
            # Create OAuth flow
            flow = Flow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                scopes=SCOPES,
                redirect_uri="http://localhost:8501"
            )
            
            # Build the full URL for token exchange
            full_url = f"http://localhost:8501/?{urllib.parse.urlencode(query_params)}"
            
            # Exchange code for tokens
            flow.fetch_token(authorization_response=full_url)
            creds = flow.credentials
            
            # Store credentials in session state
            st.session_state.credentials = {
                "token": creds.token,
                "refresh_token": creds.refresh_token,
                "token_uri": creds.token_uri,
                "client_id": creds.client_id,
                "client_secret": creds.client_secret,
                "scopes": creds.scopes
            }
            st.session_state.authenticated = True
            st.session_state.auth_step = "success"
            
            # Clear URL parameters
            st.query_params.clear()
            
            return True
            
        except Exception as e:
            st.error(f"❌ Authentication failed: {str(e)}")
            st.session_state.auth_step = "error"
            return False
    
    return False

def authenticate():
    """Handle Google OAuth authentication"""
    if not os.path.exists(CLIENT_SECRETS_FILE):
        st.error(f"❌ {CLIENT_SECRETS_FILE} not found!")
        st.markdown("""
        **Please create client_secret.json with your Google OAuth credentials:**
        json
        {
          "web": {
            "client_id": "YOUR_CLIENT_ID",
            "client_secret": "YOUR_CLIENT_SECRET",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:8501"]
          }
        }
        
        """)
        st.stop()
    
    # Check if we have valid credentials
    if st.session_state.credentials:
        try:
            creds = Credentials(**st.session_state.credentials)
            if creds.valid:
                return creds
            elif creds.expired and creds.refresh_token:
                creds.refresh(Request())
                st.session_state.credentials = {
                    "token": creds.token,
                    "refresh_token": creds.refresh_token,
                    "token_uri": creds.token_uri,
                    "client_id": creds.client_id,
                    "client_secret": creds.client_secret,
                    "scopes": creds.scopes
                }
                return creds
        except:
            pass
    
    # Handle OAuth callback
    if handle_oauth_callback():
        st.success("✅ Successfully connected to Google Drive!")
        st.balloons()
        time.sleep(2)
        st.experimental_rerun()
        return None
    
    # Show authentication interface
    st.markdown("### 🔐 Connect to Google Drive")
    st.markdown("Click the button below to connect your Google Drive:")
    
    try:
        # Create OAuth flow
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri="http://localhost:8501"
        )
        
        # Get authorization URL
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        # Create a clickable button
        st.markdown(f"""
        <a href="{auth_url}" target="_blank">
            <button class="auth-button">
                🔑 Connect Google Drive
            </button>
        </a>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("*Steps to connect:*")
        st.markdown("1. Click the button above")
        st.markdown("2. Sign in with your Google account")
        st.markdown("3. Grant permissions to access your Drive")
        st.markdown("4. You'll be redirected back here automatically")
        
    except Exception as e:
        st.error(f"❌ Error setting up connection: {str(e)}")
    
    return None

def list_files(service, query=None, parent=None, max_results=50, file_type_filter=None):
    """List files from Google Drive with optional file type filter"""
    try:
        q_parts = []
        if query:
            q_parts.append(f"fullText contains '{query}'")
        if parent:
            q_parts.append(f"'{parent}' in parents")
        else:
            q_parts.append("trashed = false")
        if file_type_filter == "Images":
            q_parts.append("mimeType contains 'image/'")
        elif file_type_filter == "Documents":
            q_parts.append("(mimeType = 'application/vnd.google-apps.document' or mimeType = 'application/pdf')")
        elif file_type_filter == "Spreadsheets":
            q_parts.append("mimeType = 'application/vnd.google-apps.spreadsheet'")
        q = " and ".join(q_parts) if q_parts else ""
        results = service.files().list(
            q=q,
            pageSize=max_results,
            fields="nextPageToken, files(id, name, mimeType, modifiedTime, size, parents, webViewLink, thumbnailLink, iconLink)"
        ).execute()
        return results.get('files', [])
    except HttpError as error:
        st.error(f"Error listing files: {error}")
        return []

def extract_pdf_text_from_bytes(pdf_bytes):
    if not PyPDF2:
        return '[PDF text extraction unavailable: PyPDF2 not installed]'
    from io import BytesIO
    pdf_stream = BytesIO(pdf_bytes)
    try:
        reader = PyPDF2.PdfReader(pdf_stream)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text
    except Exception as e:
        return f'[PDF text extraction error: {e}]'

def get_file_content(service, file_id, mime_type):
    """Extract content from different file types"""
    try:
        if "application/vnd.google-apps.document" in mime_type:
            doc = service.files().export(fileId=file_id, mimeType='text/plain').execute()
            return doc.decode('utf-8')
        elif "application/vnd.google-apps.spreadsheet" in mime_type:
            sheet = service.files().export(fileId=file_id, mimeType='text/csv').execute()
            return sheet.decode('utf-8')
        elif "application/pdf" in mime_type:
            try:
                pdf_bytes = service.files().get_media(fileId=file_id).execute()
                return extract_pdf_text_from_bytes(pdf_bytes)
            except Exception as e:
                return f"[PDF Content - Unable to extract: {e}]"
        else:
            try:
                content = service.files().get_media(fileId=file_id).execute()
                return content.decode('utf-8', errors='ignore')
            except:
                return "[Content - Unable to extract]"
    except HttpError as error:
        return f"[Error extracting content: {error}]"

def strip_extension(filename):
    return os.path.splitext(filename)[0]

def search_drive(service, query, file_type_filter=None):
    """Search Google Drive for content with file type filter"""
    try:
        files = list_files(service, query=query, max_results=20, file_type_filter=file_type_filter)
        results = []
        for file in files:
            try:
                content = ""
                if is_image_file(file['mimeType']):
                    content = "[Image file: content not searchable]"
                    name_no_ext = strip_extension(file['name']).lower()
                    if query.lower() in name_no_ext:
                        results.append({
                            'file': file,
                            'content': content[:500] + "..." if len(content) > 500 else content,
                            'relevance': 1
                        })
                else:
                    content = get_file_content(service, file['id'], file['mimeType'])
                    if query.lower() in content.lower():
                        results.append({
                            'file': file,
                            'content': content[:500] + "..." if len(content) > 500 else content,
                            'relevance': content.lower().count(query.lower())
                        })
            except Exception as e:
                continue
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results[:10]
    except Exception as e:
        st.error(f"Search error: {e}")
        return []

def generate_answer(query, search_results):
    """Generate an answer based on search results"""
    if not search_results:
        return "I couldn't find any relevant content in your Google Drive for that query."
    
    # Simple answer generation (in a real app, you'd use an AI model)
    answer = f"Based on your search for '{query}', I found {len(search_results)} relevant files:\n\n"
    
    for i, result in enumerate(search_results[:3], 1):
        file = result['file']
        answer += f"{i}. *{file['name']}* ({get_file_type_icon(file['mimeType'])})\n"
        answer += f"   - Modified: {file.get('modifiedTime', 'Unknown')}\n"
        answer += f"   - Content snippet: {result['content'][:200]}...\n\n"
    
    if len(search_results) > 3:
        answer += f"... and {len(search_results) - 3} more files."
    
    return answer

def main():
    """Main application"""
    st.markdown('<h1 class="main-header">🚀 Drive Copilot</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI-powered Google Drive assistant")
    st.warning("*Do not refresh or reuse the OAuth code/URL after authenticating. If you see an error, use the 'Reset Auth' button in the sidebar and try again.*")
    
    # Authentication
    credentials = authenticate()
    
    if not credentials:
        st.info("Please authenticate with Google Drive to continue.")
        return
    
    # Main interface
    st.markdown("### 🔍 Search Your Drive")
    
    # Search interface
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            query = st.text_input(
                "What would you like to search for?",
                placeholder="Enter your search query...",
                key="search_query"
            )
        
        with col2:
            file_type_filter = st.selectbox(
                "File Type",
                ["All", "Images", "Documents", "Spreadsheets"],
                index=0
            )
            file_type_filter = None if file_type_filter == "All" else file_type_filter
        
        with col3:
            search_button = st.button("🔍 Search", type="primary")
    
    # Search results
    if search_button and query:
        with st.spinner("Searching your Drive..."):
            service = build('drive', 'v3', credentials=credentials)
            results = search_drive(service, query, file_type_filter=file_type_filter)
            st.session_state.search_results = results
        
        if results:
            st.success(f"Found {len(results)} relevant files!")
            
            # Display results
            for i, result in enumerate(results):
                file = result['file']
                
                with st.expander(f"{get_file_type_icon(file['mimeType'])} {file['name']}", expanded=i < 2):
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        st.markdown(f"*Type:* {file['mimeType']}")
                        st.markdown(f"*Modified:* {file.get('modifiedTime', 'Unknown')}")
                        if file.get('size'):
                            st.markdown(f"*Size:* {int(file['size']):,} bytes")
                        if is_image_file(file['mimeType']) and file.get('thumbnailLink'):
                            st.image(file['thumbnailLink'], caption=file['name'], width=120)
                    
                    with col2:
                        st.markdown("*Content Preview:*")
                        st.text(result['content'][:300] + "..." if len(result['content']) > 300 else result['content'])
                        
                        if file.get('webViewLink'):
                            st.markdown(f"[Open in Drive]({file['webViewLink']})")
            
            # Generate answer
            st.markdown("### 💡 AI Summary")
            answer = generate_answer(query, results)
            st.markdown(answer)
            
        else:
            st.warning("No relevant files found. Try a different search term.")
    
    # Display previous results if available
    elif st.session_state.search_results:
        st.markdown("### 📋 Previous Search Results")
        for result in st.session_state.search_results[:3]:
            file = result['file']
            st.markdown(f"- {get_file_type_icon(file['mimeType'])} *{file['name']}*")
    
    # Sidebar with additional options
    with st.sidebar:
        st.markdown("### ⚙ Options")
        
        if st.button("🔄 Refresh Authentication"):
            st.session_state.credentials = None
            st.session_state.authenticated = False
            st.experimental_rerun()
        
        if st.button("🗑 Clear Results"):
            st.session_state.search_results = []
            st.experimental_rerun()
        
        if st.button("🔁 Reset Auth (Clear All)"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Stats")
        if st.session_state.search_results:
            st.metric("Files Found", len(st.session_state.search_results))
        
        st.markdown("---")
        st.markdown("### ℹ About")
        st.markdown("Drive Copilot helps you search and analyze your Google Drive content using AI.")

if __name__ == "__main__":
    main()