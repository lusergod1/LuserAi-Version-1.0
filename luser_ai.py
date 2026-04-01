import streamlit as st
import os
import requests
import time
import json

# --- 1. KONFİQURASİYA VƏ BRENDİNQ (Köhnə və Yeni Birlikdə) ---
st.set_page_config(
    page_title="Luser Ai 1.0 - Vercel Edition", 
    page_icon="🐉", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. PREMİUM DİZAYN (Vercel + Targaryen Red) ---
# Burada həm sən istədiyin SS-dəki Vercel stili, həm də köhnə Targaryen parıltısı birləşib.
st.markdown("""
    <style>
    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(circle, #2a0000 0%, #000000 100%) !important;
        color: white !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Vercel Style Titles */
    .hero-title {
        font-size: clamp(2.5rem, 6vw, 4rem);
        font-weight: 800;
        text-align: center;
        color: white;
        text-shadow: 0 0 20px rgba(255, 69, 0, 0.4);
        letter-spacing: -2px;
        padding-top: 40px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #888;
        margin-bottom: 40px;
    }
    
    /* Stat Cards (Vercel Style) */
    .stat-card {
        background: rgba(15, 15, 15, 0.8);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 25px;
        text-align: left;
        transition: border-color 0.3s;
    }
    .stat-card:hover { border-color: #ff4500; }
    .stat-value { font-size: 2.8rem; font-weight: 700; color: white; }
    .stat-label { font-size: 0.9rem; color: #666; text-transform: uppercase; }

    /* Footer Links */
    .footer-container { margin-top: 80px; border-top: 1px solid #222; padding: 40px 0; }
    .footer-link { color: #888; text-decoration: none; margin-bottom: 8px; display: block; }
    .footer-link:hover { color: #ff4500; }

    /* Chat UI */
    .stChatInputContainer { border: 1px solid #ff4500 !important; border-radius: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SİSTEM FUNKSİYALARI (Heç nə silinmədi) ---
ADMIN_IPS = ["94.20.98.116"] 
STATS_FILE = "stats.json"

def get_real_ip():
    try: return requests.get('https://api.ipify.org').text
    except: return "Unknown"

def manage_stats(increment=False):
    if not os.path.exists(STATS_FILE):
        data = {"total_requests": 1200000, "active_bots": 1, "contributors": 1, "models": 100}
    else:
        try:
            with open(STATS_FILE, "r") as f: data = json.load(f)
        except: data = {"total_requests": 1200000, "active_bots": 1, "contributors": 1, "models": 100}
    if increment:
        data["total_requests"] += 1
        with open(STATS_FILE, "w") as f: json.dump(data, f)
    return data

current_user_ip = get_real_ip()
stats = manage_stats()

# --- 4. GİRİŞ EKRANI (Yeni Dizayn Köhnənin Üstünə) ---
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

# Loqo Funksiyası (Təkrarlananlar silindi, ən yaxşısı qaldı)
def display_logo():
    if os.path.exists("images"):
        for f in os.listdir("images"):
            if any(x in f.lower() for x in ["luser", "nazli"]):
                st.image(os.path.join("images", f), width=70)
                return
display_logo()

st.markdown("<div class='hero-title'>Universal AI layer for<br>building frameworks and agents</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>A unified Luser SDK for building AI apps with modern streaming,<br>fallbacks, and multi-model support—powered by Elmeddin OSS.</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Statistika (Vercel Style)
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats['total_requests']/1000000:.1f}M</div><div class='stat-label'>Weekly downloads</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-card'><div class='stat-value'>23.2K</div><div class='stat-label'>GitHub stars</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats['contributors']}+</div><div class='stat-label'>Contributors</div></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats['models']}+</div><div class='stat-label'>Models supported</div></div>", unsafe_allow_html=True)

st.write("---")

# --- 5. CHAT SİSTEMİ (Hugging Face AI - Köhnə kod saxlanıldı) ---
if "messages" not in st.session_state: 
    st.session_state.messages = []

# Mesajları ekrana ver
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👨" if msg["role"] == "user" else "🐉"):
        st.markdown(msg["content"])

# Yeni Mesaj
if prompt := st.chat_input("Luser Ai 1.0 üçün bir əmr ver..."):
    manage_stats(increment=True) # Hər mesajda sayğacı artır
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨"): 
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="🐉"):
        with st.status("📡 Analiz edilir...", expanded=False):
            API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
            try:
                r = requests.post(API_URL, json={"inputs": prompt}, timeout=10)
                res = r.json()[0]['generated_text']
            except: 
                res = "Luser Ai: Hazırda serverlərdə bir az sıxlıq var, Patron. Amma sistem aktivdir!"
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

# --- 6. FOOTER (Linklərin Hamısı Bura Yığıldı) ---
st.markdown(f"""
    <div class='footer-container'>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 40px;'>
            <div>
                <p style='color:white; font-weight:bold;'>USE CASES</p>
                <a class='footer-link' href='#'>Web apps</a>
                <a class='footer-link' href='#'>Marketing sites</a>
            </div>
            <div>
                <p style='color:white; font-weight:bold;'>COMMUNITY</p>
                <a class='footer-link' href='https://instagram.com/lusergod' target='_blank'>Instagram</a>
                <a class='footer-link' href='https://tiktok.com/@lusergod' target='_blank'>TikTok</a>
                <a class='footer-link' href='https://discordapp.com/users/lusergod' target='_blank'>Discord (lusergod)</a>
            </div>
            <div>
                <p style='color:white; font-weight:bold;'>COMPANY</p>
                <a class='footer-link' href='#'>About Luser Ai</a>
                <a class='footer-link' href='#'>Privacy Policy</a>
            </div>
        </div>
        <div style='margin-top:40px; color:#444; font-size:0.8rem; text-align:center;'>
            © 2026 Luser Ai OSS, Elmeddin Inc. | IP Address: {current_user_ip}
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 7. ADMIN PANEL (Yalnız Sənin Üçün) ---
if current_user_ip in ADMIN_IPS:
    with st.sidebar:
        st.markdown("<h2 style='color:#ff4500;'>👑 PATRON PANEL</h2>", unsafe_allow_html=True)
        st.write(f"Vəziyyət: **Aktiv**")
        if st.button("Söhbəti Təmizlə"): 
            st.session_state.messages = []
            st.rerun()
        if st.button("Statistikaları Sıfırla"):
            if os.path.exists(STATS_FILE): os.remove(STATS_FILE)
            st.rerun()
