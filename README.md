# Drive Copilot

A powerful web application that connects to your Google Drive to provide intelligent search and Q&A capabilities across your documents, spreadsheets, and other files.

## 🚀 Features

### **Three-Level Retrieval Architecture**
1. **All Drive Search** - Search across your entire Google Drive
2. **Folder-Specific Search** - Search within a specific folder
3. **Document-Specific Search** - Search within a specific document

### **Intelligent Content Processing**
- **Google Docs** - Full text extraction and search
- **Google Sheets** - Cell content and data extraction
- **Google Slides** - Presentation content extraction
- **PDFs** - Text extraction (placeholder for future implementation)
- **Images & Videos** - Metadata extraction with thumbnails

### **Smart Source Attribution**
- Clear citations with file names and links
- Snippet highlighting with context
- Clickable source links to original documents

### **Modern, Intuitive UI**
- Clean, responsive design
- Real-time search with loading states
- File type icons and visual hierarchy
- Mobile-friendly interface

## 🛠️ Tech Stack

### Frontend
- **React** - Modern UI framework
- **CSS3** - Custom styling with animations
- **Fetch API** - Backend communication

### Backend
- **Flask** - Python web framework
- **Google APIs** - Drive, Docs, Sheets integration
- **OAuth 2.0** - Secure authentication
- **CORS** - Cross-origin resource sharing

## 📋 Prerequisites

1. **Python 3.8+**
2. **Node.js 14+**
3. **Google Cloud Project** with APIs enabled:
   - Google Drive API
   - Google Docs API
   - Google Sheets API

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Co-Piolot-Project
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Configure Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Google Drive API
   - Google Docs API
   - Google Sheets API
4. Create OAuth 2.0 credentials:
   - Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
   - Application type: "Web application"
   - Authorized redirect URIs: `http://localhost:3000/auth/callback`
5. Copy your Client ID and Client Secret

#### Environment Configuration
Create a `.env` file in the `backend` directory:
```env
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
SECRET_KEY=your-secret-key-here-change-this-in-production
FLASK_ENV=development
```

#### Start the Backend Server
```bash
python app.py
```
The backend will run on `http://localhost:5000`

### 3. Frontend Setup

#### Install Node.js Dependencies
```bash
cd frontend
npm install
```

#### Start the Frontend Development Server
```bash
npm start
```
The frontend will run on `http://localhost:3000`

## 🎯 Usage Guide

### 1. Authentication
- Click "Sign in with Google" to authenticate
- Grant necessary permissions to access your Drive
- You'll be redirected back to the application

### 2. Search Your Drive
- **General Search**: Type your query and select "All Drive"
- **Folder Search**: Select "Specific Folder" and choose a folder
- **Document Search**: Select "Specific Document" and choose a file

### 3. Get Intelligent Answers
- The system searches your Drive content
- Provides relevant snippets with source attribution
- Generates intelligent answers based on your content

### 4. Source Attribution
- Each answer includes clear citations
- Click on file names to open in Google Drive
- View relevant snippets with context

## 🔍 Search Examples

### Document Search
```
Query: "Q4 sales projections"
Context: All Drive
Result: Finds relevant content across all your documents
```

### Folder-Specific Search
```
Query: "budget planning"
Context: Specific Folder → "Finance 2024"
Result: Searches only within the Finance 2024 folder
```

### Document-Specific Search
```
Query: "key metrics"
Context: Specific Document → "Q4 Report.docx"
Result: Searches only within the Q4 Report document
```

## 🏗️ Architecture Overview

### Retrieval System
1. **File Indexing**: Organizes files by type and hierarchy
2. **Content Extraction**: Extracts text from various file types
3. **Search Engine**: Full-text search with context awareness
4. **Result Ranking**: Prioritizes by relevance, recency, and hierarchy

### User Experience Flow
1. **Authentication** → Google OAuth
2. **File Discovery** → Browse and select context
3. **Search** → Query processing and retrieval
4. **Results** → Snippets with source attribution
5. **Answers** → AI-generated responses with citations

## 🔒 Security & Privacy

- **OAuth 2.0**: Secure Google authentication
- **Read-only Access**: Only reads your Drive content
- **Session Management**: Secure credential handling
- **CORS Protection**: Controlled cross-origin requests

## 🚧 Future Enhancements

- **PDF Text Extraction**: Full PDF content processing
- **Image OCR**: Text extraction from images
- **Video Transcription**: Speech-to-text for videos
- **Advanced Filtering**: Date, file type, and size filters
- **Collaborative Features**: Team search and sharing
- **Export Functionality**: Save search results and answers

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Check Google Cloud Console credentials
   - Verify redirect URI configuration
   - Clear browser cookies and try again

2. **Search Not Working**
   - Ensure you have files in your Drive
   - Check file permissions
   - Verify API quotas in Google Cloud Console

3. **Backend Connection Error**
   - Check if Flask server is running on port 5000
   - Verify CORS configuration
   - Check network connectivity

### Debug Mode
Enable debug logging in the backend:
```python
# In backend/app.py
logging.basicConfig(level=logging.DEBUG)
```

## 📝 License

This project is for educational and evaluation purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Note**: This application is designed to demonstrate retrieval architecture and user experience. For production use, additional security measures, error handling, and scalability considerations should be implemented. 