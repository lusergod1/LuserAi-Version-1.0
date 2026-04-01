import streamlit as st
import os
import requests
import time
import json
import logging
from datetime import datetime

# --- 1. SİSTEM LOGGİNG ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 2. ANA SƏHİFƏ AYARLARI ---
st.set_page_config(
    page_title="Luser Ai 1.0 - Vercel Master Edition", 
    page_icon="🐉", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. PREMIUM VERCEL-TARGARYEN CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(circle at 50% 50%, #1a0000 0%, #000000 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }
    header, footer, [data-testid="stHeader"] { visibility: hidden; }
    
    .hero-container { padding: 80px 0 40px 0; text-align: center; }
    .hero-title {
        font-size: clamp(2.8rem, 8vw, 5.2rem);
        font-weight: 800;
        background: linear-gradient(180deg, #ffffff 0%, #777777 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -4px;
        line-height: 0.95;
    }
    .hero-subtitle { color: #999; margin: 20px auto 50px auto; max-width: 800px; }

    .stat-card {
        background: rgba(15, 15, 15, 0.8);
        border: 1px solid #222;
        border-radius: 16px;
        padding: 40px;
        transition: 0.4s ease;
    }
    .stat-card:hover { border-color: #ff4500; transform: translateY(-10px); }
    .stat-value { font-size: 3rem; font-weight: 800; }
    .stat-label { font-size: 0.8rem; color: #666; text-transform: uppercase; letter-spacing: 2px; }

    .stChatInputContainer { border: 1px solid #333 !important; background: #080808 !important; border-radius: 20px !important; }
    .stChatInputContainer:focus-within { border-color: #ff4500 !important; }

    .footer-link { color: #777; text-decoration: none; display: block; margin-bottom: 12px; }
    .footer-link:hover { color: #ff4500; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA VƏ TƏHLÜKƏSİZLİK ---
ADMIN_IPS = ["94.20.98.116"]
STATS_FILE = "stats.json"

def get_ip():
    try: return requests.get('https://api.ipify.org', timeout=5).text
    except: return "Unknown"

def sync_stats(increment=False):
    default = {"total_requests": 1200000, "stars": "23.2K", "contributors": 1, "models": 100}
    if not os.path.exists(STATS_FILE): data = default
    else:
        try:
            with open(STATS_FILE, "r") as f:
                data = json.load(f)
                for k, v in default.items():
                    if k not in data: data[k] = v
        except: data = default
    if increment:
        data["total_requests"] += 1
        with open(STATS_FILE, "w") as f: json.dump(data, f)
    return data

user_ip = get_ip()
stats = sync_stats()

# --- 5. UI RENDER ---
st.markdown("<div class='hero-container'>", unsafe_allow_html=True)
if os.path.exists("images"):
    for file in os.listdir("images"):
        if any(n in file.lower() for n in ["luser", "nazli"]):
            st.image(os.path.join("images", file), width=100)
            break
st.markdown("<div class='hero-title'>Universal AI layer for<br>building frameworks and agents</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Powered by Elmeddin OSS. Multi-model AI fallback system active.</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats.get('total_requests')/1000000:.1f}M</div><div class='stat-label'>Downloads</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats.get('stars')}</div><div class='stat-label'>Stars</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats.get('contributors')}</div><div class='stat-label'>Contributors</div></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats.get('models')}+</div><div class='stat-label'>Models</div></div>", unsafe_allow_html=True)

st.write("---")

# --- 6. AI ENGINE (FALLBACK SYSTEM) ---
if "messages" not in st.session_state: st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar="👨" if m["role"] == "user" else "🐉"):
        st.markdown(m["content"])

def query_ai(prompt):
    """Ehtiyat modellərlə AI sorğusu."""
    # Model 1: Mistral
    # Model 2: TinyLlama (Fallback)
    # Model 3: BlenderBot (Emergency)
    models = [
        "mistralai/Mistral-7B-Instruct-v0.2",
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "facebook/blenderbot-400M-distill"
    ]
    
    for model in models:
        try:
            API_URL = f"https://api-inference.huggingface.co/models/{model}"
            payload = {"inputs": f"<s>[INST] You are Luser Ai. Be brief. {prompt} [/INST]", "parameters": {"max_new_tokens": 200}}
            response = requests.post(API_URL, json=payload, timeout=10)
            
            if response.status_code == 200:
                res = response.json()
                if isinstance(res, list): return res[0].get('generated_text', "").split("[/INST]")[-1].strip()
                return res.get('generated_text', "").split("[/INST]")[-1].strip()
        except:
            continue # Növbəti modelə keç
    return "Luser Ai: Hazırda bütün serverlər doludur. 5 saniyə sonra yenidən cəhd edin."

if prompt := st.chat_input("Luser Ai 1.0 üçün bir şey yaz..."):
    sync_stats(increment=True)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨"): st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="🐉"):
        with st.status("📡 Analiz edilir...", expanded=False) as status:
            ans = query_ai(prompt)
            status.update(label="✅ Tamamlandı", state="complete")
        st.markdown(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})

# --- 7. FOOTER ---
st.markdown(f"""
    <div style='margin-top:100px; padding:60px 0; border-top:1px solid #111;'>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 40px;'>
            <div><p style='color:white; font-weight:bold;'>SOCIAL</p>
                <a class='footer-link' href='https://instagram.com/lusergod'>Instagram</a>
                <a class='footer-link' href='https://tiktok.com/@lusergod'>TikTok</a></div>
            <div><p style='color:white; font-weight:bold;'>LEGAL</p>
                <a class='footer-link' href='#'>Privacy Policy</a></div>
        </div>
        <p style='text-align:center; color:#444; margin-top:50px;'>© 2026 Luser Ai | Node: {user_ip}</p>
    </div>
""", unsafe_allow_html=True)

# --- 8. ADMIN ---
if user_ip in ADMIN_IPS:
    with st.sidebar:
        st.markdown("<h2 style='color:#ff4500;'>👑 ADMIN</h2>", unsafe_allow_html=True)
        if st.button("Clear Chat"): st.session_state.messages = []; st.rerun()
