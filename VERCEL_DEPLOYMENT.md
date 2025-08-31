# Vercel Deployment Guide for TechEdu Hub Chatbot

This guide will help you deploy your Flask-based TechEdu Hub chatbot to Vercel for faster performance compared to Render.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **API Keys**: OpenRouter or OpenAI API key for chat functionality

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository contains these files (already created):
- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function entry point
- `.vercelignore` - Files to exclude from deployment
- `.env.vercel` - Environment variables template
- `requirements.txt` - Python dependencies

### 2. Connect to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect it as a Python project

### 3. Configure Environment Variables

In your Vercel project dashboard, go to **Settings > Environment Variables** and add:

#### Required Variables:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
SECRET_KEY=your_super_secret_key_here_change_in_production
```

#### Optional Variables:
```
FLASK_ENV=production
PYTHONPATH=.
DATABASE_URL=your_database_url_here
EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2
TOP_K=3
MAX_TOKENS=350
CHAT_MODEL=gpt-4o-mini
```

### 4. Deploy

1. Click "Deploy" in Vercel
2. Vercel will:
   - Install dependencies from `requirements.txt`
   - Build the serverless function
   - Deploy static files
   - Provide you with a live URL

### 5. Database Considerations

#### Option 1: SQLite (Default)
- Works for development and small-scale production
- Data is ephemeral (resets on each deployment)
- No additional setup required

#### Option 2: External Database (Recommended for Production)
- Use PostgreSQL, MySQL, or other cloud databases
- Set `DATABASE_URL` environment variable
- Examples:
  ```
  # PostgreSQL
  DATABASE_URL=postgresql://user:password@host:port/database
  
  # MySQL
  DATABASE_URL=mysql://user:password@host:port/database
  ```

### 6. Verify Deployment

After deployment:
1. Visit your Vercel URL
2. Test the chatbot functionality
3. Check user registration and login
4. Verify admin dashboard access
5. Test FAQ search and AI responses

## Key Differences from Render

### Advantages:
- **Faster Cold Starts**: Vercel's serverless functions start faster
- **Global CDN**: Static files served from edge locations
- **Automatic Scaling**: Scales to zero when not in use
- **Better Performance**: Generally faster response times

### Considerations:
- **Serverless Architecture**: Each request is handled independently
- **Memory Limits**: 1GB memory limit per function
- **Execution Time**: 60-second timeout per request
- **Database**: Consider external database for persistent data

## Troubleshooting

### Common Issues:

1. **Import Errors**:
   - Ensure all dependencies are in `requirements.txt`
   - Check Python path configuration

2. **Database Connection**:
   - Verify `DATABASE_URL` environment variable
   - Ensure database is accessible from Vercel

3. **API Key Issues**:
   - Double-check `OPENROUTER_API_KEY` or `OPENAI_API_KEY`
   - Ensure keys have sufficient credits/permissions

4. **Static Files**:
   - Templates and static files are handled automatically
   - Check `vercel.json` configuration if issues occur

### Logs and Debugging:
- View function logs in Vercel dashboard
- Use Vercel CLI for local testing: `vercel dev`
- Check browser developer tools for client-side errors

## Performance Optimization

1. **Database Connection Pooling**: Use connection pooling for external databases
2. **Caching**: Implement caching for FAQ embeddings
3. **Async Operations**: Use async/await for I/O operations where possible
4. **Memory Management**: Monitor memory usage in Vercel dashboard

## Monitoring

- **Vercel Analytics**: Built-in performance monitoring
- **Function Logs**: Real-time logging in dashboard
- **Error Tracking**: Automatic error detection and alerts

## Support

If you encounter issues:
1. Check Vercel documentation: [vercel.com/docs](https://vercel.com/docs)
2. Review function logs in Vercel dashboard
3. Test locally with `vercel dev`
4. Check GitHub repository for configuration files

---

**Note**: This deployment maintains all features from the original Flask application while optimizing for Vercel's serverless environment.