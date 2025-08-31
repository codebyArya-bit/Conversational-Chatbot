# app.py
from __future__ import annotations

import os
import json
import uuid
import logging
from datetime import datetime
from typing import List, Tuple, Optional

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, skip loading .env file

try:
    try:
        from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session  # type: ignore
    except ImportError:
        raise ImportError("Flask is required. Install with: pip install flask")
except ImportError:
    raise ImportError("Flask is required. Install with: pip install flask")
try:
    from flask_cors import CORS  # type: ignore
except ImportError:
    raise ImportError("Flask-CORS is required. Install with: pip install flask-cors")
try:
    from flask_login import LoginManager, login_user, logout_user, login_required, current_user  # type: ignore
except ImportError:
    raise ImportError("Flask-Login is required. Install with: pip install flask-login")
try:
    from flask_sqlalchemy import SQLAlchemy  # type: ignore
except ImportError:
    raise ImportError("Flask-SQLAlchemy is required. Install with: pip install flask-sqlalchemy")

try:
    try:
        import numpy as np  # type: ignore
    except ImportError:
        raise ImportError("NumPy is required. Install with: pip install numpy")
except ImportError:
    raise ImportError("NumPy is required. Install with: pip install numpy")
try:
    try:
        import pandas as pd  # type: ignore
    except ImportError:
        raise ImportError("Pandas is required. Install with: pip install pandas")
except ImportError:
    raise ImportError("Pandas is required. Install with: pip install pandas")

# ---- Optional deps & fallbacks ----
try:
    import faiss  # type: ignore
    HAVE_FAISS = True
except Exception:
    faiss = None  # type: ignore
    HAVE_FAISS = False

try:
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
    except ImportError:
        raise ImportError("sentence-transformers is required. Install with: pip install sentence-transformers")
except Exception as e:
    raise RuntimeError(
        "sentence-transformers is required. Install with: pip install sentence-transformers"
    ) from e

# OpenRouter API Key for chat functionality
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
CLIENT = None
if OPENROUTER_API_KEY or OPENAI_KEY:
    try:
        try:
            from openai import OpenAI  # type: ignore
        except ImportError:
            raise ImportError("OpenAI is required. Install with: pip install openai")
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
    FAQ_CSV_PATH = os.environ.get("FAQ_CSV_PATH", "ICT Cell Common problems - Hardware issues.csv")
    EMB_PATH = os.path.join(".cache", "faq_embeddings.npy")
    Q_PATH = os.path.join(".cache", "faq_questions.json")
    MODEL_NAME = os.environ.get("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    TOP_K = int(os.environ.get("TOP_K", "3"))
    MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "350"))
    CHAT_MODEL = os.environ.get("CHAT_MODEL", "gpt-4o-mini")  # keep cheap & available
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///chatbot.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

os.makedirs(".cache", exist_ok=True)

# ---- Logging ----
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("tech-edu-hub")

# ---- Import models and forms ----
from models import db, User, ChatSession, ChatMessage, DeviceSpec, SupportTicket, AdminUser
from forms import LoginForm, RegistrationForm, DeviceSpecForm, SupportTicketForm, ChatFeedbackForm, AdminLoginForm, TicketUpdateForm

# ---- App ----
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]
CORS(app)

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---- Globals (loaded at start) ----
_embedder: Optional[SentenceTransformer] = None
_questions: List[str] = []
_answers: List[str] = []
_emb_matrix: Optional[np.ndarray] = None
_faiss_index = None  # type: ignore


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
            cached_qs = json.load(open(app.config["Q_PATH"], "r", encoding="utf-8"))
            if cached_qs == qs:
                emb = np.load(app.config["EMB_PATH"])
                log.info("Loaded cached embeddings: %s", app.config["EMB_PATH"])
                return emb
        except Exception:
            pass

    log.info("Computing embeddings for %d FAQs…", len(qs))
    emb = get_embedder().encode(qs, show_progress_bar=False).astype("float32")
    np.save(app.config["EMB_PATH"], emb)
    json.dump(qs, open(app.config["Q_PATH"], "w", encoding="utf-8"))
    log.info("Embeddings cached to .cache/")
    return emb


def load_faq_data() -> bool:
    """Load CSV and build index."""
    global _questions, _answers, _emb_matrix

    try:
        df = pd.read_csv(app.config["FAQ_CSV_PATH"])
    except Exception as e:
        log.error("Failed to read CSV at '%s': %s", app.config["FAQ_CSV_PATH"], e)
        return False

    required = {"Question", "Answer"}
    if not required.issubset(df.columns):
        log.error("CSV must contain columns %s", required)
        return False

    _questions = df["Question"].astype(str).fillna("").tolist()
    _answers = df["Answer"].astype(str).fillna("").tolist()

    if not _questions:
        log.warning("No FAQs found in CSV.")
        return False
    emb = _load_or_build_embeddings(_questions)
    _build_index(emb)
    log.info("Loaded %d FAQ entries.", len(_questions))
    return True


def _gen_llm_reply(query: str, context_qas: List[Tuple[str, str]]) -> str:
    """Call OpenAI if configured; otherwise return the top FAQ answer."""
    if CLIENT is None:
        # No API key – return top match answer directly (still useful).
        return context_qas[0][1]
    
    context = "\n\n".join(
        [f"Question: {q}\nAnswer: {a}" for (q, a) in context_qas]
    )
    
    try:
        completion = CLIENT.chat.completions.create(
            model=app.config["CHAT_MODEL"],
            temperature=0.7,
            max_tokens=app.config["MAX_TOKENS"],
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are StudyBot, a helpful IT support assistant for TechEdu Hub. "
                        "Your role is to help students and staff with technical issues. "
                        f"Use this knowledge base: {context}. "
                        "Be friendly, helpful, and provide step-by-step solutions. "
                        "Keep responses concise but informative. "
                        "If you don't know something, suggest contacting the ICT Cell directly."
                    )
                },
                {"role": "user", "content": query}
            ]
        )
        return completion.choices[0].message.content or "Sorry, I couldn't generate a response."
    except Exception as e:
        log.error("OpenAI API error: %s", e)
        return context_qas[0][1]  # fallback to direct answer


def get_chatbot_response(query: str) -> str:
    """Main chatbot response function."""
    if not _questions:
        return "Sorry, the knowledge base is not available right now."
    
    try:
        scores, indices = _search(query, app.config["TOP_K"])
        context_qas = [(_questions[i], _answers[i]) for i in indices]
        return _gen_llm_reply(query, context_qas)
    except Exception as e:
        log.error("Error generating response: %s", e)
        return "I'm sorry, I'm having trouble processing your request right now. Please try again later."


# ---- Routes ----
@app.route('/')
def home():
    """Render the main chatbot interface"""
    return render_template('index.html')


@app.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html')


@app.route('/services')
def services():
    """Render the services page"""
    return render_template('services.html')


@app.route('/resources')
def resources():
    """Render the resources page"""
    return render_template('resources.html')


@app.route('/contact')
def contact():
    """Render the contact page"""
    return render_template('contact.html')


# ---- Authentication Routes ----
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('home')
            flash('Login successful!', 'success')
            return redirect(next_page)
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.email.data)
        ).first()
        
        if existing_user:
            if existing_user.username == form.username.data:
                flash('Username already exists. Please choose a different one.', 'error')
            else:
                flash('Email already registered. Please use a different email.', 'error')
            return render_template('auth/register.html', form=form)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            student_id=form.student_id.data if form.student_id.data else None,
            department=form.department.data if form.department.data else None,
            year_of_study=form.year_of_study.data if form.year_of_study.data else None,
            phone_number=form.phone_number.data if form.phone_number.data else None
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# ---- User Profile and Device Management ----
@app.route('/profile')
@login_required
def profile():
    """User profile page."""
    user_devices = DeviceSpec.query.filter_by(user_id=current_user.id).all()
    user_tickets = SupportTicket.query.filter_by(user_id=current_user.id).order_by(SupportTicket.created_at.desc()).all()
    chat_sessions = ChatSession.query.filter_by(user_id=current_user.id).order_by(ChatSession.updated_at.desc()).limit(10).all()
    
    return render_template('user/profile.html', 
                         user=current_user, 
                         devices=user_devices, 
                         tickets=user_tickets,
                         chat_sessions=chat_sessions)

@app.route('/device-specs', methods=['GET', 'POST'])
@login_required
def device_specs():
    """Device specifications management."""
    form = DeviceSpecForm()
    
    if form.validate_on_submit():
        # If this is set as primary, unset other primary devices
        if form.is_primary.data:
            DeviceSpec.query.filter_by(user_id=current_user.id, is_primary=True).update({'is_primary': False})
        
        device = DeviceSpec(
            user_id=current_user.id,
            device_name=form.device_name.data,
            device_type=form.device_type.data,
            operating_system=form.operating_system.data,
            processor=form.processor.data,
            ram=form.ram.data,
            storage=form.storage.data,
            graphics_card=form.graphics_card.data,
            network_adapter=form.network_adapter.data,
            other_specs=form.other_specs.data,
            is_primary=form.is_primary.data
        )
        
        db.session.add(device)
        db.session.commit()
        
        flash('Device specifications saved successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('user/device_specs.html', form=form)

@app.route('/chat-history')
@login_required
def chat_history():
    """User chat history."""
    sessions = ChatSession.query.filter_by(user_id=current_user.id).order_by(ChatSession.updated_at.desc()).all()
    return render_template('user/chat_history.html', sessions=sessions)

@app.route('/chat-session/<int:session_id>')
@login_required
def view_chat_session(session_id):
    """View specific chat session."""
    chat_session = ChatSession.query.filter_by(id=session_id, user_id=current_user.id).first_or_404()
    messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.timestamp.asc()).all()
    return render_template('user/chat_session.html', session=chat_session, messages=messages)

# ---- Support Ticket Management ----
@app.route('/create-ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    """Create support ticket."""
    form = SupportTicketForm()
    
    if form.validate_on_submit():
        # Get user's primary device info
        primary_device = DeviceSpec.query.filter_by(user_id=current_user.id, is_primary=True).first()
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
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            priority=form.priority.data,
            device_info=json.dumps(device_info) if device_info else None
        )
        ticket.ticket_number = ticket.generate_ticket_number()
        
        db.session.add(ticket)
        db.session.commit()
        
        flash(f'Support ticket {ticket.ticket_number} created successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('user/create_ticket.html', form=form)

@app.route('/api/escalate-chat', methods=['POST'])
@login_required
def escalate_chat():
    """Escalate chat session to support ticket."""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        issue_description = data.get('description', '')
        
        if not session_id:
            return jsonify({'error': 'Session ID required'}), 400
        
        chat_session = ChatSession.query.filter_by(session_id=session_id, user_id=current_user.id).first()
        if not chat_session:
            return jsonify({'error': 'Chat session not found'}), 404
        
        # Get chat messages for context
        messages = ChatMessage.query.filter_by(session_id=chat_session.id).order_by(ChatMessage.timestamp.asc()).all()
        chat_context = '\n'.join([f"{msg.message_type.upper()}: {msg.content}" for msg in messages])
        
        # Get user's primary device info
        primary_device = DeviceSpec.query.filter_by(user_id=current_user.id, is_primary=True).first()
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
        
        # Create support ticket
        ticket = SupportTicket(
            user_id=current_user.id,
            chat_session_id=chat_session.id,
            title=chat_session.title or 'Escalated Chat Issue',
            description=f"{issue_description}\n\nChat Context:\n{chat_context}",
            category='other',
            priority='medium',
            device_info=json.dumps(device_info) if device_info else None
        )
        ticket.ticket_number = ticket.generate_ticket_number()
        
        # Mark chat session as escalated
        chat_session.escalated_to_support = True
        
        db.session.add(ticket)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'ticket_number': ticket.ticket_number,
            'message': 'Chat escalated to support ticket successfully'
        })
    
    except Exception as e:
        log.error("Escalation error: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500

# ---- Admin Routes ----
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    form = AdminLoginForm()
    
    if form.validate_on_submit():
        admin = AdminUser.query.filter_by(username=form.username.data).first()
        
        if admin and check_password_hash(admin.password_hash, form.password.data):
            login_user(admin)
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials.', 'error')
    
    return render_template('admin/login.html', form=form)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard."""
    if not isinstance(current_user, AdminUser):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    # Get ticket statistics
    total_tickets = SupportTicket.query.count()
    open_tickets = SupportTicket.query.filter_by(status='open').count()
    in_progress_tickets = SupportTicket.query.filter_by(status='in_progress').count()
    resolved_tickets = SupportTicket.query.filter_by(status='resolved').count()
    
    # Get recent tickets
    recent_tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_tickets=total_tickets,
                         open_tickets=open_tickets,
                         in_progress_tickets=in_progress_tickets,
                         resolved_tickets=resolved_tickets,
                         recent_tickets=recent_tickets)

@app.route('/admin/tickets')
@login_required
def admin_tickets():
    """Admin ticket management."""
    if not isinstance(current_user, AdminUser):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    status_filter = request.args.get('status', 'all')
    priority_filter = request.args.get('priority', 'all')
    
    query = SupportTicket.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    if priority_filter != 'all':
        query = query.filter_by(priority=priority_filter)
    
    tickets = query.order_by(SupportTicket.created_at.desc()).all()
    
    return render_template('admin/tickets.html', tickets=tickets, 
                         status_filter=status_filter, priority_filter=priority_filter)

@app.route('/admin/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def admin_ticket_detail(ticket_id):
    """Admin ticket detail and update."""
    if not isinstance(current_user, AdminUser):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    ticket = SupportTicket.query.get_or_404(ticket_id)
    form = TicketUpdateForm()
    
    if form.validate_on_submit():
        ticket.status = form.status.data
        ticket.admin_response = form.admin_response.data
        ticket.assigned_to_id = current_user.id
        ticket.updated_at = datetime.utcnow()
        
        if form.status.data == 'resolved':
            ticket.resolved_at = datetime.utcnow()
        
        db.session.commit()
        flash('Ticket updated successfully!', 'success')
        return redirect(url_for('admin_ticket_detail', ticket_id=ticket_id))
    
    # Pre-populate form with current values
    form.status.data = ticket.status
    form.admin_response.data = ticket.admin_response
    
    # Get chat session if exists
    chat_session = None
    chat_messages = []
    if ticket.chat_session_id:
        chat_session = ChatSession.query.get(ticket.chat_session_id)
        if chat_session:
            chat_messages = ChatMessage.query.filter_by(session_id=chat_session.id).order_by(ChatMessage.timestamp.asc()).all()
    
    return render_template('admin/ticket_detail.html', 
                         ticket=ticket, 
                         form=form,
                         chat_session=chat_session,
                         chat_messages=chat_messages)

@app.route('/admin/logout')
@login_required
def admin_logout():
    """Admin logout."""
    logout_user()
    flash('Admin logged out successfully.', 'info')
    return redirect(url_for('admin_login'))


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
        
        # Get or create session ID
        session_id = data.get('session_id') or session.get('chat_session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['chat_session_id'] = session_id
        
        # Get or create chat session
        chat_session = ChatSession.query.filter_by(session_id=session_id).first()
        if not chat_session:
            chat_session = ChatSession(
                session_id=session_id,
                user_id=current_user.id if current_user.is_authenticated else None,
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
            'user_authenticated': current_user.is_authenticated
        })
    
    except Exception as e:
        log.error("Chat error: %s", str(e))
        return jsonify({'error': 'Internal server error'}), 500


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


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get basic statistics"""
    return jsonify({
        'total_faqs': len(_questions),
        'embedding_model': app.config["MODEL_NAME"],
        'chat_model': app.config["CHAT_MODEL"],
        'openai_available': CLIENT is not None,
        'faiss_available': HAVE_FAISS
    })


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