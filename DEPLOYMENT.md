# Deployment Guide for Render

This guide will help you deploy your Conversational Chatbot to Render.

## Prerequisites

1. A Render account (sign up at https://render.com)
2. Your OpenRouter API key
3. Your GitHub repository with the latest code

## Deployment Steps

### 1. Connect Your Repository

1. Log in to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository: `https://github.com/codebyArya-bit/Conversational-Chatbot`
4. Choose the repository and click "Connect"

### 2. Configure Your Service

**Basic Settings:**
- **Name:** `conversational-chatbot` (or your preferred name)
- **Environment:** `Python 3`
- **Region:** Choose the closest to your users
- **Branch:** `main`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app.py`

### 3. Set Environment Variables

In the "Environment" section, add these variables:

**Required:**
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `SECRET_KEY`: Generate a secure random string (Render can auto-generate this)
- `FLASK_ENV`: `production`

**Optional:**
- `DATABASE_URL`: Leave empty to use SQLite (default)
- `FAQ_CSV_PATH`: `ICT Cell Common problems - Hardware issues.csv` (default)
- `EMBED_MODEL`: `sentence-transformers/all-MiniLM-L6-v2` (default)
- `TOP_K`: `3` (default)
- `MAX_TOKENS`: `350` (default)
- `CHAT_MODEL`: `gpt-4o-mini` (default)

### 4. Configure Persistent Storage (Optional)

If you want to persist your SQLite database:

1. Go to "Settings" → "Disks"
2. Add a new disk:
   - **Name:** `chatbot-disk`
   - **Mount Path:** `/opt/render/project/src/instance`
   - **Size:** `1 GB`

### 5. Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. Monitor the build logs for any issues
4. Once deployed, you'll get a URL like: `https://your-app-name.onrender.com`

## Post-Deployment

### Initialize Database

Your app will automatically create the database tables on first run. The SQLite database will be stored in the `instance/` directory.

### Test Your Application

1. Visit your Render URL
2. Test user registration and login
3. Try the chat functionality
4. Test admin dashboard access
5. Create a support ticket

### Admin Access

To create an admin user, you can:
1. Use the Flask shell (if you have access)
2. Or modify the code temporarily to create an admin user on startup

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|----------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key for chat functionality | Yes | None |
| `SECRET_KEY` | Flask secret key for sessions | Yes | Auto-generated |
| `FLASK_ENV` | Flask environment mode | No | `development` |
| `DATABASE_URL` | Database connection string | No | `sqlite:///chatbot.db` |
| `FAQ_CSV_PATH` | Path to FAQ CSV file | No | `ICT Cell Common problems - Hardware issues.csv` |
| `EMBED_MODEL` | Sentence transformer model | No | `sentence-transformers/all-MiniLM-L6-v2` |
| `TOP_K` | Number of top FAQ matches | No | `3` |
| `MAX_TOKENS` | Maximum tokens for chat responses | No | `350` |
| `CHAT_MODEL` | OpenRouter model to use | No | `gpt-4o-mini` |

## Troubleshooting

### Common Issues

1. **Build Fails:** Check that all dependencies in `requirements.txt` are correct
2. **App Won't Start:** Verify environment variables are set correctly
3. **Database Issues:** Ensure the `instance/` directory is writable
4. **Chat Not Working:** Verify your OpenRouter API key is valid

### Logs

Check the Render logs for detailed error messages:
1. Go to your service dashboard
2. Click on "Logs" tab
3. Monitor both build and runtime logs

## Security Notes

- Never commit API keys to your repository
- Use strong, unique SECRET_KEY values
- Consider using PostgreSQL for production instead of SQLite
- Enable HTTPS (Render provides this automatically)

## Scaling

Render will automatically handle scaling based on your plan. For high traffic:
- Consider upgrading to a paid plan
- Use PostgreSQL instead of SQLite
- Implement Redis for session storage
- Add monitoring and alerting