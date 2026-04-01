import streamlit as st
import os
import requests
import time
import json

# --- 1. KONFİQURASİYA VƏ BRENDİNQ ---
st.set_page_config(
    page_title="Luser Ai 1.0 - Vercel Edition", 
    page_icon="🐉", 
    layout="wide",
    initial_sidebar_state="collapsed" # İlkin olaraq sidebar gizli
)

# --- 2. VERCEL-TARGARYEN DİZAYN (CSS) ---
st.markdown("""
    <style>
    /* Vercel Black & Targaryen Red */
    .stApp {
        background-color: #000000 !important;
        color: white !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol" !important;
    }
    
    /* Header/Footer gizlətmək */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* 1-ci SS: Professional Giriş Başlığı */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        color: white;
        letter-spacing: -2px;
        padding-top: 50px;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 1.5rem;
        text-align: center;
        color: #888888;
        font-weight: 400;
        margin-bottom: 50px;
        line-height: 1.6;
    }
    
    /* 2-ci SS: Statistika Kartları */
    .stat-card {
        background-color: #0d0d0d;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        margin-bottom: 20px;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .stat-card:hover {
        border-color: #ff4500; /* Targaryen Red hover effect */
        box-shadow: 0 0 15px rgba(255, 69, 0, 0.2);
    }
    .stat-value {
        font-size: 4rem;
        font-weight: 700;
        color: white;
    }
    .stat-label {
        font-size: 1rem;
        color: #888888;
        margin-top: 10px;
    }

    /* 3-cü SS: Footer Linkləri */
    .footer-section {
        margin-top: 100px;
        border-top: 1px solid #333333;
        padding: 50px 0;
        color: #888888;
    }
    .footer-links a {
        color: #888888;
        text-decoration: none;
        margin-right: 20px;
        transition: color 0.2s;
    }
    .footer-links a:hover {
        color: #ff4500;
    }
    .footer-copyright {
        margin-top: 30px;
        color: #666666;
    }

    /* Chat giriş sahəsi (Vercel Style) */
    .stChatInputContainer {
        background-color: #050505 !important;
        border-top: 1px solid #333333 !important;
        border-radius: 10px !important;
        box-shadow: none !important;
    }
    
    /* Sidebar dizaynı */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a !important;
        border-right: 1px solid #333333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. IP TƏHLÜKƏSİZLİK SİSTEMİ ---
ADMIN_IPS = ["94.20.98.116"] # Sənin IP

def get_real_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Unknown"

current_user_ip = get_real_ip()

# --- 4. STATİSTİKA SAYĞACI (Fayl əsaslı) ---
STATS_FILE = "stats.json"

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"total_requests": 0, "weekly_active_bots": 1, "contributors": 1, "models_active": 1}
    with open(STATS_FILE, "r") as f:
        return json.load(f)

def update_stats():
    stats = load_stats()
    stats["total_requests"] += 1
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)
    return stats

# İlkin yükləmə
stats_data = load_stats()

# --- 5. ƏSAS SƏHİFƏ GÖRÜNTÜSÜ (Vercel Style) ---
# Yuxarı hissə (Loqo və Başlıq)
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

# 1-ci istək: Balaca Loqo
def display_small_logo():
    if os.path.exists("images"):
        for file in os.listdir("images"):
            if "luser" in file.lower() or "nazli" in file.lower():
                # Vercel-dəki loqo kimi balaca və təmiz (50px)
                st.image(os.path.join("images", file), width=50)
                return
display_small_logo()

# 1-ci SS: Professional Başlıq
st.markdown("<div class='hero-title'>Luser Ai Layer for building agentic apps</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>A unified Luser SDK for building Ai apps with modern streaming, and multi-model support—powered by Elmeddin OSS.</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 2-ci SS: Statistika Kartları
col1, col2, col3, col4 = st.columns(4)

def stat_card(value, label, col):
    with col:
        st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-value'>{value}</div>
                <div class='stat-label'>{label}</div>
            </div>
        """, unsafe_allow_html=True)

# Dinamik olaraq sayğacları göstər
stat_card(f"{stats_data['total_requests']/1000000:.1f}M", "Total requests", col1)
stat_card(f"{stats_data['weekly_active_bots']}+", "Weekly active bots", col2) # Nümunə: 1+
stat_card(f"{stats_data['contributors']}", "Contributors", col3)
stat_card(f"{stats_data['models_active']}", "Models active", col4)

st.write("---")

# --- 6. PULSUZ AI MÜHƏRRİKİ (Hugging Face) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat mesajlarını göstər (Professional chat mühiti üçün bir az fərqli dizayn)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👨" if msg["role"] == "user" else "🐉"):
        st.markdown(msg["content"])

# Yeni mesaj girişi
if prompt := st.chat_input("Luser Ai-a bir şey yaz..."):
    # Mesaj göndərildikdə sayğacı artır
    stats_data = update_stats()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨"):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="🐉"):
        with st.status("📡 Analiz edilir...", expanded=False):
            # Pulsuz AI modeli
            API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
            try:
                response = requests.post(API_URL, json={"inputs": prompt}, timeout=10)
                ai_response = response.json()[0]['generated_text']
            except:
                ai_response = "Luser Ai: Hazırda analiz davam edir... Bir azdan yenidən yoxlayın."
        
        st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

# --- 7. FOOTER: SOYAL LİNKLƏR (3-cü SS) ---
st.markdown("""
    <div class='footer-section'>
        <div style='text-align: center; margin-bottom: 30px; font-size: 1.2rem; color: #ff4500; font-weight: bold;'>OSS Community</div>
        <div style='display: flex; justify-content: center; flex-wrap: wrap; margin-bottom: 20px;' class='footer-links'>
            <a href='https://instagram.com/lusergod' target='_blank'>Instagram</a>
            <a href='https://tiktok.com/@lusergod' target='_blank'>TikTok</a>
            <a href='https://discordapp.com/users/lusergod' target='_blank'>Discord Account</a>
            <a href='#' target='_blank'>YouTube</a>
        </div>
        <div style='text-align: center;' class='footer-copyright'>
            © 2026 Luser Ai OSS, Elmeddin Inc. All rights reserved.
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 8. ADMIN PANEL (SIDEBAR - Yalnız IP-n üçün) ---
with st.sidebar:
    st.markdown("<h1 style='color: #ff4500;'>🐉 ADMIN</h1>", unsafe_allow_html=True)
    
    if current_user_ip in ADMIN_IPS:
        st.success(f"Patron! \nIP: {current_user_ip}")
        if st.button("Söhbəti Sıfırla"):
            st.session_state.messages = []
            st.rerun()
        if st.button("Sayğacı Sıfırla"):
            stats_data = {"total_requests": 0, "weekly_active_bots": 1, "contributors": 1, "models_active": 1}
            with open(STATS_FILE, "w") as f:
                json.dump(stats_data, f)
            st.rerun()
        st.write("Sayğac:", stats_data['total_requests'])
    else:
        st.info("Luser Ai 1.0 Active.")
