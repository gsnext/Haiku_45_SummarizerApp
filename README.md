# GenAIsummarizer - AI-Powered Document Summarization

A self-hosted, Python-based web application that uses Azure OpenAI to generate intelligent summaries of documents, web pages, and text content.

## Features

### Core Capabilities
- **Multi-Format Input**: Support for plain text, PDF, DOCX files, and web URLs
- **Configurable Summaries**: Choose from Short, Medium, or Long summary lengths
- **REST API**: Full-featured API endpoints for programmatic access
- **Web Interface**: Responsive, accessible dashboard for manual summarization
- **Batch Processing**: Process up to 10 files in a single request
- **Summary History**: Track and manage previous summaries
- **JWT Authentication**: Secure API access with token-based authentication

### Quality & Reliability
- Comprehensive error handling with user-friendly messages
- Full audit logging of all actions and errors
- Input validation and file size limits (10MB maximum)
- Responsive and accessible UI (keyboard navigation, screen reader support)
- Horizontal scaling support for large document sets

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, Linux, or macOS
- **RAM**: Minimum 2GB (4GB+ recommended)
- **Disk Space**: Minimum 500MB
- **Azure OpenAI**: Subscription and credentials required

## Installation

### 1. Clone or Download the Project

```bash
cd summarizer-app
```

### 2. Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root (template provided):

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production

# Server Configuration
PORT=8000

# Logging Level
LOG_LEVEL=INFO
```

### 5. Run the Application

```bash
python run.py
```

The application will start on `http://localhost:8000`

## Usage

### Web Interface

1. **Navigate to Home**: Visit `http://localhost:8000`
2. **Login**: Enter any username to create a session
3. **Summarize**:
   - **Text**: Paste text directly and summarize
   - **File**: Upload PDF, DOCX, or TXT files
   - **URL**: Provide a web URL to extract and summarize
4. **Choose Length**: Select Short, Medium, or Long summary
5. **View History**: Access previous summaries from the History page

### REST API

#### Authentication
All API endpoints require a JWT token. Obtain a token by logging in:

```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=myuser"
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "myuser"
}
```

#### API Endpoints

**Summarize Text**
```bash
curl -X POST http://localhost:8000/api/summarize \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text here",
    "summary_length": "medium"
  }'
```

**Summarize File**
```bash
curl -X POST http://localhost:8000/api/summarize/file \
  -H "Authorization: Bearer <token>" \
  -F "file=@document.pdf" \
  -F "summary_length=medium"
```

**Summarize URL**
```bash
curl -X POST http://localhost:8000/api/summarize/url \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "url=https://example.com&summary_length=medium"
```

**Batch Processing**
```bash
curl -X POST http://localhost:8000/api/batch \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"text": "Text 1"},
      {"text": "Text 2"},
      {"text": "Text 3"}
    ],
    "summary_length": "medium"
  }'
```

**Get History**
```bash
curl -X GET http://localhost:8000/api/history \
  -H "Authorization: Bearer <token>"
```

**Get Specific Summary**
```bash
curl -X GET http://localhost:8000/api/summary/<summary_id> \
  -H "Authorization: Bearer <token>"
```

**Delete Summary**
```bash
curl -X DELETE http://localhost:8000/api/summary/<summary_id> \
  -H "Authorization: Bearer <token>"
```

**Health Check**
```bash
curl http://localhost:8000/api/health
```

## Project Structure

```
summarizer-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app initialization
│   │   ├── api.py               # REST API endpoints
│   │   ├── ui.py                # Web UI route handlers
│   │   ├── auth.py              # JWT authentication
│   │   ├── config.py            # Configuration settings
│   │   ├── logger.py            # Logging setup
│   │   ├── errors.py            # Custom exceptions
│   │   └── summarizer/
│   │       ├── __init__.py
│   │       ├── engine.py        # Summarization logic
│   │       └── utils.py         # Text extraction utilities
│   └── tests/
│       ├── __init__.py
│       ├── test_api.py          # API endpoint tests
│       ├── test_auth.py         # Authentication tests
│       ├── test_summarizer.py   # Summarization engine tests
│       └── test_history.py      # History tracking tests
├── frontend/
│   ├── __init__.py
│   └── templates/
│       ├── index.html           # Home page
│       ├── dashboard.html       # Main dashboard
│       ├── history.html         # History view
│       └── about.html           # About page
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── startup.sh                   # Deployment startup script
├── .env                         # Environment configuration
└── README.md                    # This file
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8000 | Server port |
| `AZURE_OPENAI_API_KEY` | Required | Azure OpenAI API key |
| `AZURE_OPENAI_ENDPOINT` | Required | Azure OpenAI endpoint URL |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Required | Deployment name |
| `JWT_SECRET_KEY` | Generated | Secret key for JWT signing |
| `LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `DATABASE_URL` | sqlite:///./summarizer.db | Database connection string |

### Summary Lengths

- **Short**: ~50 words - Quick overview
- **Medium**: ~150 words - Balanced summary
- **Long**: ~300 words - Comprehensive summary

### File Upload Limits

- **Maximum file size**: 10MB
- **Supported formats**: PDF, DOCX, TXT
- **Maximum batch items**: 10 per request

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest backend/tests/

# Run with coverage report
pytest backend/tests/ --cov=backend.app --cov-report=html
```

Test files include:
- `test_auth.py` - JWT token creation and verification
- `test_api.py` - API endpoint functionality
- `test_summarizer.py` - Summarization engine
- `test_history.py` - Summary history tracking

Target coverage: 80%+

## Troubleshooting

### Issue: "Azure OpenAI credentials not configured"
**Solution**: Ensure `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` are set in `.env`

### Issue: "Failed to extract text from PDF"
**Solution**: Ensure file is a valid, non-corrupted PDF (max 10MB)

### Issue: 401 Unauthorized errors
**Solution**: Verify JWT token is valid and included in Authorization header

### Issue: Port already in use
**Solution**: Set a different port using `PORT=9000 python run.py`

### Issue: Module import errors
**Solution**: Ensure virtual environment is activated and all dependencies are installed

## Logging

Application logs are stored in the `logs/` directory:
- **Console**: Real-time logging to stdout
- **File**: Rolling logs with 7-day retention, 500MB rotation

Log format: `timestamp | level | module:function:line - message`

## Security Best Practices

1. **Change JWT Secret**: Update `JWT_SECRET_KEY` in production
2. **Secure Azure Credentials**: Never commit `.env` to version control
3. **Use HTTPS**: Deploy behind reverse proxy with SSL/TLS
4. **Rate Limiting**: Implement rate limiting in production
5. **Input Validation**: All inputs are validated for format and size
6. **CORS Configuration**: Currently allows all origins (configure as needed)

## Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

### Azure App Service
Use the provided `startup.sh` script for Azure deployment

### Manual Deployment
1. Set environment variables
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python run.py`

## Performance Considerations

- **Caching**: Implement caching for frequently summarized content
- **Database**: Move from in-memory to persistent database for production
- **Async Processing**: API supports async processing via FastAPI
- **Horizontal Scaling**: Stateless design allows multiple instances
- **Load Balancing**: Deploy behind load balancer for high availability

## Future Enhancements

- [ ] Multiple AI model support
- [ ] PostgreSQL database integration
- [ ] Advanced search and filtering
- [ ] Scheduled batch processing
- [ ] Webhook notifications
- [ ] Custom summarization templates
- [ ] Multi-language support
- [ ] Web scraping for articles

## License

This project is provided as-is for educational and commercial use.

## Support

For issues, questions, or feedback:
1. Check this README for troubleshooting
2. Review logs in the `logs/` directory
3. Ensure all dependencies are properly installed
4. Verify Azure OpenAI configuration

## Development

### Adding New Features

1. Update relevant module in `backend/app/`
2. Add corresponding API route if needed
3. Create or update tests in `backend/tests/`
4. Update this README with new functionality

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Document functions with docstrings
- Keep functions focused and modular

## Changelog

### Version 1.0.0
- Initial release
- Text, file, and URL summarization
- REST API with JWT authentication
- Web UI with history tracking
- Batch processing support
- Comprehensive logging and error handling
