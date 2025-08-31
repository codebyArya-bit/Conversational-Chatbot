# Hybrid Deployment Guide: Backend on Render + Frontend on Vercel

## Overview
This guide explains how to deploy your Conversational Chatbot with:
- **Backend**: Flask API on Render
- **Frontend**: React app on Vercel

## Architecture
```
User → Vercel (Frontend) → Render (Backend API)
```

## Part 1: Backend Deployment on Render

### 1. Manual Deployment via Render Dashboard

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Connect GitHub Repository**:
   - Click "New +" → "Blueprint"
   - Connect your GitHub account
   - Select repository: `codebyArya-bit/Conversational-Chatbot`
   - Branch: `main`

3. **Configure Service**:
   - Service will be auto-configured from `render.yaml`
   - Service Name: `conversational-chatbot`
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

4. **Set Environment Variables**:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   FLASK_ENV=production
   SECRET_KEY=your_secret_key_here
   ```

5. **Deploy**: Click "Apply" to start deployment

### 2. Expected Backend URL
- **API Base URL**: `https://conversational-chatbot.onrender.com`
- **Health Check**: `https://conversational-chatbot.onrender.com/health`
- **API Endpoints**: `https://conversational-chatbot.onrender.com/api/*`

## Part 2: Frontend Deployment on Vercel

### 1. Install Vercel CLI
```bash
npm install -g vercel
vercel login
```

### 2. Deploy Frontend to Vercel

#### Deploy to Vercel
```bash
cd frontend
vercel --prod --name frontend-khaki-sigma
```
- Project name: `frontend-khaki-sigma`
- URL: `https://frontend-khaki-sigma.vercel.app`

### 3. Vercel Configuration
The frontend is configured with:
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Framework**: React
- **Node Version**: 18

## Part 3: Configuration Files

### Backend Configuration (`render.yaml`)
```yaml
services:
  - type: web
    name: conversational-chatbot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: OPENROUTER_API_KEY
        sync: false
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
    healthCheckPath: /
```

### Frontend Configuration (`.env.production`)
```env
# Production environment variables for Vercel deployment
# Backend API URL pointing to Render deployment
REACT_APP_API_URL=https://conversational-chatbot.onrender.com
REACT_APP_DEBUG=false
REACT_APP_ENV=production
REACT_APP_VERSION=1.0.0
```

### Frontend Vercel Config (`frontend/vercel.json`)
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

## Part 4: Deployment Steps

### Step 1: Deploy Backend to Render
1. Ensure all changes are committed and pushed to GitHub
2. Follow Render deployment steps above
3. Wait for deployment to complete
4. Test backend: `curl https://conversational-chatbot.onrender.com/health`

### Step 2: Deploy Frontend to Vercel
1. Navigate to frontend directory: `cd frontend`
2. Deploy: `vercel --prod --name frontend-khaki-sigma`
3. Confirm deployment to `https://frontend-khaki-sigma.vercel.app`
4. Wait for deployment to complete

### Step 3: Verify Connection
1. Open frontend URL in browser
2. Test user registration/login
3. Test chatbot functionality
4. Check browser console for API errors

## Part 5: Expected URLs

### Backend (Render)
- **API Base**: `https://conversational-chatbot.onrender.com`
- **Health Check**: `https://conversational-chatbot.onrender.com/health`
- **Chat API**: `https://conversational-chatbot.onrender.com/api/chat`

### Frontend (Vercel)
- **Primary URL**: `https://frontend-khaki-sigma.vercel.app`

## Part 6: Testing the Full Stack

### 1. Backend Health Check
```bash
curl https://conversational-chatbot.onrender.com/health
# Expected: {"status": "healthy"}
```

### 2. Frontend Accessibility
- Open browser to your Vercel URL
- Should see the Student Technical Support homepage
- Check that logo and styling load correctly

### 3. API Integration Test
- Register a new user account
- Login successfully
- Navigate to chat interface
- Send a test message
- Verify response from backend

## Part 7: Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure Vercel frontend URL is in backend CORS_ORIGINS
   - Check `app.py` CORS configuration

2. **API Connection Failed**
   - Verify `REACT_APP_API_URL` in frontend configuration
   - Check Render backend is running and accessible

3. **Environment Variables**
   - Ensure all required env vars are set in Render dashboard
   - Redeploy after adding environment variables

4. **Build Failures**
   - Check build logs in respective dashboards
   - Verify all dependencies are listed correctly

### Logs and Monitoring
- **Render**: View logs in Render dashboard
- **Vercel**: View deployment logs in Vercel dashboard
- **Frontend**: Use browser developer tools

## Part 8: Auto-Deployment

### Backend (Render)
- Auto-deploys on push to `main` branch
- Configured via GitHub integration

### Frontend (Vercel)
- Auto-deploys on push to `main` branch
- Configured via GitHub integration
- Preview deployments for pull requests

## Summary

This hybrid deployment approach provides:
- **Scalable Backend**: Render's managed Python hosting
- **Fast Frontend**: Vercel's global CDN for React apps
- **Cost Effective**: Free tiers for both platforms
- **Easy Maintenance**: Separate deployment pipelines

Both services will auto-deploy when you push changes to GitHub, making development and maintenance seamless.