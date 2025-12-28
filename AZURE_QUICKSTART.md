# Azure OpenAI Quick Start

## 5-Minute Setup

### 1. Get Azure OpenAI Credentials (2 minutes)
- Go to [Azure Portal](https://portal.azure.com)
- Find your OpenAI resource
- Copy: API Key, Endpoint URL, Deployment Name

### 2. Update .env File (1 minute)
Edit `.env` in project root:
```env
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
```

### 3. Install & Run (2 minutes)
```bash
pip install -r requirements.txt
python run.py
```

### 4. Open Browser
Visit: http://127.0.0.1:8000

---

## Common Credentials from Azure Portal

### Finding Your API Key
1. Azure Portal → Your OpenAI Resource
2. Left sidebar: "Keys and Endpoints"
3. Copy "Key 1" or "Key 2"

### Finding Your Endpoint
1. Same location as above
2. Copy the endpoint URL
- Example: `https://mycompany.openai.azure.com/`

### Finding Deployment Name
1. Azure Portal → "Model deployments"
2. Or left sidebar: "Deployments"
3. Copy your model deployment name
- Example: `gpt-4-deployment` or `gpt-35-turbo`

---

## Test Your Setup

### Method 1: Use Web Interface
1. Go to http://127.0.0.1:8000
2. Click "Continue as Guest"
3. Go to Dashboard
4. Paste sample text and click Summarize

Sample text:
> "The Earth orbits the Sun at an average distance of 93 million miles, completing one full orbit every 365.25 days. The Moon orbits Earth every 27.3 days. Together, these orbital patterns create the seasons and lunar phases that have guided human civilization for millennia."

### Method 2: Test API Directly
```bash
# Create a guest token
curl http://127.0.0.1:8000/api/guest-token

# Copy the token value, then:
curl -X POST http://127.0.0.1:8000/api/summarize \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here", "summary_length": "medium"}'
```

---

## Features Available

✅ Summarize plain text
✅ Upload and summarize PDF files
✅ Upload and summarize DOCX documents
✅ Extract and summarize web pages
✅ Choose summary length (short/medium/long)
✅ View summary history
✅ No login required (guest access)
✅ JWT authentication for registered users

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Azure OpenAI not configured" | Add credentials to `.env` file |
| "Invalid API Key" | Check key in Azure Portal |
| "Connection refused" | Run `python run.py` first |
| "Port 8000 in use" | Change PORT in `.env` or close other apps |
| Empty summary | Check Azure OpenAI quota/limits |

---

## Next Steps

- See `AZURE_OPENAI_SETUP.md` for detailed configuration
- Check `requirements.md` for full feature list
- Review `backend/app/config.py` for all settings
