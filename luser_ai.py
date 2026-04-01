import streamlit as st
import os
import requests
import time
import json
import logging
from datetime import datetime

# --- 1. SİSTEM LOGGİNG VƏ KONFİQURASİYA ---
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
    /* Ana Fon */
    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(circle at 50% 50%, #1a0000 0%, #000000 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    header, footer, [data-testid="stHeader"] { visibility: hidden; }
    
    /* Hero Section */
    .hero-container { padding: 80px 0 40px 0; text-align: center; }
    .hero-title {
        font-size: clamp(2.8rem, 8vw, 5.2rem);
        font-weight: 800;
        background: linear-gradient(180deg, #ffffff 0%, #777777 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -4px;
        line-height: 0.95;
        margin-bottom: 25px;
    }
    .hero-subtitle { color: #999; margin: 0 auto 50px auto; max-width: 850px; font-size: 1.2rem; line-height: 1.6; }

    /* Statistika Kartları */
    .stat-wrapper {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 25px;
        margin-bottom: 70px;
    }
    .stat-card {
        background: rgba(15, 15, 15, 0.8);
        border: 1px solid #222;
        border-radius: 16px;
        padding: 40px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stat-card:hover { 
        border-color: #ff4500; 
        transform: translateY(-10px); 
        box-shadow: 0 15px 40px rgba(255, 69, 0, 0.15); 
    }
    .stat-value { font-size: 3rem; font-weight: 800; color: white; }
    .stat-label { font-size: 0.8rem; color: #666; text-transform: uppercase; letter-spacing: 2px; }

    /* Chat UI */
    .stChatInputContainer { 
        border: 1px solid #333 !important; 
        background: #080808 !important; 
        border-radius: 20px !important; 
        padding: 10px !important; 
    }
    .stChatInputContainer:focus-within { border-color: #ff4500 !important; }
    
    /* Footer */
    .footer-main { margin-top: 120px; padding: 80px 0; border-top: 1px solid #1a1a1a; }
    .footer-link { color: #666; text-decoration: none; display: block; margin-bottom: 12px; transition: color 0.3s; }
    .footer-link:hover { color: #ff4500; }
    
    /* Sidebar */
    .stSidebar { background-color: #050505 !important; border-right: 1px solid #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BİLGİ BAZASI (KNOWLEDGE BASE) ---
KNOWLEDGE_BASE = {
    "yapay zeka.pdf": "3 ay öncə: examples/ai-functions klasörünə aid.",
    "aisdk.xlsx": "3 ay öncə: ai-functions güncəlləməsi.",
    "sıkıştırma-verileri.txt": "2 həftə öncə: OpenAI sunucu tarafı sıkıştırma (#12647).",
    "ada-kurtarma-becerisi.zip": "2 ay öncə: yerel becerileri destekler (#12581).",
    "ihtiyat.mp4": "2 ay öncə: xAI video desteği eklendi.",
    "hata-mesajı.txt": "Log analizi və hata tespiti üçün istifadə olunan scriptdir.",
    "çizgi-kedi.png": "3 ay öncə əlavə edilmiş vizual aktiv.",
    "ai_scripts": "Luser Ai tərəfindən yaradılmış professional AI Programları."
}

# --- 4. DATA VƏ TƏHLÜKƏSİZLİK ---
ADMIN_IPS = ["94.20.98.116"]
STATS_FILE = "stats.json"

def get_visitor_ip():
    try: return requests.get('https://api.ipify.org', timeout=5).text
    except: return "Unknown"

def sync_stats(increment=False):
    default = {"total_requests": 1200000, "stars": "23.2K", "contributors": 1, "models": 100}
    if not os.path.exists(STATS_FILE):
        data = default
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

user_ip = get_visitor_ip()
stats_data = sync_stats()

# --- 5. UI RENDER: HEADER ---
st.markdown("<div class='hero-container'>", unsafe_allow_html=True)

# LOGO FIX (BURADAKI SINTAX XƏTASI DÜZƏLDİ)
if os.path.exists("images"):
    for file in os.listdir("images"):
        if any(n in file.lower() for n in ["luser", "nazli"]):
            st.image(os.path.join("images", file), width=100)
            break

st.markdown("<div class='hero-title'>AI Programları Layer for<br>building frameworks</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Universal AI scripts and tools—powered by Elmeddin OSS. Knowledge Base active.</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Statistika Grid
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats_data.get('total_requests')/1000000:.1f}M</div><div class='stat-label'>Downloads</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats_data.get('stars')}</div><div class='stat-label'>Stars</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats_data.get('contributors')}</div><div class='stat-label'>Contributors</div></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats_data.get('models')}+</div><div class='stat-label'>Models</div></div>", unsafe_allow_html=True)

st.write("---")

# --- 6. AI ENGINE (MULTI-MODEL FALLBACK) ---
if "messages" not in st.session_state: st.session_state.messages = []

# Tarixçə
for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar="👨" if m["role"] == "user" else "🐉"):
        st.markdown(m["content"])

def query_intelligence(prompt):
    # Knowledge Base axtarışı
    p_low = prompt.lower()
    for key in KNOWLEDGE_BASE:
        if key in p_low:
            return f"**Bilgi Bazası Məlumatı:** {KNOWLEDGE_BASE[key]}"

    # Fallback modellər
    model_list = [
        "mistralai/Mistral-7B-Instruct-v0.2",
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "facebook/blenderbot-400M-distill"
    ]
    
    for model in model_list:
        try:
            url = f"https://api-inference.huggingface.co/models/{model}"
            payload = {
                "inputs": f"<s>[INST] Sen Luser Ai-sen. Elmeddin terefinden yaradilibsan. Qisa cavab ver. Sual: {prompt} [/INST]",
                "parameters": {"max_new_tokens": 300, "temperature": 0.7}
            }
            res = requests.post(url, json=payload, timeout=12)
            if res.status_code == 200:
                out = res.json()
                if isinstance(out, list): return out[0].get('generated_text', "").split("[/INST]")[-1].strip()
                return out.get('generated_text', "").split("[/INST]")[-1].strip()
        except: continue
    return "Luser Ai: Patron, serverlərdə sıxlıq var. Bir azdan yenidən cəhd edin."

if prompt := st.chat_input("Luser Ai 1.0 üçün bir şey yaz..."):
    sync_stats(increment=True)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨"): st.markdown(prompt)
