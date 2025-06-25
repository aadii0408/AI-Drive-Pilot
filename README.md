# 🚀 Drive Copilot

A powerful web application (built with Streamlit) that connects to your Google Drive, enabling intelligent search and Q&A across your documents, spreadsheets, images, and more—with clear source attribution.

---

## ✨ Features

- **Three-Level Retrieval**
  - **All Drive Search**: Search your entire Google Drive.
  - **Folder-Specific Search**: Search within a specific folder.
  - **Document-Specific Search**: Search within a specific document.
- **Content Processing**
  - **Google Docs**: Full text extraction and search.
  - **Google Sheets**: Cell content and data extraction.
  - **PDFs**: Text extraction (if PyPDF2 is installed).
  - **Images**: Thumbnails and metadata (no OCR).
- **Source Attribution**
  - File name, type, snippet, link, and last modified date.
- **Modern UI**
  - Clean, responsive Streamlit interface.
  - File type filter (All, Images, Documents, Spreadsheets).
  - Real-time search and answer display.

---

## 🛠️ Tech Stack

- **Frontend & Backend**: [Streamlit](https://streamlit.io/)
- **Google APIs**: Drive, Docs, Sheets
- **OAuth 2.0**: Secure authentication

---

## 📦 Prerequisites

- Python 3.8+
- Google Cloud Project with APIs enabled:
  - Google Drive API
  - Google Docs API
  - Google Sheets API

---

## ⚡ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>

```

### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project or select an existing one.
3. Enable:
   - Google Drive API
   - Google Docs API
   - Google Sheets API
4. Create OAuth 2.0 credentials:
   - Application type: **Web application**
   - Authorized redirect URI: `http://localhost:8501`
5. Download the `client_secret.json` and place it in the `backend/` directory.

### 4. Run the Streamlit App

```bash
streamlit run streamlit_app.py
```

The app will be available at [http://localhost:8501](http://localhost:8501).

---

## 🐳 Docker Usage

You can run Drive Copilot in a containerized environment using Docker.

### 1. Build the Docker Image

```bash
cd backend
# Build the Docker image (replace 'drive-copilot' with your preferred image name)
docker build -t drive-copilot .
```

### 2. Run the Docker Container

You must provide your `client_secret.json` for Google OAuth. You can do this by mounting it into the container:

```bash
docker run -p 8501:8501 \
  -v $(pwd)/client_secret.json:/app/client_secret.json \
  drive-copilot
```

- The app will be available at [http://localhost:8501](http://localhost:8501).
- If you prefer, you can COPY `client_secret.json` into the image at build time (not recommended for public images).

---

## 🏃 Usage Guide

1. **Authenticate**: Click "Sign in with Google" and grant permissions.
2. **Search**: Enter your query, select context (All Drive, Folder, Document), and optionally filter by file type.
3. **View Results**: See relevant snippets with file name, type, snippet, link, and last modified date.
4. **Source Attribution**: Click file names to open in Google Drive.

---
## 📝 Evaluation

To systematically evaluate Drive Copilot's retrieval and answer quality, use the included evaluation spreadsheet:

### **Evaluation Workflow**

1. **Prepare Test Files**: Create a folder in your Google Drive and add a diverse set of files (Docs, Sheets, PDFs, images, etc.).
2. **Write Test Queries**: Use the "Test Query" column in the spreadsheet to list questions you want to test.
3. **Run Each Query**: Enter the query in Drive Copilot, review the results, and record:
   - **Expected Result**: What you believe the correct answer/snippet should be.


### **Evaluation Spreadsheet Template**

The file `Testing Evals.xlsx` in this directory provides a ready-to-use template.

---

## 🔒 Security & Privacy

- **OAuth 2.0**: Secure Google authentication
- **Read-only Access**: Only reads your Drive content
- **Session Management**: Secure credential handling

---

## 🐞 Troubleshooting

- **Authentication Failed**: Check Google Cloud credentials and redirect URI.
- **No Results**: Ensure files exist and are accessible in your Drive.
- **PDF/Text Extraction Issues**: Make sure `PyPDF2` is installed for PDF support.

---

## 🚧 Future Enhancements

- Full PDF text extraction
- Image OCR (text from images)
- Video/audio transcription
- Advanced filtering (date, type, size)
- Export search results

--- 