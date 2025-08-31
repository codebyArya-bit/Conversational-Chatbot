# Vercel Frontend Deployment Guide

## Overview
**Note**: This project now uses hybrid deployment (Backend on Render + Frontend on Vercel). For complete deployment instructions, see `HYBRID_DEPLOYMENT_GUIDE.md`.

This guide explains how to deploy only the frontend React application to Vercel.

## Prerequisites
- Vercel account (free tier available)
- GitHub repository with your code
- Node.js installed locally

## Backend Deployment (Serverless Functions)

### 1. Vercel CLI Setup
```bash
npm install -g vercel
vercel login
```

### 2. Deploy Backend
1. Navigate to your project root directory
2. Run the deployment command:
```bash
vercel --prod
```

3. Follow the prompts:
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N** (for first deployment)
   - Project name: `frontend-khaki-sigma`
   - Directory: `.` (current directory)
   - Override settings? **N**

### 3. Environment Variables
After deployment, add these environment variables in Vercel dashboard:
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `FLASK_ENV`: `production`
- `SECRET_KEY`: A secure random string
- `PYTHONPATH`: `.`

## Frontend Deployment

### Deploy Frontend to Vercel
1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Deploy the frontend:
```bash
vercel --prod
```

3. When prompted for project name, use: `frontend-khaki-sigma`

4. Deployment will be available at: `https://frontend-khaki-sigma.vercel.app`

## Configuration Files

### Backend Configuration (`vercel.json`)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb",
        "runtime": "python3.11"
      }
    }
  ],
  "installCommand": "pip install -r requirements-vercel.txt",
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production",
    "PYTHONPATH": "."
  }
}
```

### Frontend Configuration (`frontend/vercel.json`)
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

## Expected URLs
- **Backend API**: `https://conversational-chatbot.onrender.com/api/*` (Deployed on Render)
- **Frontend**: 
  - **Frontend**: `https://frontend-khaki-sigma.vercel.app/`

## Testing the Deployment

### 1. Test Backend API
```bash
curl https://conversational-chatbot.onrender.com/health
```

### 2. Test Frontend
Open your browser and navigate to:
- `https://frontend-khaki-sigma.vercel.app/`

### 3. Test Full Integration
1. Open the frontend URL
2. Try to register/login
3. Test the chatbot functionality
4. Check browser console for any API connection errors

## Troubleshooting

### Common Issues

1. **API Not Found (404)**
   - Ensure `api/index.py` exists and is properly configured
   - Check that `requirements-vercel.txt` includes all dependencies

2. **CORS Errors**
   - Verify CORS configuration in `app.py`
   - Ensure frontend URL is in CORS_ORIGINS

3. **Environment Variables**
   - Add all required environment variables in Vercel dashboard
   - Redeploy after adding environment variables

4. **Build Failures**
   - Check build logs in Vercel dashboard
   - Ensure all dependencies are in `requirements-vercel.txt`

### Logs and Monitoring
- View deployment logs in Vercel dashboard
- Use `vercel logs` command for real-time logs
- Monitor function execution in Vercel analytics

## Auto-Deployment
Once connected to GitHub:
1. Push changes to your repository
2. Vercel automatically deploys on push to main branch
3. Preview deployments for pull requests

## Next Steps
1. Set up custom domain (optional)
2. Configure analytics and monitoring
3. Set up staging environment
4. Implement CI/CD workflows

## Support
If you encounter issues:
1. Check Vercel documentation
2. Review deployment logs
3. Test locally first
4. Check environment variables configuration