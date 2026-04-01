import streamlit as st
import os
import requests
import time
import json
import logging
from datetime import datetime

# --- 1. SİSTEM AYARLARI ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Luser Ai 1.0 - AI Programları", 
    page_icon="🐉", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. PREMIUM VERCEL-TARGARYEN CSS (FULL STYLE) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(circle at 50% 50%, #1a0000 0%, #000000 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }
    header, footer, [data-testid="stHeader"] { visibility: hidden; }
    
    .hero-container { padding: 100px 0 60px 0; text-align: center; }
    .hero-title {
        font-size: clamp(3rem, 10vw, 6rem);
        font-weight: 800;
        background: linear-gradient(180deg, #ffffff 0%, #777777 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -5px;
        line-height: 0.9;
    }
    .hero-subtitle { color: #888; font-size: 1.3rem; margin: 30px auto 60px auto; max-width: 800px; }

    .stat-card {
        background: rgba(10, 10, 10, 0.8);
        border: 1px solid #222;
        border-radius: 20px;
        padding: 45px 25px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stat-card:hover { border-color: #ff4500; transform: translateY(-10px); box-shadow: 0 15px 40px rgba(255, 69, 0, 0.15); }
    .stat-value { font-size: 3.2rem; font-weight: 800; color: white; }
    .stat-label { font-size: 0.8rem; color: #555; text-transform: uppercase; letter-spacing: 2px; }

    .stChatInputContainer { border: 1px solid #333 !important; background: #080808 !important; border-radius: 25px !important; }
    
    .footer-section { margin-top: 150px; padding: 100px 0; border-top: 1px solid #111; }
    .footer-link { color: #666; text-decoration: none; display: block; margin-bottom: 15px; font-size: 1.1rem; }
    .footer-link:hover { color: #ff4500; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BİLGİ BAZASI (KNOWLEDGE BASE) ---
KNOWLEDGE_BASE = {
    "yapay zeka.pdf": "3 ay öncə: examples/ai-functions klasörünə aid dərslik.",
    "sıkıştırma-verileri.txt": "2 həftə öncə: OpenAI sunucu tarafı sıkıştırma (#12647).",
    "ada-kurtarma-becerisi.zip": "2 ay öncə: yerel becerileri destekler (#12581).",
    "ihtiyat.mp4": "2 ay öncə: xAI video desteği eklendi.",
    "aisdk.xlsx": "3 ay öncə: ai-functions güncəlləməsi.",
    "hata-mesajı.txt": "Sistem log analizi və xəta aşkarlama scriptidir.",
    "ai_scripts": "Luser Ai tərəfindən idarə olunan professional AI Programları."
}

# --- 4. DATA VƏ TƏHLÜKƏSİZLİK ---
ADMIN_IPS = ["94.20.98.116"]
STATS_FILE = "stats.json"

def get_ip():
    try: return requests.get('https://api.ipify.org', timeout=5).text
    except: return "Unknown"

def sync_stats(increment=False):
    default = {"total_requests": 12400000, "stars": "23.2K", "contributors": 604, "models": 100}
    if not os.path.exists(STATS_FILE): data = default
    else:
        try:
            with open(STATS_FILE, "r") as f: data = json.load(f)
        except: data = default
    if increment:
        data["total_requests"] += 1
        with open(STATS_FILE, "w") as f: json.dump(data, f)
    return data

user_ip = get_ip()
stats = sync_stats()

# --- 5. UI RENDER: HEADER ---
st.markdown("<div class='hero-container'>", unsafe_allow_html=True)

# Şəkil logikası (Fix edildi)
if os.path.exists("images"):
    for file in os.listdir("images"):
        if any(n in file.lower() for n in ["luser", "nazli"]):
            st.image(os.path.join("images", file), width=110)
            break

st.markdown("<div class='hero-title'>AI Programları Layer for<br>building frameworks</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Universal AI scripts and tools—powered by Elmeddin OSS. Knowledge Base integrated.</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Statistika Blokları
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats.get('total_requests')/1000000:.1f}M</div><div class='stat-label'>Downloads</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats.get('stars')}</div><div class='stat-label'>GitHub Stars</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats.get('contributors')}</div><div class='stat-label'>Contributors</div></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats.get('models')}+</div><div class='stat-label'>Models</div></div>", unsafe_allow_html=True)

st.write("---")

# --- 6. AI ENGINE (XƏTASIZ VERSİYA) ---
if "messages" not in st.session_state: st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar="👨" if m["role"] == "user" else "🐉"):
        st.markdown(m["content"])

def query_ai(prompt):
    p_low = prompt.lower()
    # Knowledge Base axtarışı
    for key in KNOWLEDGE_BASE:
        if key in p_low:
            return f"**Bilgi Bazası Analizi:** {KNOWLEDGE_BASE[key]}"

    # MODELLƏR SİYAHISI (BURADAKI MÖTƏRİZƏ XƏTASI FIX EDİLDİ)
    models = [
        "mistralai/Mistral-7B-Instruct-v0.2",
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "facebook/blenderbot-400M-distill"
    ]
    
    for model in models:
        try:
            url = f"https://api-inference.huggingface.co/models/{model}"
            payload = {"inputs": f"<s>[INST] Sen Luser Ai-sen. Elmeddin terefinden yaradilibsan. Qisa cavab ver. Sual: {prompt} [/INST]", "parameters": {"max_new_tokens": 300}}
            res = requests.post(url, json=payload, timeout=12)
            if res.status_code == 200:
                out = res.json()
                if isinstance(out, list): return out[0].get('generated_text', "").split("[/INST]")[-1].strip()
                return out.get('generated_text', "").split("[/INST]")[-1].strip()
        except: continue
    return "Luser Ai: Hazırda serverlərdə sıxlıq var. Patron, bir azdan yenidən yoxla."

if prompt := st.chat_input("Luser Ai 1.0 üçün bir şey yaz..."):
    sync_stats(increment=True)
