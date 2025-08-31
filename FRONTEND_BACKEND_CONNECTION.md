# Frontend-Backend Connection Guide

## 🔗 Connecting React Frontend to Render Backend

This guide explains how to configure your React frontend to connect to the deployed Flask backend on Render.

## 📋 Current Configuration

### Backend API Service
- **Current Default**: `https://student-chatbot-ap9p.onrender.com`
- **Your New Backend**: `https://conversational-chatbot-XXXX.onrender.com` (after deployment)

### Frontend Configuration Files

#### 1. Environment Variables
**File**: `frontend/.env.production`
```env
# Production environment variables for Render deployment
# Update this URL with your actual Render backend URL after deployment
# Format: https://conversational-chatbot-XXXX.onrender.com
REACT_APP_API_URL=https://conversational-chatbot-XXXX.onrender.com
REACT_APP_DEBUG=false
REACT_APP_ENV=production
REACT_APP_VERSION=1.0.0
```

#### 2. API Service Configuration
**File**: `frontend/src/services/api.ts`
```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://student-chatbot-ap9p.onrender.com';
```

#### 3. Deployment Configurations

**Render Blueprint** (`render.yaml`):
```yaml
services:
  - type: static
    name: chatbot-frontend
    buildCommand: cd frontend && npm ci && npm run build
    staticPublishPath: ./frontend/build
    envVars:
      - key: REACT_APP_API_URL
        value: https://conversational-chatbot-XXXX.onrender.com
```

**Netlify** (`netlify.toml`):
```toml
[build.environment]
  REACT_APP_API_URL = "https://conversational-chatbot-XXXX.onrender.com"
```

## 🚀 Step-by-Step Connection Process

### Step 1: Deploy Backend to Render
1. Follow the instructions in `RENDER_MANUAL_DEPLOYMENT.md`
2. Deploy using the Render dashboard with the `render.yaml` blueprint
3. Note your backend URL: `https://conversational-chatbot-XXXX.onrender.com`

### Step 2: Update Frontend Configuration

#### Option A: Update Environment Files
1. **Update `.env.production`**:
   ```bash
   # Replace XXXX with your actual service ID
   REACT_APP_API_URL=https://conversational-chatbot-abc123.onrender.com
   ```

2. **Update `render.yaml`** (if deploying frontend to Render):
   ```yaml
   envVars:
     - key: REACT_APP_API_URL
       value: https://conversational-chatbot-abc123.onrender.com
   ```

3. **Update `netlify.toml`** (if deploying frontend to Netlify):
   ```toml
   REACT_APP_API_URL = "https://conversational-chatbot-abc123.onrender.com"
   ```

#### Option B: Direct API Configuration Update
If you prefer to hardcode the URL:

**File**: `frontend/src/services/api.ts`
```typescript
// Replace with your actual backend URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://conversational-chatbot-abc123.onrender.com';
```

### Step 3: Test Backend Connection

#### Health Check
Test your backend is running:
```bash
curl https://conversational-chatbot-abc123.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

#### API Endpoints
Verify these endpoints are accessible:
- **Health**: `GET /api/health`
- **Chat**: `POST /api/chat`
- **Auth**: `POST /auth/login`, `POST /auth/register`
- **Stats**: `GET /api/stats`

### Step 4: Deploy Frontend

#### Option A: Deploy to Render (Full-Stack)
1. Push updated configuration to GitHub
2. Use the `render.yaml` blueprint to deploy both services
3. Frontend will be available at: `https://chatbot-frontend-XXXX.onrender.com`

#### Option B: Deploy to Netlify (Frontend Only)
1. Connect your GitHub repository to Netlify
2. Set build command: `cd frontend && npm run build`
3. Set publish directory: `frontend/build`
4. Frontend will be available at: `https://your-app-name.netlify.app`

#### Option C: Deploy to Vercel (Frontend Only)
1. Connect your GitHub repository to Vercel
2. Set root directory: `frontend`
3. Frontend will be available at: `https://your-app-name.vercel.app`

### Step 5: Verify Full-Stack Connection

#### Test Authentication
1. Visit your frontend URL
2. Try to register a new account
3. Login with the account
4. Check browser network tab for API calls

#### Test Chat Functionality
1. Navigate to the Chat page
2. Send a test message
3. Verify you receive a response from the backend
4. Check chat history is saved

#### Test Device Management
1. Go to Device Specs page
2. Add a new device specification
3. Verify it's saved and displayed

## 🔧 Troubleshooting

### Common Issues

#### 1. CORS Errors
**Problem**: Frontend can't connect to backend due to CORS policy

**Solution**: Verify backend CORS configuration in `app.py`:
```python
from flask_cors import CORS

# Allow your frontend domain
CORS(app, origins=['https://your-frontend-domain.com'])
```

#### 2. Environment Variables Not Loading
**Problem**: `REACT_APP_API_URL` is undefined

**Solutions**:
- Ensure variable starts with `REACT_APP_`
- Restart development server after changing `.env` files
- Check deployment platform environment variable settings

#### 3. API Endpoints Not Found (404)
**Problem**: Frontend gets 404 errors for API calls

**Solutions**:
- Verify backend is deployed and running
- Check API endpoint paths match frontend calls
- Ensure backend health check passes

#### 4. Authentication Issues
**Problem**: Login/register not working

**Solutions**:
- Check JWT token handling in frontend
- Verify backend authentication endpoints
- Check browser localStorage for token storage

### Debug Steps

1. **Check Backend Status**:
   ```bash
   curl https://your-backend-url.onrender.com/api/health
   ```

2. **Check Frontend Environment**:
   ```javascript
   console.log('API URL:', process.env.REACT_APP_API_URL);
   ```

3. **Monitor Network Requests**:
   - Open browser DevTools → Network tab
   - Perform actions and check API calls
   - Look for failed requests or CORS errors

4. **Check Backend Logs**:
   - Go to Render dashboard
   - View your service logs
   - Look for error messages or failed requests

## 🎯 Expected Result

After successful configuration:

✅ **Frontend Features Working**:
- User registration and login
- AI-powered chat functionality
- Device specification management
- Support ticket system
- Chat history tracking
- Admin dashboard (for admin users)

✅ **Backend Integration**:
- All API endpoints responding
- Database operations working
- Authentication flow complete
- Real-time chat responses

✅ **Production Deployment**:
- Frontend accessible via public URL
- Backend API accessible and secure
- Environment variables properly configured
- CORS policies correctly set

---

**🎉 Your full-stack Student Chatbot application will be live and fully functional!**

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review deployment logs in your platform dashboard
3. Verify all environment variables are set correctly
4. Test API endpoints individually before testing the full application