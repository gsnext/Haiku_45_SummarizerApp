# Azure OpenAI Configuration Guide

## Overview
The GenAIsummarizer application is configured to use **Azure OpenAI** for all summarization tasks. This guide explains the setup and how to configure your Azure OpenAI credentials.

## Current Implementation

### Backend Configuration
- **Framework**: FastAPI with Azure OpenAI client
- **Summarization Engine**: `backend/app/summarizer/engine.py`
- **Configuration**: `backend/app/config.py`
- **Environment Variables**: `.env` file

### Azure OpenAI Integration Details

#### 1. **Configuration File** (`backend/app/config.py`)
The application reads Azure OpenAI credentials from environment variables:
```python
AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
```

#### 2. **Summarization Engine** (`backend/app/summarizer/engine.py`)
The engine initializes the Azure OpenAI client:
```python
self.client = AzureOpenAI(
    api_key=settings.AZURE_OPENAI_API_KEY,
    api_version="2024-02-15-preview",
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
)
```

**Key Features:**
- Supports three summary lengths: short (50 words), medium (150 words), long (300 words)
- Uses GPT-4 or GPT-3.5 turbo model (configured via deployment name)
- Temperature: 0.5 for consistent, accurate summaries
- Max tokens: 500

#### 3. **API Endpoints** (`backend/app/api.py`)
Three summarization endpoints:
- `POST /api/summarize` - Summarize text input
- `POST /api/summarize/file` - Summarize uploaded files (PDF, DOCX, TXT)
- `POST /api/summarize/url` - Summarize content from URLs

#### 4. **Frontend Integration** (`frontend/templates/dashboard.html`)
The frontend sends requests with JWT authentication:
```javascript
const response = await fetch('/api/summarize', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
        text: text,
        summary_length: length
    })
});
```

## Setup Instructions

### Prerequisites
1. Azure subscription with OpenAI service deployed
2. API Key and Endpoint from Azure Portal
3. Deployment name for your GPT model

### Step 1: Get Azure OpenAI Credentials

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource
3. Copy these values:
   - **API Key**: Keys and Endpoints → Copy one of the keys
   - **Endpoint**: Keys and Endpoints → Copy the endpoint URL
   - **Deployment Name**: Model deployments → Note your deployment name

### Step 2: Configure Environment Variables

Update `.env` file with your Azure OpenAI credentials:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your-api-key-from-azure-portal
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name

# Example values:
# AZURE_OPENAI_ENDPOINT=https://mycompany.openai.azure.com/
# AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4-deployment

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production

# Server Configuration
PORT=8000

# Logging Configuration
LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=sqlite:///./summarizer.db
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

The `openai` package includes Azure OpenAI support (version 1.0+).

### Step 4: Start the Application

```bash
python run.py
```

The server will start on `http://127.0.0.1:8000`

## Usage

### Guest Access (No Login Required)
1. Open http://127.0.0.1:8000
2. Click "Continue as Guest"
3. Use any summarization feature

### Text Summarization
1. Go to Dashboard → Summarize Text tab
2. Paste your text
3. Select summary length (Short, Medium, Long)
4. Click "Summarize"

### File Summarization
1. Go to Dashboard → File tab
2. Upload PDF, DOCX, or TXT file
3. Select summary length
4. Click "Summarize"

### URL Summarization
1. Go to Dashboard → URL tab
2. Enter webpage URL
3. Select summary length
4. Click "Summarize"

## Features

✅ **Azure OpenAI Integration**
- Uses your Azure OpenAI deployment
- Supports GPT-4 and GPT-3.5-turbo models

✅ **Multiple Input Formats**
- Plain text input
- PDF file upload
- DOCX document upload
- TXT file upload
- Web URL content extraction

✅ **Configurable Summary Length**
- Short: ~50 words
- Medium: ~150 words
- Long: ~300 words

✅ **User Authentication**
- JWT-based authentication
- Guest access without login
- Summary history per user

✅ **Error Handling**
- Validates input size
- Handles failed API calls
- Provides user-friendly error messages

## API Response Format

### Success Response
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "text": "Original text here...",
    "summary": "Generated summary here...",
    "length": "medium",
    "created_at": "2025-12-28T14:22:40.123456",
    "user_id": "guest_abc123"
}
```

### Error Response
```json
{
    "detail": {
        "error": {
            "message": "Azure OpenAI is not configured. Please set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT.",
            "code": "CONFIGURATION_ERROR"
        }
    }
}
```

## Troubleshooting

### "Azure OpenAI is not configured"
- Check if `.env` file exists in project root
- Verify `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` are set
- Ensure no spaces around values in `.env`

### "Invalid API Key"
- Go to Azure Portal and copy the correct key
- Check for trailing/leading spaces
- Verify the key belongs to your OpenAI resource

### "Deployment not found"
- Verify deployment name matches exactly in Azure Portal
- Check it's deployed and running

### "Connection refused"
- Ensure server is running: `python run.py`
- Check PORT is not in use
- Verify firewall settings allow localhost:8000

## Monitoring

Logs are saved in `logs/` directory:
```bash
tail -f logs/app.log
```

Watch for these logs when testing:
- "Guest user created" - Guest session started
- "Token verified for user" - Authentication successful
- "Generating [length] summary" - Summarization started
- "Successfully generated summary" - Summarization completed

## Cost Optimization

### Token Usage Tips
1. **Summary Length**: Use "short" for quick overviews to save tokens
2. **Batch Processing**: Combine multiple summaries if possible
3. **Caching**: The app stores history to avoid re-summarizing

### Expected Costs
- Short summary: ~50-100 tokens
- Medium summary: ~150-250 tokens
- Long summary: ~300-500 tokens

Monitor usage in Azure Portal → OpenAI resource → Monitoring → Usage

## Version Information

- **App Version**: 1.0.0
- **Azure OpenAI API Version**: 2024-02-15-preview
- **OpenAI Package**: Latest (supports Azure)
- **Python**: 3.8+

## Support

For issues or questions:
1. Check logs in `logs/` directory
2. Review error messages in browser console
3. Verify `.env` configuration
4. Check Azure Portal for resource status
