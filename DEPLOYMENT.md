# GenAIsummarizer Deployment Guide

This guide covers deploying GenAIsummarizer to various environments.

## Local Development

### Prerequisites
- Python 3.8+
- Virtual environment support
- Azure OpenAI subscription

### Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.template .env
# Edit .env with your Azure OpenAI credentials

# 4. Run the application
python run.py
```

The app will be available at `http://localhost:8000`

## Production Deployment

### Windows Server

```powershell
# 1. Install Python 3.8+ from python.org
# 2. Clone the project
git clone <repository-url>
cd summarizer-app

# 3. Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file with production settings
# (Use secure secret keys and Azure credentials)

# 6. Create Windows Service (using NSSM)
nssm install GenAIsummarizer "C:\path\to\venv\Scripts\python.exe" "C:\path\to\run.py"
nssm set GenAIsummarizer AppDirectory "C:\path\to\summarizer-app"
nssm start GenAIsummarizer
```

### Linux/Ubuntu

```bash
# 1. Install Python 3.8+
sudo apt-get update
sudo apt-get install python3.8 python3.8-venv python3-pip

# 2. Clone the project
git clone <repository-url>
cd summarizer-app

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file with production settings

# 6. Run with systemd (recommended)
sudo nano /etc/systemd/system/genaisummarizer.service
```

**Example systemd service file:**

```ini
[Unit]
Description=GenAIsummarizer Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/summarizer-app
Environment="PATH=/path/to/summarizer-app/venv/bin"
ExecStart=/path/to/summarizer-app/venv/bin/python run.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable genaisummarizer
sudo systemctl start genaisummarizer
sudo systemctl status genaisummarizer
```

### Docker Deployment

**Dockerfile:**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "run.py"]
```

**Build and run:**

```bash
# Build image
docker build -t genaisummarizer:1.0.0 .

# Run container
docker run -d \
  --name genaisummarizer \
  -p 8000:8000 \
  -e AZURE_OPENAI_API_KEY=your-key \
  -e AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/ \
  -e AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment \
  -e JWT_SECRET_KEY=your-secret \
  -v genaisummarizer-logs:/app/logs \
  genaisummarizer:1.0.0
```

**Docker Compose:**

```yaml
version: '3.8'

services:
  genaisummarizer:
    build: .
    container_name: genaisummarizer
    ports:
      - "8000:8000"
    environment:
      - AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY}
      - AZURE_OPENAI_ENDPOINT=${AZURE_OPENAI_ENDPOINT}
      - AZURE_OPENAI_DEPLOYMENT_NAME=${AZURE_OPENAI_DEPLOYMENT_NAME}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - PORT=8000
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

### Azure App Service

1. **Create App Service:**
   - Create a new Python App Service on Azure Portal
   - Select Python 3.9 runtime

2. **Deploy using Git:**
   ```bash
   # Add Azure remote
   git remote add azure <azure-repo-url>
   
   # Push to Azure
   git push azure main
   ```

3. **Configure Startup:**
   - Set startup command: `sh startup.sh`

4. **Set Environment Variables:**
   - In Azure Portal → App Service → Settings → Configuration
   - Add application settings:
     - `AZURE_OPENAI_API_KEY`
     - `AZURE_OPENAI_ENDPOINT`
     - `AZURE_OPENAI_DEPLOYMENT_NAME`
     - `JWT_SECRET_KEY`

5. **Restart App Service**

### Nginx Reverse Proxy (Recommended for Production)

**Nginx Configuration:**

```nginx
upstream genaisummarizer {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name example.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;

    client_max_body_size 10M;

    location / {
        proxy_pass http://genaisummarizer;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_request_buffering off;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }

    location /api/ {
        proxy_pass http://genaisummarizer;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Production Considerations

### Security

1. **Environment Variables:**
   - Store all secrets in environment variables
   - Use strong JWT secret keys (32+ characters)
   - Rotate keys regularly

2. **HTTPS:**
   - Always use HTTPS in production
   - Use Let's Encrypt for free SSL certificates
   - Set security headers

3. **Rate Limiting:**
   - Implement rate limiting to prevent abuse
   - Consider using tools like Fail2Ban

4. **Firewall:**
   - Restrict access to trusted IP ranges
   - Use security groups in cloud providers

### Performance

1. **Caching:**
   - Cache frequently requested summaries
   - Use Redis for session management

2. **Load Balancing:**
   - Deploy multiple instances behind a load balancer
   - Use sticky sessions if needed

3. **Database:**
   - Migrate from SQLite to PostgreSQL
   - Set up automated backups

4. **Monitoring:**
   - Monitor CPU, memory, and disk usage
   - Set up alerts for service failures
   - Log all errors and unusual activity

### Backup & Recovery

```bash
# Backup logs directory
tar -czf backup_logs_$(date +%Y%m%d).tar.gz logs/

# Backup configuration
cp .env .env.backup
```

## Troubleshooting Deployment

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>
```

### Permission Denied
```bash
# Make startup script executable
chmod +x startup.sh
```

### Module Not Found
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Connection Refused
- Check if service is running
- Verify port configuration
- Check firewall rules
- Review logs for errors

## Monitoring & Logs

### View Logs

**Docker:**
```bash
docker logs -f genaisummarizer
```

**Systemd:**
```bash
sudo journalctl -u genaisummarizer -f
```

**File:**
```bash
tail -f logs/summarizer.log
```

### Health Check

```bash
curl http://localhost:8000/api/health
```

## Upgrade Procedure

1. Backup current installation
2. Stop the service
3. Pull latest code
4. Update dependencies: `pip install -r requirements.txt`
5. Run any migrations (if applicable)
6. Start the service
7. Verify health endpoint

## Support

For deployment issues:
- Check application logs
- Verify environment variables
- Test Azure OpenAI connectivity
- Review system resources
