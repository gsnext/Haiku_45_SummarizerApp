# Quick Start Guide - GenAIsummarizer

Get up and running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Azure OpenAI subscription
- Git (optional)

## Step 1: Navigate to Project

```bash
cd summarizer-app
```

## Step 2: Create Virtual Environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI - web framework
- Uvicorn - server
- Azure OpenAI client
- PDF/DOCX processors
- JWT authentication
- And more...

## Step 4: Configure Azure OpenAI

Edit the `.env` file:

```bash
# Windows: notepad .env
# Linux/macOS: nano .env
```

Add your Azure credentials:
```
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
JWT_SECRET_KEY=your-secret-key
```

Get these from:
1. Azure Portal → OpenAI resource
2. Keys and Endpoints section
3. Copy API key and endpoint

## Step 5: Run the Application

```bash
python run.py
```

Expected output:
```
=== Starting GenAIsummarizer server on 127.0.0.1:8000 ===
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## Step 6: Access the Application

1. Open browser: `http://localhost:8000`
2. Enter any username to login
3. Try summarizing some text!

## API Usage

### Get a Token

```bash
curl -X POST http://localhost:8000/api/login \
  -d "username=testuser"
```

Response:
```json
{"token": "your-jwt-token", "username": "testuser"}
```

### Summarize Text

```bash
curl -X POST http://localhost:8000/api/summarize \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text to summarize here",
    "summary_length": "medium"
  }'
```

## Useful URLs

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | Home page |
| http://localhost:8000/dashboard | Main interface |
| http://localhost:8000/history | Summary history |
| http://localhost:8000/about | About page |
| http://localhost:8000/api/health | Health check |

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest backend/tests/

# Run with coverage
pytest backend/tests/ --cov=backend.app
```

## Stop the Application

Press `Ctrl+C` in terminal

## Troubleshooting

### Issue: "No module named 'fastapi'"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Port 8000 already in use
```bash
# Use different port
PORT=9000 python run.py
```

### Issue: Azure credentials not working
1. Verify credentials in `.env`
2. Check Azure Portal for correct values
3. Ensure API key is not expired

### Issue: Virtual environment not activating
```bash
# Windows - try:
python -m venv venv
python -m venv\Scripts\activate.bat

# Linux/macOS - try:
python3 -m venv venv
. venv/bin/activate
```

## Next Steps

- Read [README.md](README.md) for comprehensive documentation
- Review [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- Explore API endpoints with provided examples
- Run the test suite
- Deploy to your server

## Need Help?

1. Check the README.md file
2. Review application logs in `logs/` directory
3. Verify environment variables are set
4. Test Azure OpenAI connection
5. Run tests to diagnose issues

## Project Structure

```
summarizer-app/
├── backend/app/         - FastAPI application
├── frontend/templates/  - HTML templates
├── backend/tests/       - Unit tests
├── requirements.txt     - Dependencies
├── run.py              - Start script
├── .env                - Configuration (edit this!)
├── README.md           - Full documentation
└── DEPLOYMENT.md       - Deployment guide
```

## Summary of Files

- **33 files** total
- **Python backend** with FastAPI
- **Responsive frontend** with HTML/CSS/JS
- **4 HTML templates** for UI
- **Comprehensive tests**
- **Full documentation**

## Key Commands

```bash
# Activate environment
source venv/bin/activate         # Linux/macOS
venv\Scripts\activate            # Windows

# Install packages
pip install -r requirements.txt

# Run app
python run.py

# Run tests
pytest backend/tests/

# Deactivate environment
deactivate
```

## Production Deployment

For Azure App Service, Linux, Docker, or Windows Server:
- See [DEPLOYMENT.md](DEPLOYMENT.md)
- Includes systemd, Docker, Nginx examples
- Security and performance recommendations

---

**Ready to go!** 🚀

Have fun summarizing documents with AI!
