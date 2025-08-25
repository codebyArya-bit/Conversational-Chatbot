# 🤖 College IT Support Chatbot - Conversational AI Assistant

A modern web-based chatbot designed to provide 24/7 IT support for college students and staff when technical support personnel are not available. Built with Flask, OpenAI GPT, and FAISS vector search for intelligent FAQ matching.

## 🌟 Features

- **24/7 Availability**: Students can get help anytime, even when IT staff is offline
- **Intelligent Responses**: Uses OpenAI GPT-3.5 for natural, helpful responses
- **FAQ Integration**: FAISS vector search matches user queries with relevant solutions
- **Modern Web Interface**: Responsive design that works on desktop and mobile
- **Session Management**: Maintains chat history during user sessions
- **Quick Questions**: Pre-defined common issues for faster support
- **Real-time Chat**: Instant responses with typing indicators

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Internet connection for AI model downloads

### Installation

1. **Clone or download this repository**
   ```bash
   cd "Conversational Chatbot"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   **Windows (Command Prompt):**
   ```cmd
   set OPENAI_API_KEY=your_api_key_here
   ```
   
   **Windows (PowerShell):**
   ```powershell
   $env:OPENAI_API_KEY="your_api_key_here"
   ```
   
   **Linux/Mac:**
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
Conversational Chatbot/
├── app.py                          # Main Flask application
├── run.py                          # Startup script
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── templates/
│   └── index.html                  # Web interface
├── ICT Cell Common problems - Hardware issues.csv  # FAQ database
├── main.py                         # Original Streamlit version
├── chat_bot_prototype_code.py      # Original prototype
└── README_NEW.md                   # This documentation
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
OPENAI_API_KEY=your_actual_api_key
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

### FAQ Data

The chatbot uses `ICT Cell Common problems - Hardware issues.csv` for its knowledge base. You can:

- **Add new entries**: Edit the CSV file with new Question-Answer pairs
- **Update existing solutions**: Modify answers in the CSV file
- **Replace entirely**: Use your own CSV with 'Question' and 'Answer' columns

## 🏫 College Deployment Guide

### For IT Administrators

1. **Server Requirements**
   - Python 3.8+ environment
   - 2GB RAM minimum (4GB recommended)
   - Internet access for OpenAI API calls
   - SSL certificate for HTTPS (recommended)

2. **Production Deployment**
   ```bash
   # Install production server
   pip install gunicorn
   
   # Run with Gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Nginx Configuration** (Optional)
   ```nginx
   server {
       listen 80;
       server_name your-college-domain.edu;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Customization for Your College

1. **Update Branding**
   - Edit `templates/index.html`
   - Change "KIIT Deemed To Be University" to your college name
   - Update colors and logos as needed

2. **Customize FAQ Data**
   - Replace the CSV file with your college's common IT issues
   - Include college-specific software, systems, and procedures

3. **Modify AI Personality**
   - Edit the system prompt in `app.py` (line ~70)
   - Adjust the assistant's name and personality

## 🔌 API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat` - Send message and get response
- `GET /api/session/<id>/history` - Get chat history
- `GET /api/health` - Health check
- `GET /api/stats` - Usage statistics

## 🛠️ Development

### Running in Development Mode

```bash
# Enable debug mode
set FLASK_ENV=development  # Windows
export FLASK_ENV=development  # Linux/Mac

python run.py
```

### Adding New Features

1. **Backend**: Modify `app.py` for new API endpoints
2. **Frontend**: Update `templates/index.html` for UI changes
3. **Configuration**: Add settings to `config.py`

## 📊 Monitoring and Analytics

- **Usage Stats**: Available at `/api/stats`
- **Health Check**: Monitor `/api/health`
- **Logs**: Check console output for errors and usage

## 🔒 Security Considerations

- **API Keys**: Never commit API keys to version control
- **Rate Limiting**: Built-in protection against spam
- **Input Validation**: Messages are limited and sanitized
- **HTTPS**: Use SSL certificates in production

## 🆘 Troubleshooting

### Common Issues

1. **"OpenAI API key not set"**
   - Ensure OPENAI_API_KEY environment variable is set
   - Check that the API key is valid and has credits

2. **"FAQ data not found"**
   - Verify the CSV file exists in the project directory
   - Check that it has 'Question' and 'Answer' columns

3. **"Port already in use"**
   - Change the port in `run.py` or kill the existing process
   - Use `netstat -ano | findstr :5000` to find the process

4. **Slow responses**
   - Check internet connection
   - Verify OpenAI API status
   - Consider upgrading server resources

### Getting Help

- Check the console output for detailed error messages
- Ensure all dependencies are installed correctly
- Verify Python version compatibility (3.8+)

## 🔄 Migration from Streamlit Version

If you were using the original `main.py` Streamlit version:

1. **Data Migration**: Your CSV file works without changes
2. **API Keys**: Same OpenAI API key can be used
3. **Features**: All original functionality is preserved and enhanced
4. **Performance**: Web version is faster and more scalable

## 📈 Future Enhancements

- **Database Integration**: Store chat history permanently
- **Admin Dashboard**: Manage FAQs through web interface
- **Multi-language Support**: Support for different languages
- **Analytics Dashboard**: Detailed usage and performance metrics
- **Integration**: Connect with college management systems

## 📄 License

This project is designed for educational use in colleges and universities. Feel free to modify and adapt it for your institution's needs.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests to improve the chatbot for the college community.

---

**Made with ❤️ for college communities worldwide**