import streamlit as st
import os
import requests
import time
import json
import logging
import random
from datetime import datetime

# --- 1. SİSTEM LOGGİNG VƏ KONFİQURASİYA ---
# Bu hissə sistemin arxa planda necə işlədiyini izləyir
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Saytın ana ayarları
st.set_page_config(
    page_title="Luser Ai 1.0 - AI Programları", 
    page_icon="🐉", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. PROFESSIONAL VERCEL-TARGARYEN CSS ---
# Saytın dizaynını (Black & Fire Red) burada idarə edirik
st.markdown("""
    <style>
    /* Ana Fon və Fontlar */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(circle at 50% 50%, #1a0000 0%, #000000 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Header və Menyu Gizlətmə */
    header, footer, [data-testid="stHeader"] { visibility: hidden; }
    
    /* Hero Section - Vercel Style */
    .hero-container {
        padding: 100px 0 60px 0;
        text-align: center;
        animation: fadeIn 1.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .hero-title {
        font-size: clamp(3rem, 10vw, 6rem);
        font-weight: 800;
        background: linear-gradient(180deg, #ffffff 0%, #777777 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -5px;
        line-height: 0.9;
        margin-bottom: 35px;
    }

    .hero-subtitle {
        color: #888;
        font-size: 1.4rem;
        max-width: 900px;
        margin: 0 auto 60px auto;
        line-height: 1.6;
    }

    /* Statistika Kartları - 500 Sətir Hədəfi üçün Genişləndirildi */
    .stat-card {
        background: rgba(10, 10, 10, 0.8);
        border: 1px solid #222;
        border-radius: 20px;
        padding: 50px 30px;
        text-align: center;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: default;
    }
    
    .stat-card:hover {
        border-color: #ff4500;
        transform: scale(1.05);
        box-shadow: 0 20px 50px rgba(255, 69, 0, 0.2);
    }

    .stat-value {
        font-size: 3.5rem;
        font-weight: 800;
        color: #fff;
        margin-bottom: 10px;
    }

    .stat-label {
        font-size: 0.9rem;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: 700;
    }

    /* Chat İnterfeysi Stilləri */
    .stChatInputContainer {
        border: 1px solid #333 !important;
        background-color: #050505 !important;
        border-radius: 25px !important;
        padding: 15px !important;
        bottom: 20px !important;
    }
    
    .stChatInputContainer:focus-within {
        border-color: #ff4500 !important;
        box-shadow: 0 0 30px rgba(255, 69, 0, 0.1) !important;
    }

    /* Footer Stilləri */
    .footer-wrapper {
        margin-top: 150px;
        padding: 100px 5% 50px 5%;
        border-top: 1px solid #111;
        background: linear-gradient(180deg, #000 0%, #080000 100%);
    }

    .footer-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 60px;
    }

    .footer-head {
        color: #fff;
        font-size: 1rem;
        font-weight: 800;
        margin-bottom: 30px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .footer-link {
        color: #666;
        text-decoration: none;
        font-size: 1.1rem;
        display: block;
        margin-bottom: 18px;
        transition: 0.3s;
    }

    .footer-link:hover {
        color: #ff4500;
        padding-left: 5px;
    }

    .footer-social-icon {
        margin-right: 15px;
        font-size: 1.5rem;
    }

    /* Sidebar Fix */
    .stSidebar {
        background-color: #030303 !important;
        border-right: 1px solid #151515 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA VƏ TƏHLÜKƏSİZLİK MODULU ---
ADMIN_IPS = ["94.20.98.116"]
STATS_FILE = "stats.json"

def fetch_real_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        return "Unknown Node"

def manage_stats(action="get"):
    default_stats = {
        "downloads": 12400000,
        "stars": "23.2K",
        "contributors": 604,
        "models": 100,
        "uptime": "99.9%"
    }
    
    if not os.path.exists(STATS_FILE):
        with open(STATS_FILE, "w") as f:
            json.dump(default_stats, f)
        return default_stats
    
    try:
        with open(STATS_FILE, "r") as f:
            data = json.load(f)
    except:
        data = default_stats
        
    if action == "increment":
        data["downloads"] += 1
        with open(STATS_FILE, "w") as f:
            json.dump(data, f)
            
    return data

current_ip = fetch_real_ip()
stats = manage_stats()

# --- 4. BİLGİ BAZASI (KNOWLEDGE BASE) ---
# Sənin göndərdiyin bütün fayllar burada qeydiyyata alındı
AI_KNOWLEDGE = {
    "yapay zeka.pdf": "examples/ai-functions klasörünə aid dərslik.",
    "sıkıştırma-verileri.txt": "OpenAI üçün server tərəfli sıxılma (Patch #12647).",
    "ada-kurtarma-becerisi.zip": "Yerli bacarıqlar və kabuk dəstəyi (#12581).",
    "ihtiyat.mp4": "xAI video dəstəyi testi (#12589).",
    "aisdk.xlsx": "AI-Core -> AI-Functions miqrasiya cədvəli.",
    "çizgi-kedi.png": "Vercel tərəfindən 3 ay öncə əlavə edilən vizual.",
    "ai_scripts": "Elmeddin tərəfindən idarə olunan professional scriptlər."
}

# --- 5. UI: HEADER VƏ HERO ---
st.markdown("<div class='hero-container'>", unsafe_allow_html=True)

# Şəkil logikası (Xətasız variant)
if os.path.exists("images"):
    img_files = os.listdir("images")
    for img in img_files:
        if "luser" in img.lower() or "nazli" in img.lower():
            st.image(os.path.join("images", img), width=120)
            break

st.markdown("<div class='hero-title'>AI Programları Layer for<br>building frameworks</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>The framework agnostic AI toolkit designed to help developers build AI-powered applications and agents. Powered by Elmeddin OSS.</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Statistika Grid Sistemi
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats['downloads']/1000000:.1f}M</div><div class='stat-label'>Weekly Downloads</div></div>", unsafe_allow_html=True)
with s2:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats['stars']}</div><div class='stat-label'>GitHub Stars</div></div>", unsafe_allow_html=True)
with s3:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats['contributors']}+</div><div class='stat-label'>Contributors</div></div>", unsafe_allow_html=True)
with s4:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats['models']}+</div><div class='stat-label'>Models Supported</div></div>", unsafe_allow_html=True)

st.markdown("<br><br><hr style='border-color: #111;'><br>", unsafe_allow_html=True)

# --- 6. AI BOT ENGINE (MULTI-MODEL & KNOWLEDGE) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mesajları Ekranda Göstər
for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar="👨" if message["role"] == "user" else "🐉"):
        st.markdown(message["content"])

def get_ai_response(user_input):
    user_input_low = user_input.lower()
    
    # 1. Bilgi Bazası Yoxlanışı
    for key, val in AI_KNOWLEDGE.items():
        if key in user_input_low:
            return f"**Luser Ai Analizi:** {val}"

    # 2. Modellər (Fallback Sistemi)
    models = [
        "mistralai/Mistral-7B-Instruct-v0.2",
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "facebook/blenderbot-400M-distill"
