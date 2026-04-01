import streamlit as st
import os
import requests
import time

# --- KONFİQURASİYA ---
st.set_page_config(page_title="Luser Ai 1.0 Version", page_icon="🚀", layout="wide")

# --- SƏNİN IP ÜNVANIN (Şəkildən götürüldü) ---
ADMIN_IPS = ["94.20.98.116"]

# --- CİHAZIN IP-SİNİ YOXLA ---
def get_user_ip():
    try:
        # Real IP-ni çəkmək üçün servis
        return requests.get('https://api.ipify.org').text
    except:
        return None

user_ip = get_user_ip()

# --- FULL DARK MODE & TARGARYEN CSS ---
st.markdown("""
    <style>
    /* Bütün səhifəni qaralt */
    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(circle, #2a0000 0%, #000000 100%) !important;
    }
    
    /* Gereksiz ağlıqları gizlə */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Luser Ai Başlığı */
    .luser-glow {
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        color: #ff4500;
        text-shadow: 0 0 20px #ff4500;
        letter-spacing: 5px;
        padding: 20px 0;
    }

    /* Chat giriş sahəsi */
    .stChatInputContainer {
        background-color: #050505 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ANA PANEL ---
st.markdown("<div class='luser-glow'>LUSER AI 1.0 VERSION</div>", unsafe_allow_html=True)

# --- LOQO SİSTEMİ ---
def find_logo():
    if os.path.exists("images"):
        for f in os.listdir("images"):
            if "luser" in f.lower():
                return os.path.join("images", f)
    return None

logo_path = find_logo()
if logo_path:
    st.image(logo_path, use_container_width=True)

# --- ADMIN PANEL SİSTEMİ (IP KİLİDİ) ---
if user_ip in ADMIN_IPS:
    st.sidebar.success(f"Xoş gəldin, Patron! (IP: {user_ip})")
    with st.sidebar.expander("👑 ADMIN PANEL"):
        st.write("Sistem tənzimləmələri:")
        if st.button("Söhbətləri Sıfırla"):
            st.session_state.messages = []
            st.rerun()
        st.info("Bu panel yalnız sənin cihazında görünür.")
else:
    # Kənar şəxslər üçün görünən hissə
    st.sidebar.info("Luser Ai 1.0 Aktivdir.")
    # st.sidebar.write(f"Ziyarətçi IP: {user_ip}") # Yoxlamaq istəsən bunu aktiv edə bilərsən

# --- CHAT SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Luser Ai-a bir şey yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.status("📡 Analiz edilir...", expanded=False):
            # Pulsuz AI modeli (Hugging Face)
            API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
            try:
                response = requests.post(API_URL, json={"inputs": prompt})
                res = response.json()[0]['generated_text']
            except:
                res = "Luser Ai: Hazırda serverlərdə yüklənmə var, bir azdan yenidən yoxlayın."
        
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
