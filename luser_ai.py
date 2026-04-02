import streamlit as st
import os
import requests
import json
import datetime
from gtts import gTTS
from io import BytesIO
import pandas as pd
from duckduckgo_search import DDGS

# ==========================================
# 0. SİSTEM VƏ MOBİL DİZAYN TƏNZİMLƏMƏSİ
# ==========================================
st.set_page_config(page_title="AI Programlan", page_icon="🐉", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    .hero-title { font-size: 3rem; font-weight: 900; text-align: center; color: white; margin-top: 10px; }
    .hero-subtitle { text-align: center; color: #888; margin-bottom: 20px; font-size: 1.1rem; }
    .section-title { font-size: 2rem; font-weight: bold; color: #ff4500; border-bottom: 2px solid #333; padding-bottom: 10px; margin-top: 40px; margin-bottom: 20px;}
    .info-box { background-color: #111; padding: 20px; border-radius: 10px; border: 1px solid #333; margin-bottom: 15px;}
    .stChatInputContainer { border: 1px solid #ffffff !important; border-radius: 10px !important; background-color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. GİZLİ DATA LOG SİSTEMİ
# ==========================================
LOG_FILE = "luser_database.json"

def get_ip():
    try: return requests.get('https://api.ipify.org').text
    except: return "Hidden"

user_ip = get_ip()

def save_visit(ip):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"Tarix": now, "IP": ip, "Status": "Online"}
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f: logs = json.load(f)
        except: logs = []
    # Eyni IP ard-arda yazılmasın deyə kiçik yoxlama
    if not logs or logs[-1].get("IP") != ip:
        logs.append(entry)
        with open(LOG_FILE, "w") as f: json.dump(logs, f)

save_visit(user_ip)

# Yan Paneldə (Sidebar) Gizli Giriş
st.sidebar.markdown("<h3 style='color:white;'>Sistem Girişi</h3>", unsafe_allow_html=True)
admin_pass = st.sidebar.text_input("Şifrə:", type="password")

# ==========================================
# SEKSİYA 1: LOQO VƏ AI CHAT EKRANI
# ==========================================
def display_old_logo():
    if os.path.exists("images"):
        for f in os.listdir("images"):
            if any(x in f.lower() for x in ["luser", "nazli"]):
                st.image(os.path.join("images", f), width=130)
                return

col_l1, col_l2, col_l3 = st.columns([5,2,5])
with col_l2: display_old_logo()

st.markdown("<div class='hero-title'>AI Programlan</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Universal SDK by Elmeddin | Seksya 1</div>", unsafe_allow_html=True)

# Dil və Mod Seçimi
c1, c2, c3 = st.columns(3)
if "lang" not in st.session_state: st.session_state.lang = "az"
if c1.button("🇦🇿 AZ"): st.session_state.lang = "az"
if c2.button("🇺🇸 EN"): st.session_state.lang = "en"
if c3.button("🇷🇺 RU"): st.session_state.lang = "ru"

st.file_uploader("Fayl, PDF və ya Şəkil yüklə (+)", type=['png', 'jpg', 'pdf'])

# Chat Mühərriki və Veb Tarama
def web_search_ai(query):
    try:
        # Daha stabil axtarış üçün max_results azaldıldı
        results = DDGS().text(query, max_results=2)
        if results:
            context = "\n\n".join([f"**{r['title']}**\n{r['body']}" for r in results])
            return f"🌍 **Dünya Vebindən Tapılan Nəticələr:**\n\n{context}"
        else:
            return "İnternetdə bu suala uyğun dəqiq məlumat tapılmadı. Fərqli sözlərlə cəhd et, Patron."
    except Exception as e:
        return "Sistem hal-hazırda webə qoşula bilmir (DuckDuckGo bloklaması). Bir neçə saniyə sonra yenidən cəhd et."

if "messages" not in st.session_state: st.session_state.messages = []

# Chat Ekranı
for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar="🐉" if m["role"]=="assistant" else "👤"):
        st.write(m["content"])

if prompt := st.chat_input("Dünyanı taramaq üçün sual ver..."):
    
    # İKİ MƏRHƏLƏLİ ADMİN PANELİ (luserabi + luserzz)
    if prompt.lower() == "luserzz" and admin_pass == "luserabi":
        st.error("👑 İKİ MƏRHƏLƏLİ TƏSDİQ UĞURLU! ADMİN PANELİ AÇILIR...")
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f: data = json.load(f)
            st.table(pd.DataFrame(data).tail(30)) # Son 30 girişi cədvəldə göstər
        else: 
            st.write("Sistemdə hələ heç bir data yoxdur.")
    else:
        # NORMAL CHAT
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"): st.write(prompt)

        with st.chat_message("assistant", avatar="🐉"):
            with st.spinner("🌍 Məlumatlar axtarılır..."):
                final_answer = web_search_ai(prompt)
                st.write(final_answer)
                
                # Səsli Oxuma (Hər dildə)
                s_lang = 'tr' if st.session_state.lang == "az" else st.session_state.lang
                try:
                    # Səsli oxunacaq mətni təmizləyirik və qısaldırıq ki, xəta verməsin
                    clean_text = final_answer.replace("*", "").replace("🌍 Dünya Vebindən Tapılan Nəticələr:", "")[:400]
                    tts = gTTS(text=clean_text, lang=s_lang)
                    fp = BytesIO()
                    tts.write_to_fp(fp)
                    st.audio(fp)
                except: pass
                
                st.session_state.messages.append({"role": "assistant", "content": final_answer})

# ==========================================
# SEKSİYA 2: STATİSTİKA VƏ MODLARIN İZAHA
# ==========================================
st.markdown("<div class='section-title'>SEKSİYA 2: Sistem Statusu və Modlar</div>", unsafe_allow_html=True)

# Dinamik Aktiv İstifadəçi Sayı
try:
    with open(LOG_FILE, "r") as f:
        total_users = len(json.load(f))
except: total_users = 1

st.markdown(f"""
    <div class='info-box'>
        <h2 style='color: white; margin:0;'>🟢 Aktiv Ziyarətçilər: {total_users * 3} </h2>
        <p style='color: #888; font-size: 0.9rem;'>Son 24 saat ərzində sistemə bağlanan unikal cihazlar.</p>
    </div>
""", unsafe_allow_html=True)

# Modların İzahı
st.markdown("""
    <div class='info-box'>
        <h3 style='color: #ff4500;'>⚡ Hızlı Mod (Sınırsız)</h3>
        <p style='color: white;'>Gündəlik sürətli axtarışlar üçündür. Saniyələr içində qısa və konkret cavablar verir. Ödənişsizdir və hər kəs istifadə edə bilər.</p>
        
        <h3 style='color: #ff4500;'>👑 Pro Mod (15 AZN)</h3>
        <p style='color: white;'>Daha geniş məlumat bazasına daxil olur. Kod yazmaq, uzun məqalələr hazırlamaq və daha dəqiq analizlər etmək üçün nəzərdə tutulub. Sürətli və səhvsizdir.</p>
        
        <h3 style='color: #ff4500;'>🧠 Düşünməli Mod (10 AZN)</h3>
        <p style='color: white;'>Riyazi və məntiqi tapşırıqlar üçün nəzərdə tutulub. Addım-addım düşünərək sualı həll edir. Ən yaxşı və ən məntiqi cavabı tapana qədər analiz edir.</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# SEKSİYA 3: SOSİAL MEDİA VƏ ƏLAQƏ
# ==========================================
st.markdown("<div class='section-title'>SEKSİYA 3: Əlaqə və Tərəfdaşlıq</div>", unsafe_allow_html=True)

st.markdown(f"""
    <div style='text-align: center; padding: 30px; background-color: #111; border-radius: 10px; border: 1px solid #333;'>
        <h3 style='color: white;'>Luser Ai Sahibinə Qoşulun</h3>
        <p style='color: #888; margin-bottom: 20px;'>Yeniliklərdən anında xəbərdar olmaq və dəstək üçün izləyin:</p>
        
        <a href='https://instagram.com/luser4x' target='_blank' style='display: inline-block; padding: 10px 20px; background-color: #E1306C; color: white; text-decoration: none; border-radius: 5px; margin: 10px; font-weight: bold;'>📸 INSTAGRAM (@luser4x)</a>
        
        <a href='https://tiktok.com/@luser4x' target='_blank' style='display: inline-block; padding: 10px 20px; background-color: #000000; color: white; border: 1px solid white; text-decoration: none; border-radius: 5px; margin: 10px; font-weight: bold;'>🎵 TIKTOK (@luser4x)</a>
        
        <p style='color:#444; font-size:12px; margin-top:30px;'>Server Local IP: {user_ip} | © 2026 AI Programlan</p>
    </div>
""", unsafe_allow_html=True)
