import streamlit as st
import os
import requests
import json
import datetime
from gtts import gTTS
from io import BytesIO
import pandas as pd
from duckduckgo_search import DDGS # Pulsuz canlı axtarış üçün

# ==========================================
# 1. KONFİQURASİYA VƏ MOBİL OPTİMİZASİYA
# ==========================================
st.set_page_config(page_title="AI Programlan", page_icon="🐉", layout="wide")

# Mobil cihazlarda ağ ekran xətasını tamamilə yox edən CSS
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    /* Chat giriş sahəsi */
    .stChatInputContainer { 
        border: 1px solid #ffffff !important; 
        border-radius: 10px !important; 
        background-color: #000 !important;
        bottom: 20px !important;
    }
    .hero-title { font-size: 3.5rem; font-weight: 800; text-align: center; color: white; padding-top: 10px; }
    .hero-subtitle { text-align: center; color: #888; margin-bottom: 20px; font-size: 1.1rem; }
    
    /* Admin Cədvəli stili */
    .stTable { background-color: #111; border-radius: 10px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. GİZLİ DATA LOG SİSTEMİ (Local Host)
# ==========================================
LOG_FILE = "luser_database.json"
MY_IP = "94.20.98.116"

def get_ip():
    try: return requests.get('https://api.ipify.org').text
    except: return "Hidden"

user_ip = get_ip()

def save_visit(ip):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Hansı cihazla girdiyini təxmin etmək
    entry = {"Tarix": now, "IP": ip, "Status": "Online"}
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f: logs = json.load(f)
        except: logs = []
    logs.append(entry)
    with open(LOG_FILE, "w") as f: json.dump(logs, f)

save_visit(user_ip)

# ==========================================
# 3. KÖHNƏ LOQO VƏ BAŞLIQ BƏRPASI
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
st.markdown("<div class='hero-subtitle'>Universal SDK by Elmeddin | Live Web Search</div>", unsafe_allow_html=True)

# ==========================================
# 4. MODLAR VƏ DİL SEÇİMİ
# ==========================================
if "lang" not in st.session_state: st.session_state.lang = "az"

st.write("---")
c1, c2, c3 = st.columns(3)
if c1.button("🇦🇿 AZERBAİJAN"): st.session_state.lang = "az"
if c2.button("🇺🇸 ENGLİSH"): st.session_state.lang = "en"
if c3.button("🇷🇺 RUSSIAN"): st.session_state.lang = "ru"

selected_mode = st.radio("Sistem Modu:", 
    ["Hızlı (Sınırsız)", "Pro (15 AZN)", "Düşünməli (10 AZN)"], horizontal=True)

# Fayl Yükləmə (+)
st.file_uploader("Fayl, PDF və ya Şəkil (+)", type=['png', 'jpg', 'pdf', 'jpeg'])

# ==========================================
# 5. DÜNYA WEB TARAMA SİSTEMİ (No-Key AI)
# ==========================================
def web_search_ai(query):
    try:
        with DDGS() as ddgs:
            # Dünyadakı bütün veb saytlarda axtarış edir
            results = [r for r in ddgs.text(query, max_results=5)]
            if results:
                context = "\n".join([f"{res['title']}: {res['body']}" for res in results])
                return context
            else:
                return "Təəssüf ki, internetdə bu barədə məlumat tapılmadı."
    except Exception as e:
        return "Sistem hal-hazırda dünyanı taraya bilmir, bir azdan yoxla."

# ==========================================
# 6. CHAT VƏ ADMİN PANELİ (luserzz)
# ==========================================
if "messages" not in st.session_state: st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar="🐉" if m["role"]=="assistant" else "👤"):
        st.write(m["content"])

if prompt := st.chat_input("Dünyanı taramaq üçün bir şey yaz..."):
    
    # GİZLİ ADMİN PANELİ (luserzz + IP Kontrol)
    if prompt.lower() == "luserz" and user_ip == MY_IP:
        st.error("👑 PATRON GİRİŞİ TƏSDİQLƏNDİ. ADMİN PANELİ AÇILIR...")
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f: data = json.load(f)
            st.table(pd.DataFrame(data).tail(20)) # Son 20 girişi göstər
        else: st.write("Data hələ toplanmayıb.")
    
    else:
        # NORMAL İSTİFADƏÇİ ÜÇÜN WEB TARAMA
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"): st.write(prompt)

        with st.chat_message("assistant", avatar="🐉"):
            with st.spinner("🌍 Dünya vebləri taranır və ən düzgün cavab hazırlanır..."):
                # İnternetdən canlı datanı çəkirik
                final_answer = web_search_ai(prompt)
                st.write(final_answer)
                
                # Səsli Oxuma
                s_lang = 'tr' if st.session_state.lang == "az" else st.session_state.lang
                try:
                    tts = gTTS(text=final_answer[:300], lang=s_lang) # Çox uzun olsa kəsirik
                    fp = BytesIO()
                    tts.write_to_fp(fp)
                    st.audio(fp)
                except: pass
                
                st.session_state.messages.append({"role": "assistant", "content": final_answer})

# ==========================================
# 7. SOSİAL LİNKLƏR (@luser4x)
# ==========================================
st.markdown(f"""
    <div style='text-align: center; margin-top: 50px; border-top: 1px solid #222; padding-top: 20px;'>
        <a href='https://instagram.com/luser4x' target='_blank' style='color:white; margin:15px; text-decoration:none; font-weight:bold;'>INSTAGRAM</a>
        <a href='https://tiktok.com/@luser4x' target='_blank' style='color:white; margin:15px; text-decoration:none; font-weight:bold;'>TIKTOK</a>
        <p style='color:#333; font-size:11px; margin-top:15px;'>Local Server ID: {user_ip} | Elmeddin Edition</p>
    </div>
""", unsafe_allow_html=True)
