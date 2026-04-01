import streamlit as st
import os
import requests
import time
import json
import logging
from datetime import datetime

# --- 1. SİSTEM VƏ LOGGİNG AYARLARI ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 2. KONFİQURASİYA VƏ BRENDİNQ ---
st.set_page_config(
    page_title="Luser Ai 1.0 - Vercel Master Edition", 
    page_icon="🐉", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. EXTENDED CSS (Vercel Dark + Targaryen Glow) ---
st.markdown("""
    <style>
    /* Ana Fon və Rəng Palitrası */
    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(circle at 50% 50%, #1a0000 0%, #000000 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', -apple-system, system-ui, sans-serif !important;
    }
    
    /* Standart Streamlit Elementlərini Gizlə */
    header, footer, [data-testid="stHeader"] { visibility: hidden; }
    
    /* Vercel Hero Bölməsi */
    .hero-container {
        padding: 60px 0;
        text-align: center;
    }
    .hero-title {
        font-size: clamp(2.5rem, 7vw, 4.5rem);
        font-weight: 800;
        background: linear-gradient(180deg, #ffffff 0%, #a1a1a1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -3px;
        line-height: 1.1;
        margin-bottom: 20px;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: #888888;
        max-width: 700px;
        margin: 0 auto 40px auto;
        line-height: 1.6;
    }

    /* Statistika Kartları */
    .stat-wrapper {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-bottom: 60px;
    }
    .stat-card {
        background: rgba(10, 10, 10, 0.6);
        border: 1px solid #222;
        border-radius: 12px;
        padding: 30px;
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        border-color: #ff4500;
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(255, 69, 0, 0.1);
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 5px;
    }

    /* Chat UI Tənzimləmələri */
    .stChatInputContainer {
        border: 1px solid #333 !important;
        background-color: #050505 !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #ff4500 !important;
    }

    /* Footer Dizaynı */
    .footer-main {
        margin-top: 100px;
        padding: 60px 0;
        border-top: 1px solid #222;
    }
    .footer-link {
        color: #888;
        text-decoration: none;
        font-size: 0.95rem;
        transition: color 0.2s;
    }
    .footer-link:hover { color: #ff4500; }
    
    /* Button Customization */
    .stButton>button {
        background-color: transparent !important;
        color: #ff4500 !important;
        border: 1px solid #ff4500 !important;
        border-radius: 8px !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA İDARƏETMƏ VƏ TƏHLÜKƏSİZLİK ---
ADMIN_IPS = ["94.20.98.116"]
STATS_FILE = "stats.json"

def get_visitor_ip():
    """Ziyarətçinin real IP ünvanını qaytarır."""
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except Exception as e:
        logger.error(f"IP retrieval error: {e}")
        return "Unknown"

def init_stats():
    """Statistikaları ilkin vəziyyətə gətirir və KeyError-in qarşısını alır."""
    return {
        "total_requests": 1200000,
        "weekly_active_bots": 5,
        "contributors": 1,
        "models_supported": 100,
        "last_updated": str(datetime.now())
    }

def load_or_update_stats(increment=False):
    """Fayldan statistikaları oxuyur və açarları yoxlayır."""
    default = init_stats()
    if not os.path.exists(STATS_FILE):
        data = default
    else:
        try:
            with open(STATS_FILE, "r") as f:
                data = json.load(f)
                # Eksik açarları yoxla (KeyError Fix)
                for key in default:
                    if key not in data:
                        data[key] = default[key]
        except Exception as e:
            logger.error(f"Stats load error: {e}")
            data = default
            
    if increment:
        data["total_requests"] += 1
        data["last_updated"] = str(datetime.now())
        try:
            with open(STATS_FILE, "w") as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"Stats save error: {e}")
            
    return data

# Məlumatları yüklə
current_ip = get_visitor_ip()
stats_data = load_or_update_stats()

# --- 5. LOGO VƏ BAŞLIQ (UI) ---
def render_header():
    st.markdown("<div class='hero-container'>", unsafe_allow_html=True)
    
    # Loqo axtarışı
    logo_found = False
    if os.path.exists("images"):
        for file in os.listdir("images"):
            if any(name in file.lower() for name in ["luser", "nazli"]):
                st.image(os.path.join("images", file), width=80)
                logo_found = True
                break
    
    st.markdown("<div class='hero-title'>Universal AI layer for<br>building frameworks and agents</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>A unified Luser SDK for building AI apps with modern streaming, and multi-model support—powered by Elmeddin OSS.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

render_header()

# Statistika Kartları (Dinamik)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats_data.get('total_requests', 0)/1000000:.1f}M</div><div class='stat-label'>Weekly downloads</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>23.2K</div><div class='stat-label'>GitHub stars</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats_data.get('contributors', 1)}</div><div class='stat-label'>Contributors</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats_data.get('models_supported', 100)}+</div><div class='stat-label'>Models supported</div></div>", unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: #222;'><br>", unsafe_allow_html=True)

# --- 6. CHAT SİSTEMİ (TinyLlama Sürətli Model) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj tarixçəsini render et
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👨" if message["role"] == "user" else "🐉"):
        st.markdown(message["content"])

# Giriş sahəsi
if prompt := st.chat_input("Luser Ai 1.0 üçün bir əmr ver..."):
    # Stat artır
    load_or_update_stats(increment=True)
    
    # İstifadəçi mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨"):
        st.markdown(prompt)
    
    # AI Cavabı
    with st.chat_message("assistant", avatar="🐉"):
        with st.status("📡 Analiz edilir...", expanded=False) as status:
            # Sürətli TinyLlama modeli (Max 10 saniye timeout)
            API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
            try:
                payload = {
                    "inputs": f"<|system|>\nYou are Luser Ai, a professional AI developed by Elmeddin. Be helpful and very concise. Response language: Azerbaijani/English.<|user|>\n{prompt}<|assistant|>\n",
                    "parameters": {"max_new_tokens": 250, "temperature": 0.7
