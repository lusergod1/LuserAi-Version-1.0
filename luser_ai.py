import streamlit as st
import os
import requests
import json
import time
from io import BytesIO
import base64

# Gerekli səs kitabxanası (Əgər xəta versə, deməli requirements.txt-yə gTTS yazmamısan)
try:
    from gtts import gTTS
    VOICE_ENABLED = True
except ImportError:
    VOICE_ENABLED = False

# ==========================================
# 1. SİSTEM KONFİQURASİYASI
# ==========================================
st.set_page_config(
    page_title="Luser Ai 1.0 - Ultimate Edition", 
    page_icon="🐉", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. TARGARYEN X VERCEL DİZAYN (CSS)
# ==========================================
st.markdown("""
    <style>
    /* Premium Qara və Qırmızı Arxa Plan */
    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(circle at top center, #2a0000 0%, #000000 80%) !important;
        color: #ffffff !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* Standart Streamlit elementlərini gizlət */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Qəhrəman (Hero) Başlığı */
    .hero-title {
        font-size: clamp(2.5rem, 8vw, 4rem);
        font-weight: 900;
        text-align: center;
        color: #ff4500;
        text-shadow: 0 0 25px rgba(255, 69, 0, 0.6), 0 0 5px #ffffff;
        letter-spacing: 6px;
        padding-top: 10px;
        margin-bottom: 5px;
        text-transform: uppercase;
    }
    .hero-subtitle {
        text-align: center;
        color: #aaaaaa;
        font-size: 1.2rem;
        margin-bottom: 40px;
    }

    /* Vercel Stilində Statistika Kartları */
    .stat-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 40px;
    }
    .stat-card {
        background-color: rgba(15, 15, 15, 0.9);
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        flex: 1;
        transition: all 0.3s ease;
    }
    .stat-card:hover { 
        border-color: #ff4500; 
        box-shadow: 0 0 20px rgba(255, 69, 0, 0.15); 
        transform: translateY(-2px);
    }
    .stat-value { font-size: 2.5rem; font-weight: 800; color: #ffffff; }
    .stat-label { font-size: 0.85rem; color: #888888; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px;}

    /* Chat və Footer */
    .stChatInputContainer { background-color: #050505 !important; border-top: 1px solid #ff4500 !important; }
    .footer-section { margin-top: 80px; padding: 40px 0; border-top: 1px solid #222; text-align: center; }
    .footer-links a { color: #888; text-decoration: none; margin: 0 15px; font-weight: 500; transition: 0.2s; font-size: 1.1rem;}
    .footer-links a:hover { color: #ff4500; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. IP QORUMASI VƏ TƏHLÜKƏSİZLİK
# ==========================================
ADMIN_IPS = ["94.20.98.116"]

def get_real_ip():
    try: 
        return requests.get('https://api.ipify.org', timeout=3).text
    except: 
        return "Unknown"

current_ip = get_real_ip()

# ==========================================
# 4. STATİSTİKA MÜHƏRRİKİ
# ==========================================
STATS_FILE = "stats.json"

def get_stats(increment_request=False):
    # Əgər fayl yoxdursa, başlanğıc rəqəmləri yarat
    if not os.path.exists(STATS_FILE):
        data = {"total_requests": 25400, "active_bots": 1, "contributors": 1}
    else:
        try:
            with open(STATS_FILE, "r") as f: data = json.load(f)
        except:
            data = {"total_requests": 25400, "active_bots": 1, "contributors": 1}
    
    # Hər mesajda sayğacı artır
    if increment_request:
        data["total_requests"] += 1
        with open(STATS_FILE, "w") as f: json.dump(data, f)
    return data

stats_data = get_stats()

# ==========================================
# 5. UI (GÖRÜNTÜ) BÖLMƏSİ
# ==========================================

# A. Loqo Sistemi (Böyük Xəta Qoruyucusu ilə)
def display_logo():
    if os.path.exists("images"):
        for f in os.listdir("images"):
            if "luser" in f.lower() or "nazli" in f.lower():
                st.image(os.path.join("images", f), width=70)
                return

col1, col2, col3 = st.columns([5,1,5])
with col2: display_logo()

# B. Başlıq
st.markdown("<div class='hero-title'>LUSER AI 1.0</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Universal AI Layer Powered by Elmeddin OSS</div>", unsafe_allow_html=True)

# C. Vercel Statistika Kartları
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats_data['total_requests']}</div><div class='stat-label'>Total Requests</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats_data['active_bots']}+</div><div class='stat-label'>Active Models</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats_data['contributors']}</div><div class='stat-label'>Contributors</div></div>", unsafe_allow_html=True)

st.write("---")

# ==========================================
# 6. SƏS VƏ CHAT MÜHƏRRİKİ (Core AI)
# ==========================================

# Səs yaratmaq üçün funksiya (Text-to-Speech)
def create_audio_player(text):
    if not VOICE_ENABLED: return None
    try:
        tts = gTTS(text=text, lang='tr') # 'tr' Türkcə ləhcəsi ilə oxuyur
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        return None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Keçmiş mesajları ekranda göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👨" if msg["role"] == "user" else "🐉"):
        st.markdown(msg["content"])
        # Əgər botun cavabıdırsa və audiosu varsa, səs pleyerini göstər
        if msg["role"] == "assistant" and "audio" in msg and msg["audio"] is not None:
            st.audio(msg["audio"], format="audio/mp3")

# Yeni Mesaj Girişi
if prompt := st.chat_input("Luser Ai-a sual ver və səsini eşit..."):
    
    # 1. Sayğacı artır
    get_stats(increment_request=True)
    
    # 2. İstifadəçi mesajını ekrana yaz
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨"):
        st.markdown(prompt)
    
    # 3. AI Analizi və Cavabı
    with st.chat_message("assistant", avatar="🐉"):
        with st.spinner("📡 Luser Core Düşünür və Səs Hazırlayır..."):
            API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
            try:
                # Pulsuz AI API çağırışı
                response = requests.post(API_URL, json={"inputs": prompt}, timeout=15)
                ai_text = response.json()[0]['generated_text']
            except:
                ai_text = "Salam Patron. Sistemdə hal-hazırda kiçik bir yüklənmə var. Mən həmişə səninləyəm!"
            
            # Səsi Yarat
            audio_data = create_audio_player(ai_text)
            
            # Ekrana yazdır və Səsi qoy
            st.markdown(ai_text)
            if audio_data:
                st.audio(audio_data, format="audio/mp3")
            
            # Yaddaşa sal
            st.session_state.messages.append({"role": "assistant", "content": ai_text, "audio": audio_data})

# ==========================================
# 7. FOOTER VƏ SOSİAL LİNKLƏR
# ==========================================
st.markdown("""
    <div class='footer-section'>
        <div class='footer-links'>
            <a href='https://instagram.com/lusergod' target='_blank'>INSTAGRAM</a>
            <a href='https://tiktok.com/@lusergod' target='_blank'>TIKTOK</a>
            <a href='https://discordapp.com/users/lusergod' target='_blank'>DISCORD</a>
        </div>
        <p style='margin-top:25px; color:#555; font-size:0.9rem;'>© 2026 LUSER AI OSS | DESIGNED BY ELMEDDIN</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 8. GİZLİ ADMIN PANELİ (Yalnız Sənin Üçün)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #ff4500;'>👑 LUSER CORE</h2>", unsafe_allow_html=True)
    
    if current_ip in ADMIN_IPS:
        st.success(f"Giriş Təsdiqləndi!\nIP: {current_ip}")
        st.write("---")
        if st.button("🗑️ Bütün Söhbəti Sil"):
            st.session_state.messages = []
            st.rerun()
        if st.button("🔄 Sayğacı Sıfırla"):
            if os.path.exists(STATS_FILE): os.remove(STATS_FILE)
            st.rerun()
        st.info("Sistem Statusu: Stabil & Səs Aktivdir.")
    else:
        st.info("Sistem Aktivdir. Ziyarətçi rejimi.")
