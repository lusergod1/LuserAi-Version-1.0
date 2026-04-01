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

# --- 2. ANA KONFİQURASİYA ---
st.set_page_config(
    page_title="Luser Ai 1.0 - AI Programları", 
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
    .stat-card:hover { border-color: #ff4500; transform: translateY(-10px); box-shadow: 0 15px 40px rgba(255, 69, 0, 0.15); }
    .stat-value { font-size: 3rem; font-weight: 800; color: white; }
    .stat-label { font-size: 0.8rem; color: #666; text-transform: uppercase; letter-spacing: 2px; }

    /* Chat UI */
    .stChatInputContainer { border: 1px solid #333 !important; background: #080808 !important; border-radius: 20px !important; padding: 10px !important; }
    .stChatInputContainer:focus-within { border-color: #ff4500 !important; box-shadow: 0 0 20px rgba(255, 69, 0, 0.1) !important; }
    
    /* Footer */
    .footer-main { margin-top: 120px; padding: 80px 0; border-top: 1px solid #1a1a1a; }
    .footer-link { color: #666; text-decoration: none; display: block; margin-bottom: 12px; transition: color 0.3s; }
    .footer-link:hover { color: #ff4500; }
    
    /* Sidebar Fix */
    .stSidebar { background-color: #050505 !important; border-right: 1px solid #1a1a1a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. BİLGİ BAZASI (KNOWLEDGE BASE) ---
KNOWLEDGE_BASE = {
    "yapay zeka.pdf": "3 ay öncə: examples/ai-functions klasörünə aid.",
    "sıkıştırma-verileri.txt": "2 həftə öncə: OpenAI sunucu tarafı sıkıştırma (#12647).",
    "ada-kurtarma-becerisi.zip": "2 ay öncə: yerel becerileri destekler (#12581).",
    "ihtiyat.mp4": "2 ay öncə: xAI video desteği eklendi.",
    "aisdk.xlsx": "3 ay öncə: ai-functions klasör güncellemesi.",
    "hata-mesajı.txt": "Log analizi və hata tespiti scripti.",
    "ai_scripts": "Luser Ai tərəfindən idarə olunan professional AI Programlarıdır."
}

# --- 5. DATA VƏ TƏHLÜKƏSİZLİK ---
ADMIN_IPS = ["94.20.98.116"]
STATS_FILE = "stats.json"

def get_visitor_ip():
    try: return requests.get('https://api.ipify.org', timeout=5).text
    except: return "Unknown"

def load_or_init_stats(increment=False):
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
stats_data = load_or_init_stats()

# --- 6. UI RENDER (HEADER) ---
st.markdown("<div class='hero-container'>", unsafe_allow_html=True)
if os.path.exists("images"):
    for file in os.listdir("images"):
        if any(n
               
