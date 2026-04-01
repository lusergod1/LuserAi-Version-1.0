import streamlit as st
import os
import requests
import json
import time
from io import BytesIO
import base64

# Gerekli səs kitabxanası (Requriements.txt-yə gTTS yazılmalıdır)
try:
    from gtts import gTTS
    VOICE_ENABLED = True
except ImportError:
    VOICE_ENABLED = False

# ==========================================
# 1. SİSTEM KONFİQURASİYASI (Eyni saxla, başlığı dəyiş)
# ==========================================
st.set_page_config(
    page_title="AI Programlan - Universal SDK", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. image_9.png DİZAYNI (CSS) - Yenilə
# ==========================================
# Şəkildəki tünd qara fon, ağ şriftlər və ağ kənarlı elementlər
st.markdown("""
    <style>
    /* Premium Qara Fon (Şəkildəki kimi) */
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* Standart Streamlit elementlərini gizlət */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] {background: rgba(0,0,0,0);}

    /* Hero (Qəhrəman) Başlığı - Ağ və Sadə (Şəkildəki kimi) */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        letter-spacing: -1px;
        padding-top: 50px;
        margin-bottom: 5px;
        text-transform: none; /* Şəkildəki kimi qalın, ağ, normal */
    }
    .hero-subtitle {
        text-align: center;
        color: #888888;
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 30px;
    }
    
    /* Dil Seçimi Düymələri (AZ, EN, RU) - Sadə outline style */
    .language-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 40px;
    }
    .language-button {
        background-color: transparent;
        border: 1px solid #ffffff;
        border-radius: 4px;
        color: #ffffff;
        padding: 8px 16px;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s, color 0.2s;
    }
    .language-button:hover {
        background-color: #ffffff;
        color: #000000;
    }

    /* Statistika Kartları - Ağ Kənarlı (Şəkildəki kimi) */
    .stat-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 40px;
    }
    .stat-card {
        background-color: #000000;
        border: 1px solid #ffffff;
        border-radius: 8px;
        padding: 25px;
        text-align: center;
        flex: 1;
    }
    .stat-value { font-size: 2.8rem; font-weight: 800; color: #ffffff; margin-bottom: 5px;}
    .stat-label { font-size: 0.9rem; color: #ffffff; text-transform: none; letter-spacing: 0px;}

    /* Chat Giriş Sahəsi (Vercel Style, ağ kənarlı) - Şəkildəki daxiletmə sahəsinə uyğun */
    .stChatInputContainer {
        background-color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 8px !important;
        padding: 5px 10px !important;
    }
    
    /* Chat daxilindəki düymə */
    [data-testid="stChatInputButton"] {
        border: none !important;
        background: none !important;
        color: #ffffff !important;
        right: 15px !important;
        top: 15px !important;
    }
    [data-testid="stChatInputButton"] svg {
        fill: #ffffff !important;
    }
    
    /* Footer */
    .footer-section { margin-top: 80px; padding: 40px 0; border-top: 1px solid #222; text-align: center; }
    .footer-links a { color: #888; text-decoration: none; margin: 0 15px; font-weight: 500; transition: 0.2s; font-size: 1.1rem;}
    .footer-links a:hover { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. IP QORUMASI VƏ TƏHLÜKƏSİZLİK (Eyni saxla)
# ==========================================
ADMIN_IPS = ["94.20.98.116"]

def get_real_ip():
    try: 
        return requests.get('https://api.ipify.org', timeout=3).text
    except: 
        return "Unknown"

current_ip = get_real_ip()

# ==========================================
# 4. STATİSTİKA MÜHƏRRİKİ (Eyni saxla)
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
# 5. UI (GÖRÜNTÜ) BÖLMƏSİ (Yenilə)
# ==========================================

# Loqo Sistemi (Böyük Xəta Qoruyucusu ilə - Eyni saxla, bir az ölçüsünü azalt)
def display_logo():
    if os.path.exists("images"):
        for f in os.listdir("images"):
            if "luser" in f.lower() or "nazli" in f.lower():
                # Şəkildəki loqo daha təmiz görünür, ölçüsünü bir az azaldıram
                st.image(os.path.join("images", f), width=60)
                return

# A. Loqo və Başlıq (image_9.png strukturuna uyğun)
col1, col2, col3 = st.columns([5,1,5])
with col2: 
    # Dil düymələrinin dərhal üstünə loqo yerləşdirirəm
    st.markdown("<div style='display: flex; justify-content: center; margin-bottom: -30px;'>", unsafe_allow_html=True)
    display_logo()
    st.markdown("</div>", unsafe_allow_html=True)

# Şəkildəki böyük, qalın, ağ "AI Programlan" başlığı
st.markdown("<div class='hero-title'>AI Programlan</div>", unsafe_allow_html=True)
# Şəkildəki "Universal SDK by Elmeddin" alt başlığı
st.markdown("<div class='hero-subtitle'>Universal SDK by Elmeddin</div>", unsafe_allow_html=True)

# Dil Seçimi Düymələri (AZ, EN, RU) - Sadəcə UI dizayn
st.markdown("""
    <div class='language-container'>
        <button class='language-button'>AZ</button>
        <button class='language-button'>EN</button>
        <button class='language-button'>RU</button>
    </div>
""", unsafe_allow_html=True)

# B. Statistika Kartları (Ağ Kənarlı - image_9.png stili)
c1, c2, c3 = st.columns(3)
# Mövcud sayğac məlumatlarını şəkildəki stildə göstər
with c1: 
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats_data['total_requests']}</div><div class='stat-label'>Total Requests</div></div>", unsafe_allow_html=True)
with c2: 
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats_data['active_bots']}+</div><div class='stat-label'>Active Models</div></div>", unsafe_allow_html=True)
with c3: 
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats_data['contributors']}</div><div class='stat-label'>Contributors</div></div>", unsafe_allow_html=True)

# C. Chat Input (Kənarı ağ və qırmızı etmək üçün CSS) - image_9.png daxiletmə sahəsinə uyğun
st.write("---")

# ==========================================
# 6. SƏS VƏ CHAT MÜHƏRRİKİ (Core AI - Eyni saxla)
# ==========================================

# Səs yaratmaq üçün funksiya (Text-to-Speech)
def create_audio_player(text):
    if not VOICE_ENABLED: return None
    try:
        tts = gTTS(text=text, lang='tr') # Türkcə səs ləhcəsi
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
    # Avatarı image_9.png-a uyğunlaşdırmaq üçün bir az daha təmiz etmək
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
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
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # 3. AI Analizi və Cavabı
    with st.chat_message("assistant", avatar="🤖"):
        # Şəkildəki sadə tərəfə uyğun olaraq, səs hazırlama mətnini daha sadə etmək
        with st.spinner("Analyzing and Generating Voice..."):
            API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
            try:
                # Pulsuz AI API çağırışı
                response = requests.post(API_URL, json={"inputs": prompt}, timeout=15)
                ai_text = response.json()[0]['generated_text']
            except:
                ai_text = "Analyzing your request... AI core is preparing a response. Please stand by."
            
            # Səsi Yarat
            audio_data = create_audio_player(ai_text)
            
            # Ekrana yazdır və Səsi qoy
            st.markdown(ai_text)
            if audio_data:
                st.audio(audio_data, format="audio/mp3")
            
            # Yaddaşa sal
            st.session_state.messages.append({"role": "assistant", "content": ai_text, "audio": audio_data})

# ==========================================
# 7. FOOTER VƏ SOSİAL LİNKLƏR (Eyni saxla)
# ==========================================
st.markdown("""
    <div class='footer-section'>
        <div class='footer-links'>
            <a href='https://instagram.com/lusergod' target='_blank'>INSTAGRAM</a>
            <a href='https://tiktok.com/@lusergod' target='_blank'>TIKTOK</a>
            <a href='https://discordapp.com/users/lusergod' target='_blank'>DISCORD</a>
        </div>
        <p style='margin-top:25px; color:#555; font-size:0.9rem;'>© 2026 AI Programlan OSS | DESIGNED BY ELMEDDIN</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 8. GİZLİ ADMIN PANELİ (Yalnız Sənin Üçün - Eyni saxla, başlığı dəyiş)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #ffffff;'>🤖 AI PROGRAMLAN</h2>", unsafe_allow_html=True)
    
    if current_ip in ADMIN_IPS:
        st.success(f"Access Granted!\nIP: {current_ip}")
        st.write("---")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        if st.button("🔄 Reset Sayğac"):
            if os.path.exists(STATS_FILE): os.remove(STATS_FILE)
            st.rerun()
        st.info("System Status: Stable & Voice Active.")
    else:
        st.info("System Active. Visitor Mode.")
