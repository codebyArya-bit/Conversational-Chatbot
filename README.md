# TechEdu Hub - AI-Powered Educational Chatbot 🎓

A comprehensive web platform that combines IT support, educational resources, and an intelligent AI chatbot to help students with technical issues and academic questions.

![TechEdu Hub](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![AI](https://img.shields.io/badge/AI-Powered-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

- **🤖 AI-Powered Chatbot**: Intelligent assistant using sentence transformers and FAISS for semantic search
- **📚 Educational Resources**: Comprehensive learning materials covering networking, databases, programming, and cybersecurity
- **🎨 Modern UI/UX**: Responsive design with smooth animations and intuitive navigation
- **⚡ Real-time Chat**: Interactive chatbot with typing indicators and quick question buttons
- **📱 Mobile Responsive**: Optimized for all devices and screen sizes
- **🔍 Semantic Search**: Advanced FAQ matching using machine learning embeddings
- **🎯 Student-Focused**: Designed specifically for educational environments

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/techedu-hub.git
   cd techedu-hub
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env file and add your OpenAI API key (optional for demo)
   OPENAI_API_KEY=your_openai_api_key_here
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the application**
   
   Open your browser and navigate to: `http://localhost:5000`

## 📁 Project Structure

```
techedu-hub/
├── app.py                 # Main Flask application
├── run.py                 # Application runner
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── index.html        # Homepage
│   ├── about.html        # About page
│   ├── services.html     # Services page
│   ├── resources.html    # Resources page
│   └── contact.html      # Contact page
├── .cache/               # Cached embeddings and data
│   ├── faq_embeddings.npy
│   └── faq_questions.json
└── ICT Cell Common problems - Hardware issues.csv  # FAQ dataset
```

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **AI/ML**: 
  - Sentence Transformers (for text embeddings)
  - FAISS (for similarity search)
  - OpenAI API (optional integration)
- **Frontend**: 
  - HTML5, CSS3, JavaScript
  - Font Awesome icons
  - Google Fonts
- **Data Processing**: Pandas, NumPy
- **Environment**: Python-dotenv for configuration

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# OpenAI API Key (optional - for enhanced AI responses)
OPENAI_API_KEY=your_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### FAQ Dataset

The application uses `ICT Cell Common problems - Hardware issues.csv` for the knowledge base. You can:

- Replace this file with your own FAQ dataset
- Ensure the CSV has columns for questions and answers
- The system will automatically generate embeddings for semantic search

## 🎯 Usage

### For Students

1. **Homepage**: Browse educational content and features
2. **AI Assistant**: Click "Try AI Assistant" to start chatting
3. **Quick Questions**: Use pre-defined buttons for common issues
4. **Learning Resources**: Explore theories and educational materials
5. **Navigation**: Use the top menu to access different sections

### For Developers

1. **API Endpoints**:
   - `POST /api/chat` - Send messages to the chatbot
   - `GET /` - Homepage
   - `GET /about` - About page
   - `GET /services` - Services page
   - `GET /resources` - Resources page
   - `GET /contact` - Contact page

2. **Customization**:
   - Modify templates in the `templates/` directory
   - Update FAQ data in the CSV file
   - Customize styling in the HTML templates
   - Add new routes in `app.py`

## 🚀 Deployment

### Local Development

```bash
# Run with debug mode
python run.py

# Or use Flask CLI
flask --app app run --debug
```

### Production Deployment

1. **Using Gunicorn** (recommended for production):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Using Docker** (create Dockerfile):
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**:
   - Ensure virtual environment is activated
   - Install all dependencies: `pip install -r requirements.txt`

2. **Port Already in Use**:
   - Change port in `run.py` or kill the process using port 5000

3. **Missing Dependencies**:
   - Update pip: `python -m pip install --upgrade pip`
   - Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

4. **Slow Initial Load**:
   - First run downloads ML models (sentence transformers)
   - Subsequent runs will be faster due to caching

### Performance Optimization

- The application caches embeddings in `.cache/` directory
- First-time setup may take longer due to model downloads
- Consider using a production WSGI server for better performance

## 📞 Support

For support and questions:

- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

## 🙏 Acknowledgments

- Sentence Transformers for semantic search capabilities
- FAISS for efficient similarity search
- Flask community for the excellent web framework
- Font Awesome for beautiful icons
- Google Fonts for typography

---

**Made with ❤️ for students and educators**

*TechEdu Hub - Empowering learning through AI and technology*
