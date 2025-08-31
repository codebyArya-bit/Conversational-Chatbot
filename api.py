# api.py - Backend API for React Frontend
from __future__ import annotations

import os
import json
import uuid
import logging
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
from functools import wraps

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, skip loading .env file

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    from flask_sqlalchemy import SQLAlchemy
    import jwt
except ImportError as e:
    raise ImportError(f"Required package missing: {e}")

try:
    import numpy as np
    import pandas as pd
except ImportError as e:
    raise ImportError(f"Required package missing: {e}")

# ---- Optional deps & fallbacks ----
try:
    import faiss
    HAVE_FAISS = True
except Exception:
    faiss = None
    HAVE_FAISS = False

try:
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    raise ImportError(f"sentence-transformers is required: {e}")

# OpenRouter API Key for chat functionality
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
CLIENT = None
if OPENROUTER_API_KEY or OPENAI_KEY:
    try:
        from openai import OpenAI
        # Use OpenRouter if available, otherwise fallback to OpenAI
        if OPENROUTER_API_KEY:
            CLIENT = OpenAI(
                api_key=OPENROUTER_API_KEY,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            CLIENT = OpenAI(api_key=OPENAI_KEY)
    except Exception:
        CLIENT = None

# ---- Config ----
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.environ.get("FLASK_SECRET_KEY", "change-this-in-prod")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or SECRET_KEY
    FAQ_CSV_PATH = os.environ.get("FAQ_CSV_PATH", "ICT Cell Common problems - Hardware issues.csv")
    EMB_PATH = os.path.join(".cache", "faq_embeddings.npy")
    Q_PATH = os.path.join(".cache", "faq_questions.json")
    MODEL_NAME = os.environ.get("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    TOP_K = int(os.environ.get("TOP_K", "3"))
    MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "350"))
    CHAT_MODEL = os.environ.get("CHAT_MODEL", "gpt-4o-mini")
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///chatbot.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')

os.makedirs(".cache", exist_ok=True)

# ---- Logging ----
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("tech-edu-hub-api")

# ---- Import models ----
from models import db, User, ChatSession, ChatMessage, DeviceSpec, SupportTicket, AdminUser

# ---- App ----
app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS
CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

# Initialize database
db.init_app(app)

# ---- JWT Helper Functions ----
def generate_token(user_id: int, is_admin: bool = False) -> str:
    """Generate JWT token for user authentication."""
    payload = {
        'user_id': user_id,
        'is_admin': is_admin,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require valid JWT token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Get user from database
        user = User.query.get(payload['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 401
        
        request.current_user = user
        request.is_admin = payload.get('is_admin', False)
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin privileges."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not getattr(request, 'is_admin', False):
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    
    return decorated

# ---- Globals (loaded at start) ----
_embedder: Optional[SentenceTransformer] = None
_questions: List[str] = []
_answers: List[str] = []
_emb_matrix: Optional[np.ndarray] = None
_faiss_index = None

def get_embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        log.info("Loading embedding model: %s", app.config["MODEL_NAME"])
        _embedder = SentenceTransformer(app.config["MODEL_NAME"])
    return _embedder

def _normalize(mat: np.ndarray) -> np.ndarray:
    # L2 normalize for cosine/IP search
    norms = np.linalg.norm(mat, axis=1, keepdims=True) + 1e-12
    return mat / norms

def _build_index(embeddings: np.ndarray):
    """Build FAISS or prepare NumPy fallback."""
    global _faiss_index, _emb_matrix
    _emb_matrix = _normalize(embeddings.astype("float32"))
    if HAVE_FAISS:
        dim = _emb_matrix.shape[1] if _emb_matrix is not None else 0
        if faiss is not None:
            index = faiss.IndexFlatIP(dim)  # cosine via normalized vectors
        else:
            raise ImportError("FAISS is required for vector indexing")
        index.add(_emb_matrix)
        _faiss_index = index
        if _emb_matrix is not None:
            log.info("FAISS index ready: %d vectors (dim=%d)", _emb_matrix.shape[0], dim)
        else:
            log.info("FAISS index ready: vectors (dim=%d)", dim)
    else:
        _faiss_index = None
        log.info("FAISS not available; using NumPy cosine similarity fallback.")

def _search(query: str, k: int) -> Tuple[np.ndarray, np.ndarray]:
    """Return (distances, indices)."""
    k = max(1, min(k, len(_questions)))
    q_emb = get_embedder().encode([query], show_progress_bar=False).astype("float32")
    q_emb = _normalize(q_emb)

    if HAVE_FAISS and _faiss_index is not None:
        D, I = _faiss_index.search(q_emb, k)
        return D[0], I[0]

    # NumPy fallback: cosine similarity
    sims = (_emb_matrix @ q_emb.T).ravel()  # shape (N,)
    idx = np.argpartition(-sims, range(k))[:k]
    idx = idx[np.argsort(-sims[idx])]
    return sims[idx], idx

def _load_or_build_embeddings(qs: List[str]) -> np.ndarray:
    """Load cached embeddings if matching; otherwise compute & cache."""
    # Try to reuse cache only if question list matches previous cache
    if os.path.exists(app.config["EMB_PATH"]) and os.path.exists(app.config["Q_PATH"]):
        try:
            with open(app.config["Q_PATH"], "r", encoding="utf-8") as f:
                cached_qs = json.load(f)
            if cached_qs == qs:
                log.info("Loading cached embeddings...")
                return np.load(app.config["EMB_PATH"])
        except Exception as e:
            log.warning("Cache load failed: %s", e)

    # Compute fresh embeddings
    log.info("Computing embeddings for %d questions...", len(qs))
    embeddings = get_embedder().encode(qs, show_progress_bar=True)
    
    # Cache them
    try:
        np.save(app.config["EMB_PATH"], embeddings)
        with open(app.config["Q_PATH"], "w", encoding="utf-8") as f:
            json.dump(qs, f, ensure_ascii=False, indent=2)
        log.info("Embeddings cached.")
    except Exception as e:
        log.warning("Cache save failed: %s", e)
    
    return embeddings

def load_faq_data() -> bool:
    """Load FAQ data from CSV and build search index."""
    global _questions, _answers
    
    try:
        if not os.path.exists(app.config["FAQ_CSV_PATH"]):
            log.error("FAQ CSV not found: %s", app.config["FAQ_CSV_PATH"])
            return False
        
        df = pd.read_csv(app.config["FAQ_CSV_PATH"])
        log.info("Loaded CSV with columns: %s", list(df.columns))
        
        # Assume columns are 'Question' and 'Answer' or similar
        question_col = None
        answer_col = None
        
        for col in df.columns:
            if 'question' in col.lower() or 'problem' in col.lower():
                question_col = col
            elif 'answer' in col.lower() or 'solution' in col.lower():
                answer_col = col
        
        if question_col is None or answer_col is None:
            log.error("Could not identify question/answer columns in CSV")
            return False
        
        _questions = df[question_col].dropna().astype(str).tolist()
        _answers = df[answer_col].dropna().astype(str).tolist()
        
        # Ensure same length
        min_len = min(len(_questions), len(_answers))
        _questions = _questions[:min_len]
        _answers = _answers[:min_len]
        
        log.info("Loaded %d FAQ pairs", len(_questions))
        
        # Build embeddings and search index
        embeddings = _load_or_build_embeddings(_questions)
        _build_index(embeddings)
        
        return True
        
    except Exception as e:
        log.error("Failed to load FAQ data: %s", e)
        return False

def get_chatbot_response(user_message: str) -> str:
    """Generate chatbot response using FAQ search + OpenAI."""
    try:
        # Search FAQ
        if len(_questions) == 0:
            faq_context = "No FAQ data available."
        else:
            distances, indices = _search(user_message, app.config["TOP_K"])
            faq_pairs = []
            for i, idx in enumerate(indices):
                if idx < len(_questions) and idx < len(_answers):
                    faq_pairs.append(f"Q: {_questions[idx]}\nA: {_answers[idx]}")
            faq_context = "\n\n".join(faq_pairs)
        
        # Generate response with OpenAI
        if CLIENT is None:
            return f"I found some relevant information:\n\n{faq_context}"
        
        system_prompt = f"""You are a helpful technical support assistant for students. 
Use the following FAQ information to answer the user's question. 
If the FAQ doesn't contain relevant information, provide general helpful guidance.

FAQ Information:
{faq_context}

Provide clear, concise, and helpful responses. If you're referencing the FAQ, mention that."""
        
        response = CLIENT.chat.completions.create(
            model=app.config["CHAT_MODEL"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=app.config["MAX_TOKENS"],
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        log.error("Chatbot response error: %s", e)
        return "I apologize, but I'm having trouble processing your request right now. Please try again later."

# ---- API Routes ----

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'faq_loaded': len(_questions) > 0,
        'total_faqs': len(_questions),
        'openai_available': CLIENT is not None,
        'faiss_available': HAVE_FAISS
    })

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration endpoint."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Validation
        if not username or len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters long'}), 400
        
        if not email or '@' not in email:
            return jsonify({'error': 'Valid email is required'}), 400
        
        if not password or len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = generate_token(user.id)
        
        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': False
            }
        }), 201
        
    except Exception as e:
        log.error("Registration error: %s", e)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Check regular user first
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            token = generate_token(user.id)
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_admin': False
                }
            })
        
        # Check admin user
        admin = AdminUser.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            token = generate_token(admin.id, is_admin=True)
            return jsonify({
                'message': 'Admin login successful',
                'token': token,
                'user': {
                    'id': admin.id,
                    'username': admin.username,
                    'email': admin.email,
                    'is_admin': True
                }
            })
        
        return jsonify({'error': 'Invalid username or password'}), 401
        
    except Exception as e:
        log.error("Login error: %s", e)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/auth/verify', methods=['GET'])
@token_required
def verify_token_endpoint():
    """Verify token and return user info."""
    user = request.current_user
    return jsonify({
        'valid': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': getattr(request, 'is_admin', False)
        }
    })

# Chat routes
@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint with session management."""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get session ID
        session_id = data.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Get user if authenticated
        user_id = None
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            payload = verify_token(token[7:])
            if payload:
                user_id = payload['user_id']
        
        # Get or create chat session
        chat_session = ChatSession.query.filter_by(session_id=session_id).first()
        if not chat_session:
            chat_session = ChatSession(
                session_id=session_id,
                user_id=user_id,
                title=user_message[:100] + '...' if len(user_message) > 100 else user_message
            )
            db.session.add(chat_session)
            db.session.commit()
        
        # Save user message
        user_msg = ChatMessage(
            session_id=chat_session.id,
            message_type='user',
            content=user_message
        )
        db.session.add(user_msg)
        
        # Get chatbot response
        bot_response = get_chatbot_response(user_message)
        
        # Save bot response
        bot_msg = ChatMessage(
            session_id=chat_session.id,
            message_type='bot',
            content=bot_response,
            faq_matched=True if 'FAQ' in bot_response else False
        )
        db.session.add(bot_msg)
        
        # Update session timestamp
        chat_session.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'response': bot_response,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'user_authenticated': user_id is not None
        })
    
    except Exception as e:
        log.error("Chat error: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/chat/history', methods=['GET'])
@token_required
def chat_history():
    """Get user's chat history."""
    try:
        user = request.current_user
        sessions = ChatSession.query.filter_by(user_id=user.id).order_by(ChatSession.updated_at.desc()).all()
        
        history = []
        for session in sessions:
            history.append({
                'id': session.id,
                'session_id': session.session_id,
                'title': session.title,
                'created_at': session.created_at.isoformat(),
                'updated_at': session.updated_at.isoformat()
            })
        
        return jsonify({'history': history})
        
    except Exception as e:
        log.error("Chat history error: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/chat/session/<session_id>', methods=['GET'])
@token_required
def get_chat_session(session_id):
    """Get messages for a specific chat session."""
    try:
        user = request.current_user
        chat_session = ChatSession.query.filter_by(session_id=session_id, user_id=user.id).first()
        
        if not chat_session:
            return jsonify({'error': 'Session not found'}), 404
        
        messages = ChatMessage.query.filter_by(session_id=chat_session.id).order_by(ChatMessage.timestamp.asc()).all()
        
        message_list = []
        for msg in messages:
            message_list.append({
                'id': msg.id,
                'type': msg.message_type,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat(),
                'faq_matched': msg.faq_matched
            })
        
        return jsonify({
            'session': {
                'id': chat_session.id,
                'session_id': chat_session.session_id,
                'title': chat_session.title,
                'created_at': chat_session.created_at.isoformat(),
                'updated_at': chat_session.updated_at.isoformat()
            },
            'messages': message_list
        })
        
    except Exception as e:
        log.error("Get chat session error: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500

# Device management routes
@app.route('/api/devices', methods=['GET'])
@token_required
def get_devices():
    """Get user's devices."""
    try:
        user = request.current_user
        devices = DeviceSpec.query.filter_by(user_id=user.id).all()
        
        device_list = []
        for device in devices:
            device_list.append({
                'id': device.id,
                'device_name': device.device_name,
                'device_type': device.device_type,
                'operating_system': device.operating_system,
                'processor': device.processor,
                'ram': device.ram,
                'storage': device.storage,
                'graphics_card': device.graphics_card,
                'network_adapter': device.network_adapter,
                'other_specs': device.other_specs,
                'is_primary': device.is_primary,
                'created_at': device.created_at.isoformat() if device.created_at else None
            })
        
        return jsonify({'devices': device_list})
        
    except Exception as e:
        log.error("Get devices error: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/devices', methods=['POST'])
@token_required
def create_device():
    """Create a new device specification."""
    try:
        user = request.current_user
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        device_name = data.get('device_name', '').strip()
        if not device_name:
            return jsonify({'error': 'Device name is required'}), 400
        
        # If this is set as primary, unset other primary devices
        if data.get('is_primary', False):
            DeviceSpec.query.filter_by(user_id=user.id, is_primary=True).update({'is_primary': False})
        
        device = DeviceSpec(
            user_id=user.id,
            device_name=device_name,
            device_type=data.get('device_type', 'laptop'),
            operating_system=data.get('operating_system', ''),
            processor=data.get('processor', ''),
            ram=data.get('ram', ''),
            storage=data.get('storage', ''),
            graphics_card=data.get('graphics_card', ''),
            network_adapter=data.get('network_adapter', ''),
            other_specs=data.get('other_specs', ''),
            is_primary=data.get('is_primary', False)
        )
        
        db.session.add(device)
        db.session.commit()
        
        return jsonify({
            'message': 'Device created successfully',
            'device': {
                'id': device.id,
                'device_name': device.device_name,
                'device_type': device.device_type,
                'is_primary': device.is_primary
            }
        }), 201
        
    except Exception as e:
        log.error("Create device error: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
@token_required
def delete_device(device_id):
    """Delete a device specification."""
    try:
        user = request.current_user
        device = DeviceSpec.query.filter_by(id=device_id, user_id=user.id).first()
        
        if not device:
            return jsonify({'error': 'Device not found'}), 404
        
        db.session.delete(device)
        db.session.commit()
        
        return jsonify({'message': 'Device deleted successfully'})
        
    except Exception as e:
        log.error("Delete device error: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500

# Support ticket routes
@app.route('/api/support/tickets', methods=['GET'])
@token_required
def get_tickets():
    """Get user's support tickets."""
    try:
        user = request.current_user
        tickets = SupportTicket.query.filter_by(user_id=user.id).order_by(SupportTicket.created_at.desc()).all()
        
        ticket_list = []
        for ticket in tickets:
            ticket_list.append({
                'id': ticket.id,
                'ticket_number': ticket.ticket_number,
                'title': ticket.title,
                'description': ticket.description,
                'category': ticket.category,
                'priority': ticket.priority,
                'status': ticket.status,
                'admin_response': ticket.admin_response,
                'created_at': ticket.created_at.isoformat(),
                'updated_at': ticket.updated_at.isoformat(),
                'resolved_at': ticket.resolved_at.isoformat() if ticket.resolved_at else None
            })
        
        return jsonify({'tickets': ticket_list})
        
    except Exception as e:
        log.error("Get tickets error: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/support/tickets', methods=['POST'])
@token_required
def create_ticket():
    """Create a new support ticket."""
    try:
        user = request.current_user
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        
        if not description:
            return jsonify({'error': 'Description is required'}), 400
        
        # Get user's primary device info
        primary_device = DeviceSpec.query.filter_by(user_id=user.id, is_primary=True).first()
        device_info = None
        if primary_device:
            device_info = {
                'device_name': primary_device.device_name,
                'device_type': primary_device.device_type,
                'operating_system': primary_device.operating_system,
                'processor': primary_device.processor,
                'ram': primary_device.ram,
                'storage': primary_device.storage
            }
        
        ticket = SupportTicket(
            user_id=user.id,
            title=title,
            description=description,
            category=data.get('category', 'general'),
            priority=data.get('priority', 'medium'),
            device_info=json.dumps(device_info) if device_info else None
        )
        ticket.ticket_number = ticket.generate_ticket_number()
        
        db.session.add(ticket)
        db.session.commit()
        
        return jsonify({
            'message': f'Support ticket {ticket.ticket_number} created successfully',
            'ticket': {
                'id': ticket.id,
                'ticket_number': ticket.ticket_number,
                'title': ticket.title,
                'status': ticket.status
            }
        }), 201
        
    except Exception as e:
        log.error("Create ticket error: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500

# Admin routes
@app.route('/api/admin/tickets', methods=['GET'])
@token_required
@admin_required
def admin_get_tickets():
    """Get all support tickets for admin."""
    try:
        status_filter = request.args.get('status', 'all')
        priority_filter = request.args.get('priority', 'all')
        
        query = SupportTicket.query
        
        if status_filter != 'all':
            query = query.filter_by(status=status_filter)
        
        if priority_filter != 'all':
            query = query.filter_by(priority=priority_filter)
        
        tickets = query.order_by(SupportTicket.created_at.desc()).all()
        
        ticket_list = []
        for ticket in tickets:
            # Get user info
            user = User.query.get(ticket.user_id)
            
            ticket_list.append({
                'id': ticket.id,
                'ticket_number': ticket.ticket_number,
                'title': ticket.title,
                'description': ticket.description,
                'category': ticket.category,
                'priority': ticket.priority,
                'status': ticket.status,
                'admin_response': ticket.admin_response,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                } if user else None,
                'device_info': json.loads(ticket.device_info) if ticket.device_info else None,
                'created_at': ticket.created_at.isoformat(),
                'updated_at': ticket.updated_at.isoformat(),
                'resolved_at': ticket.resolved_at.isoformat() if ticket.resolved_at else None
            })
        
        return jsonify({'tickets': ticket_list})
        
    except Exception as e:
        log.error("Admin get tickets error: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/admin/tickets/<int:ticket_id>', methods=['PUT'])
@token_required
@admin_required
def admin_update_ticket(ticket_id):
    """Update a support ticket as admin."""
    try:
        ticket = SupportTicket.query.get_or_404(ticket_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update ticket fields
        if 'status' in data:
            ticket.status = data['status']
        
        if 'admin_response' in data:
            ticket.admin_response = data['admin_response']
        
        if 'assigned_to_id' in data:
            ticket.assigned_to_id = data['assigned_to_id']
        
        ticket.updated_at = datetime.utcnow()
        
        if data.get('status') == 'resolved':
            ticket.resolved_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'message': 'Ticket updated successfully'})
        
    except Exception as e:
        log.error("Admin update ticket error: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Load FAQ data on startup
    if load_faq_data():
        log.info("FAQ data loaded successfully")
    else:
        log.warning("Warning: Could not load FAQ data")
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)