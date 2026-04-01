import streamlit as st
import os
import requests
import time
import json
import logging
import random
from datetime import datetime

# --- 1. SİSTEM VƏ LOGGİNG KONFİQURASİYASI ---
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
    /* Qara və Qırmızı Parıltı Fonu */
    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(circle at 50% 50%, #1a0000 0%, #000000 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    
    /* Gereksiz elementləri gizləmək */
    header, footer, [data-testid="stHeader"] { visibility: hidden; }
    
    /* Vercel Hero Bölməsi */
    .hero-container {
        padding: 80px 0 40px 0;
        text-align: center;
    }
    .hero-title {
        font-size: clamp(2.8rem, 8vw, 5.2rem);
        font-weight: 800;
        background: linear-gradient(180deg, #ffffff 0%, #777777 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -4px;
        line-height: 0.95;
        margin-bottom: 30px;
    }
    .hero-subtitle {
        font-size: 1.35rem;
        color: #999999;
        max-width: 850px;
        margin: 0 auto 50px auto;
        line-height: 1.5;
    }

    /* Statistika Paneli (4-lü Kart Sistemi) */
    .stat-wrapper {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 30px;
        margin-bottom: 80px;
    }
    .stat-card {
        background: rgba(15, 15, 15, 0.8);
        border: 1px solid #222;
        border-radius: 16px;
        padding: 40px;
        text-align: left;
        transition: all 0.4s ease;
    }
    .stat-card:hover {
        border-color: #ff4500;
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(255, 69, 0, 0.15);
    }
    .stat-value {
        font-size: 3.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 8px;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
    }

    /* Professional Chat İnterfeysi */
    .stChatInputContainer {
        border: 1px solid #333 !important;
        background-color: #080808 !important;
        border-radius: 20px !important;
        padding: 15px !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #ff4500 !important;
        box-shadow: 0 0 25px rgba(255, 69, 0, 0.2) !important;
    }

    /* Footer və Linklər */
    .footer-main {
        margin-top: 140px;
        padding: 80px 0;
        border-top: 1px solid #151515;
    }
    .footer-heading {
        color: #ffffff;
        font-size: 0.95rem;
        font-weight: 800;
        margin-bottom: 25px;
        text-transform: uppercase;
    }
    .footer-link {
        color: #777;
        text-decoration: none;
        font-size: 1rem;
        display: block;
        margin-bottom: 15px;
        transition: color 0.3s ease;
    }
    .footer-link:hover { color: #ff4500; }
    
    /* Button Stilləri */
    .stButton>button {
        background-color: #111 !important;
        color: #ffffff !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        height: 50px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        border-color: #ff4500 !important;
        color: #ff4500 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. STATİSTİKA VƏ IP QORUMASI ---
ADMIN_IPS = ["94.20.98.116"]
STATS_FILE = "stats.json"

def get_user_real_ip():
    try:
        # Daha stabil IP servisi
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        return "Unknown"

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
        with open(STATS_FILE, "w") as f:
            json.dump(data, f)
    return data

user_ip = get_user_real_ip()
stats = sync_stats()

# --- 5. UI: HEADER VƏ LOQO ---
def render_header_section():
    st.markdown("<div class='hero-container'>", unsafe_allow_html=True)
    
    # Loqo Sistemi
    if os.path.exists("images"):
        for file in os.listdir("images"):
            if any(n in file.lower() for n in ["luser", "nazli"]):
                st.image(os.path.join("images", file), width=100)
                break
    
    st.markdown("<div class='hero-title'>Universal AI layer for<br>building frameworks and agents</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>A unified Luser SDK for building AI apps with modern streaming, and multi-model support—powered by Elmeddin OSS.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

render_header_section()

# Statistika Kartları
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats.get('total_requests')/1000000:.1f}M</div><div class='stat-label'>Weekly downloads</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats.get('stars')}</div><div class='stat-label'>GitHub stars</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats.get('contributors')}</div><div class='stat-label'>Contributors</div></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats.get('models')}+</div><div class='stat-label'>Models supported</div></div>", unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: #1a1a1a;'><br>", unsafe_allow_html=True)

# --- 6. GÜCLÜ VƏ STABİL CHAT SİSTEMİ (Mistral-7B) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar="👨" if m["role"] == "user" else "🐉"):
        st.markdown(m["content"])

if prompt := st.chat_input("Luser Ai 1.0 üçün bir şey yaz..."):
    sync_stats(increment=True)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨"):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="🐉"):
        with st.status("📡 Luser Ai Analiz Edir...", expanded=False) as status:
            # Daha stabil Mistral-7B Modeli
            API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
            try:
                # Sürətli cavab üçün tənzimləmə
                headers = {"Authorization": f"Bearer {st.secrets.get('HF_TOKEN', '')}"} # Token varsa istifadə et
                payload = {
                    "inputs": f"<s>[INST] You are Luser Ai, created by Elmeddin. Respond concisely in Azerbaijani/English. Prompt: {prompt} [/INST]",
                    "parameters": {"max_new_tokens": 500, "temperature": 0.7, "return_full_text": False}
                }
                
                # Botun cavab verməsi üçün 10 saniyə limit
                response = requests.post(API_URL, json=payload, timeout=12)
                
                if response.status_code == 200:
                    res_json = response.json()
                    # Cavabın gəlmə formasını yoxla
                    if isinstance(res_json, list):
                        ans = res_json[0].get('generated_text', "Luser Ai: Hazırdır!")
                    else:
                        ans = res_json.get('generated_text', "Luser Ai: Analiz tamamlandı.")
                    
                    status.update(label="✅ Tamamlandı", state="complete")
                else:
                    ans = "Luser Ai: Server hazırda yüklənib, zəhmət olmasa bir neçə saniyə sonra yenidən göndərin."
                    status.update(label="⚠️ Server Yüklənib", state="error")
            except Exception as e:
                ans = "Luser Ai: Bağlantı xətası baş verdi. Amma mən hələ də buradayam!"
                status.update(label="❌ Xəta", state="error")
        
        st.markdown(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})

# --- 7. FOOTER: SOSİAL VƏ QANUNİ LİNKLƏR ---
st.markdown(f"""
    <div class='footer-main'>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 80px;'>
            <div>
                <div class='footer-heading'>Explore</div>
                <a class='footer-link' href='#'>Documentation</a>
                <a class='footer-link' href='#'>AI SDK</a>
                <a class='footer-link' href='#'>Showcase</a>
            </div>
            <div>
                <div class='footer-heading'>Social</div>
                <a class='footer-link' href='https://instagram.com/lusergod' target='_blank'>Instagram</a>
                <a class='footer-link' href='https://tiktok.com/@lusergod' target='_blank'>TikTok</a>
                <a class='footer-link' href='https://discordapp.com/users/lusergod' target='_blank'>Discord Profil</a>
            </div>
            <div>
                <div class='footer-heading'>Legal</div>
                <a class='footer-link' href='#'>Privacy Policy</a>
                <a class='footer-link' href='#'>Terms of Service</a>
                <a class='footer-link' href='#'>Cookie Policy</a>
            </div>
        </div>
        <div style='text-align: center; margin-top: 100px; color: #555; font-size: 0.85rem;'>
            © 2026 Luser Ai, Elmeddin Inc. Bütün hüquqlar qorunur.<br>
            Node IP: <span style='color: #ff4500;'>{user_ip}</span> | Status: <span style='color: #00ff00;'>Online</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 8. ADMIN DASHBOARD ---
if user_ip in ADMIN_IPS:
    with st.sidebar:
        st.markdown("<h2 style='color: #ff4500;'>🐉 PATRON DASHBOARD</h2>", unsafe_allow_html=True)
        st.write(f"Xoş gəldin, Elmeddin!")
        
        if st.button("Söhbəti Təmizlə"):
            st.session_state.messages = []
            st.rerun()
            
        if st.button("Statistikaları Sıfırla"):
            if os.path.exists(STATS_FILE): os.remove(STATS_FILE)
            st.rerun()
            
        with st.expander("Sistem Məlumatları"):
            st.write(f"İstifadəçi IP: {user_ip}")
            st.write(f"Fayl: luser_ai.py")
else:
    with st.sidebar:
        st.markdown("<h3 style='color: #444;'>Luser Ai v1.0</h3>", unsafe_allow_html=True)
        st.caption("Powered by Elmeddin")
        
