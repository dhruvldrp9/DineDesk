# Deployment Guide

## Local Development

### Quick Start
1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your API keys
3. Install dependencies: `pip install -r requirements-production.txt`
4. Run setup: `python setup_supabase_direct.py`
5. Start application: `python run.py`

## Production Deployment Options

### 1. Heroku Deployment

Create `Procfile`:
```
web: gunicorn --bind 0.0.0.0:$PORT app_simple:app
```

Deploy steps:
```bash
heroku create your-app-name
heroku config:set GROQ_API_KEY=your_key_here
heroku config:set SUPABASE_URL=your_url_here
heroku config:set DATABASE_URL=your_db_url_here
heroku config:set SESSION_SECRET=your_secret_here
git push heroku main
```

### 2. Railway Deployment

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Railway will automatically detect and deploy Flask app

### 3. Vercel Deployment

Create `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app_simple.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app_simple.py"
    }
  ]
}
```

### 4. DigitalOcean App Platform

1. Connect repository to DO App Platform
2. Configure environment variables
3. Set run command: `gunicorn --bind 0.0.0.0:8080 app_simple:app`

### 5. AWS Elastic Beanstalk

Create `application.py`:
```python
from app_simple import app as application

if __name__ == "__main__":
    application.run()
```

## Environment Variables

Required for all deployments:
```
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
DATABASE_URL=your_postgresql_connection_string
SESSION_SECRET=your_session_secret_key
```

## Post-Deployment Setup

1. Run database setup script once:
   ```bash
   python setup_supabase_direct.py
   ```

2. Verify voice features work (requires HTTPS in production)

3. Test user registration and chat functionality

## Performance Considerations

- Enable gzip compression
- Use CDN for static assets
- Configure database connection pooling
- Set up monitoring and logging

## Security Checklist

- [ ] All API keys stored as environment variables
- [ ] Session secret is random and secure
- [ ] HTTPS enabled for production
- [ ] Database access restricted to app only
- [ ] Regular security updates applied