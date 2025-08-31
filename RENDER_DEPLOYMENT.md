# Render Deployment Guide

This guide explains how to deploy both the backend Flask API and frontend React application to Render.

## Prerequisites

1. Create a [Render account](https://render.com)
2. Connect your GitHub repository to Render
3. Ensure your code is pushed to GitHub

## Deployment Steps

### Option 1: Deploy Using render.yaml (Recommended)

1. **Push your code to GitHub** with the `render.yaml` file in the root directory

2. **Create a new Blueprint on Render:**
   - Go to your Render dashboard
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file
   - Click "Apply" to deploy both services

3. **Set Environment Variables:**
   - The backend service will need:
     - `OPENROUTER_API_KEY`: Your OpenRouter API key
     - `FLASK_ENV`: Set to `production`
     - `SECRET_KEY`: Will be auto-generated

### Option 2: Deploy Services Individually

#### Backend Deployment

1. **Create a new Web Service:**
   - Go to Render dashboard → "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `conversational-chatbot`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python app.py`
     - **Root Directory**: Leave empty (root of repo)

2. **Set Environment Variables:**
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: Generate a secure random string

3. **Add Persistent Disk:**
   - Name: `chatbot-disk`
   - Mount Path: `/opt/render/project/src/instance`
   - Size: 1 GB

#### Frontend Deployment

1. **Create a new Static Site:**
   - Go to Render dashboard → "New" → "Static Site"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `chatbot-frontend`
     - **Build Command**: `cd frontend && npm ci && npm run build`
     - **Publish Directory**: `frontend/build`
     - **Root Directory**: Leave empty

2. **Set Environment Variables:**
   - `REACT_APP_API_URL`: `https://conversational-chatbot.onrender.com` (your backend URL)

## Configuration Files

### render.yaml
The `render.yaml` file in the root directory contains the complete configuration for both services.

### Frontend Environment
The frontend uses `.env.production` for production environment variables.

## Deployment URLs

After successful deployment:
- **Backend API**: `https://conversational-chatbot.onrender.com`
- **Frontend**: `https://chatbot-frontend.onrender.com`

## Troubleshooting

### Common Issues

1. **Build Failures:**
   - Check the build logs in Render dashboard
   - Ensure all dependencies are listed in `package.json` and `requirements.txt`
   - Verify Node.js version compatibility

2. **API Connection Issues:**
   - Verify `REACT_APP_API_URL` points to the correct backend URL
   - Check CORS configuration in the Flask backend
   - Ensure backend is running and accessible

3. **Database Issues:**
   - Verify persistent disk is properly mounted
   - Check database initialization in the Flask app

### Logs and Monitoring

- Access logs through Render dashboard
- Monitor service health and performance
- Set up alerts for service downtime

## Environment Variables Summary

### Backend (`conversational-chatbot`)
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `FLASK_ENV`: `production`
- `SECRET_KEY`: Auto-generated secure key

### Frontend (`chatbot-frontend`)
- `REACT_APP_API_URL`: Backend service URL
- `REACT_APP_DEBUG`: `false`

## Notes

- Render free tier has limitations (services sleep after inactivity)
- Consider upgrading to paid plans for production use
- Both services will have HTTPS enabled automatically
- Database data persists with the mounted disk