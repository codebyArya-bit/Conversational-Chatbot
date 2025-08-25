# app.py
from __future__ import annotations

import os
import json
import uuid
import logging
from datetime import datetime
from typing import List, Tuple, Optional

try:
    try:
        from flask import Flask, request, jsonify, render_template  # type: ignore
    except ImportError:
        raise ImportError("Flask is required. Install with: pip install flask")
except ImportError:
    raise ImportError("Flask is required. Install with: pip install flask")
try:
    from flask_cors import CORS  # type: ignore
except ImportError:
    raise ImportError("Flask-CORS is required. Install with: pip install flask-cors")

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

# OpenAI is optional; we degrade to direct FAQ answers if no key.
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
CLIENT = None
if OPENAI_KEY:
    try:
        try:
            from openai import OpenAI  # type: ignore
        except ImportError:
            raise ImportError("OpenAI is required. Install with: pip install openai")
        CLIENT = OpenAI(api_key=OPENAI_KEY)
    except Exception:
        CLIENT = None

# ---- Config ----
class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "change-this-in-prod")
    FAQ_CSV_PATH = os.environ.get("FAQ_CSV_PATH", "ICT Cell Common problems - Hardware issues.csv")
    EMB_PATH = os.path.join(".cache", "faq_embeddings.npy")
    Q_PATH = os.path.join(".cache", "faq_questions.json")
    MODEL_NAME = os.environ.get("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    TOP_K = int(os.environ.get("TOP_K", "3"))
    MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "350"))
    CHAT_MODEL = os.environ.get("CHAT_MODEL", "gpt-4o-mini")  # keep cheap & available

os.makedirs(".cache", exist_ok=True)

# ---- Logging ----
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("tech-edu-hub")

# ---- App ----
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]
CORS(app)

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


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400
    
    user_message = data['message'].strip()
    
    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    # Get chatbot response
    bot_response = get_chatbot_response(user_message)
    
    return jsonify({
        'response': bot_response,
        'session_id': str(uuid.uuid4()),
        'timestamp': datetime.now().isoformat()
    })


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
    app.run(debug=True, host='0.0.0.0', port=5000)