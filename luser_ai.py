import streamlit as st
import os
import requests
import time

# --- 1. KONFİQURASİYA VƏ BRENDİNQ ---
st.set_page_config(
    page_title="Luser Ai 1.0 - Targaryen Edition", 
    page_icon="🐉", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. TARGARYEN & NAZLI PREMİUM DİZAYN (CSS) ---
st.markdown("""
    <style>
    /* Tam ekran qara və qırmızı parıltı */
    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(circle, #2a0000 0%, #000000 100%) !important;
        color: white !important;
    }
    
    /* Header və Footer gizlətmək (Ağ boşluqları yox edir) */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] {background: rgba(0,0,0,0);}

    /* Luser Ai Neon Başlıq */
    .luser-title {
        font-size: clamp(2rem, 8vw, 3.5rem);
        font-weight: 900;
        text-align: center;
        color: #ff4500;
        text-shadow: 0 0 25px #ff4500, 0 0 5px #ffffff;
        letter-spacing: 8px;
        padding: 20px 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Sidebar dizaynı */
    [data-testid="stSidebar"] {
        background-color: #080808 !important;
        border-right: 1px solid #ff4500 !important;
    }

    /* Chat giriş sahəsi */
    .stChatInputContainer {
        background-color: #050505 !important;
        border-top: 1px solid #ff4500 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. IP TƏHLÜKƏSİZLİK SİSTEMİ ---
ADMIN_IPS = ["94.20.98.116"] # Sənin qeyd etdiyin IP

def get_real_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Unknown"

current_user_ip = get_real_ip()

# --- 4. LOQO VƏ BAŞLIQ ---
st.markdown("<div class='luser-title'>LUSER AI 1.0 VERSION</div>", unsafe_allow_html=True)

def display_logo():
    if os.path.exists("images"):
        for file in os.listdir("images"):
            if "luser" in file.lower() or "nazli" in file.lower():
                st.image(os.path.join("images", file), use_container_width=True)
                return
display_logo()

# --- 5. ADMIN PANEL (Yalnız Sənin Üçün) ---
with st.sidebar:
    st.markdown("<h1 style='color: #ff4500;'>🐉 LUSER CORE</h1>", unsafe_allow_html=True)
    
    if current_user_ip in ADMIN_IPS:
        st.success(f"Xoş gəldin, Patron! \n(IP: {current_user_ip})")
        with st.expander("👑 ADMIN PANEL"):
            if st.button("Söhbəti Sıfırla"):
                st.session_state.messages = []
                st.rerun()
            st.write("Sistem: **Stabil**")
            st.write("Brend: **Targaryen/Nazlı**")
    else:
        st.info("Luser Ai 1.0 Aktivdir.")
    
    st.divider()
    st.caption("Yaradıcı: Elmeddin")

# --- 6. PULSUZ AI MÜHƏRRİKİ (Hugging Face) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Keçmiş mesajları göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Yeni mesaj girişi
if prompt := st.chat_input("Luser Ai üçün bir əmr ver..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.status("📡 Analiz edilir...", expanded=False):
            # Pulsuz və Limitless Model
            API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
            try:
                response = requests.post(API_URL, json={"inputs": prompt}, timeout=10)
                ai_response = response.json()[0]['generated_text']
            except:
                ai_response = "Luser Ai: Hazırda serverlərdə kiçik bir gecikmə var, mən həmişə buradayam!"
        
        st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
