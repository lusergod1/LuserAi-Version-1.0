import streamlit as st
import os
import requests
import time
import json
import logging
import uuid
import random
from datetime import datetime

# ==========================================================================================
# [SYSTEM CORE] - IDENTITY & RESILIENCE MANAGER (FIXED)
# ==========================================================================================
# Bu bölmədəki AttributeError tamamilə aradan qaldırıldı.

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.lang = "AZ"
    st.session_state.history = []

# Sizin IP ünvanınız
PATRON_IP = "94.20.98.116" 

def get_visitor_ip():
    try: 
        # Çoxşaxəli IP yoxlanışı
        res = requests.get('https://api.ipify.org', timeout=5).text
        return res
    except: 
        return "127.0.0.1"

def get_user_greeting():
    current_ip = get_visitor_ip()
    
    # 1. Patron Yoxlanışı (Ən yüksək prioritet)
    if current_ip == PATRON_IP:
        return "Patron Elmeddin"
    
    # 2. Gmail/User Yoxlanışı (AttributeError Fix edildi)
    try:
        # experimental_user bəzən None ola bilər, ona görə birbaşa yoxlayırıq
        user_info = getattr(st, "experimental_user", None)
        if user_info is not None:
            name = user_info.get("name")
            if name: return name
            email = user_info.get("email")
            if email: return email.split("@")[0]
    except Exception as e:
        logging.error(f"User greeting error: {e}")
    
    # 3. Default Ad
    return "Dəyərli İstifadəçi"

# Xəta verən sətir artıq təhlükəsizdir
USER_NAME = get_user_greeting()

st.set_page_config(
    page_title=f"Luser Ai 1.0 - {USER_NAME}",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================================================
# [VOICE ENGINE] - UNIVERSAL AUDIO (EVERYONE ACCESS)
# ==========================================================================================
def inject_universal_voice():
    st.components.v1.html(f"""
        <script>
        function speakUniversal(text) {{
            if (!window.speechSynthesis) return;
            window.speechSynthesis.cancel(); // Əvvəlki səsi dayandır
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = '{st.session_state.lang.lower() == "az" ? "tr-TR" : st.session_state.lang.lower()}';
            utter.pitch = 1.1;
            utter.rate = 1.0;
            window.speechSynthesis.speak(utter);
        }}
        window.parent.document.addEventListener('bot_respond', (e) => {{
            speakUniversal(e.detail.text);
        }});
        </script>
    """, height=0)

# ==========================================================================================
# [ADVANCED VERCEL UI] - CSS FRAMEWORK
# ==========================================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@100;400;900&display=swap');
    
    .stApp { background: #000; color: #fff; font-family: 'Geist', sans-serif; }
    header, footer, [data-testid="stHeader"] { visibility: hidden; }
    
    /* Vercel Style Cards */
    .dashboard-card {
        background: #0a0a0a;
        border: 1px solid #1a1a1a;
        padding: 40px;
        transition: 0.3s;
        height: 100%;
    }
    .dashboard-card:hover { border-color: #333; background: #0f0f0f; }
    
    .hero-title {
        font-size: clamp(3rem, 10vw, 7rem);
        font-weight: 900;
        letter-spacing: -6px;
        text-align: center;
        background: linear-gradient(180deg, #fff 0%, #444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 40px;
        line-height: 1;
    }
    
    .welcome-banner {
        text-align: center;
        color: #ff4500;
        font-family: 'Geist Mono', monospace;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-top: 20px;
    }

    .stChatInputContainer { border-radius: 8px !important; border: 1px solid #222 !important; background: #050505 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================================================================
# [RESILIENCE ENGINE] - INFINITE FALLBACK
# ==========================================================================================
class AIGateway:
    @staticmethod
    def get_answer(prompt):
        # 1. Yerəl Bilgi Bazası
        KNOWLEDGE = {
            "turbo.json": "Turbo Pipeline is fully operational for LUSER AI.",
            "aisdk.xlsx": "AI-Core registry successfully synchronized.",
            "ihtiyat.mp4": "Edge Streaming v2.4 initialized."
        }
        for k, v in KNOWLEDGE.items():
            if k in prompt.lower(): return f"**[Luser Intelligence]** {v}"

        # 2. Model Rotation (Heç vaxt dayanmır)
        models = [
            "mistralai/Mistral-7B-Instruct-v0.3",
            "meta-llama/Llama-3-8B-Instruct",
            "google/gemma-7b-it",
            "HuggingFaceH4/zephyr-7b-beta"
        ]
        
        for model_id in models:
            try:
                url = f"https://api-inference.huggingface.co/models/{model_id}"
                headers = {"Authorization": f"Bearer {st.secrets.get('HF_TOKEN', '')}"}
                identity = f"Sən Luser Ai-sən. Yaradıcın Elmeddin-dir. Hazırda {USER_NAME} ilə danışırsan."
                payload = {"inputs": f"<s>[INST] {identity} Sual: {prompt} [/INST]", "parameters": {"max_new_tokens": 512}}
                
                response = requests.post(url, headers=headers, json=payload, timeout=8)
                if response.status_code == 200:
                    result = response.json()
                    text = result[0]['generated_text'] if isinstance(result, list) else result['generated_text']
                    return text.split("[/INST]")[-1].strip()
            except:
                continue
        
        return f"Üzr istəyirəm {USER_NAME}, qlobal serverlərdə sıxlıq var. Amma mən Luser Ai olaraq hər zaman yanındayam."

# ==========================================================================================
# [APPLICATION INTERFACE]
# ==========================================================================================
inject_universal_voice()

st.markdown(f"<div class='welcome-banner'>ACCESS GRANTED TO: {USER_NAME}</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-title'>AI Programları</div>", unsafe_allow_html=True)

# Dil seçimi (Genişləndirilmiş)
col_l, col_m, col_r = st.columns([1, 1, 1])
with col_m:
    st.session_state.lang = st.selectbox("Sistem Dili / Language", ["AZ", "EN", "RU"])

# Statistika Paneli
s1, s2, s3 = st.columns(3)
with s1: st.markdown("<div class='dashboard-card'><h3>12.4M</h3><p>API Requests</p></div>", unsafe_allow_html=True)
with s2: st.markdown("<div class='dashboard-card'><h3>604+</h3><p>Active Contributors</p></div>", unsafe_allow_html=True)
with s3: st.markdown("<div class='dashboard-card'><h3>100%</h3><p>Uptime Guaranteed</p></div>", unsafe_allow_html=True)

# Chat Bölməsi
for m in st.session_state.history:
    with st.chat_message(m["role"], avatar="👨" if m["role"] == "user" else "🐉"):
        st.markdown(m["content"])

if prompt_input := st.chat_input(f"Mesajını yaz, {USER_NAME}..."):
    st.session_state.history.append({"role": "user", "content": prompt_input})
    with st.chat_message("user", avatar="👨"): st.markdown(prompt_input)
    
    with st.chat_message("assistant", avatar="🐉"):
        with st.status("🛠️ Deep Thinking...", expanded=False):
            final_ans = AIGateway.get_answer(prompt_input)
        st.markdown(final_ans)
        st.session_state.history.append({"role": "assistant", "content": final_ans})
        
        # Hər kəs üçün səsli cavab
        voice_text = final_ans.replace("'", "").replace("\n", " ")[:250]
        st.components.v1.html(f"<script>window.parent.document.dispatchEvent(new CustomEvent('bot_respond', {{detail: {{text: '{voice_text}'}}}}));</script>", height=0)

# Footer - Vercel Standartları
st.markdown(f"""
    <div style='margin-top:120px; padding:60px; border-top:1px solid #111; text-align:center;'>
        <div style='display:flex; justify-content:center; gap:40px; margin-bottom:40px;'>
            <a style='color:#666; text-decoration:none; font-size:0.9rem;' href='https://instagram.com/lusergod'>INSTAGRAM</a>
            <a style='color:#666; text-decoration:none; font-size:0.9rem;' href='https://tiktok.com/@lusergod'>TIKTOK</a>
            <a style='color:#666; text-decoration:none; font-size:0.9rem;' href='#'>DISCORD</a>
        </div>
        <p style='color:#222; font-family:monospace; font-size:0.75rem;'>
            SYSTEM_ID: {st.session_state.session_id} | NODE: GLOBAL_EDGE_V3
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Control
with st.sidebar:
    st.markdown("### 🐉 LUSER COMMAND CENTER")
    if get_visitor_ip() == PATRON_IP:
        st.success("DOĞRULANDI: Patron Elmeddin")
    else:
        st.info(f"USER: {USER_NAME}")
    
    admin_pwd = st.text_input("Giriş:", type="password")
    if admin_pwd == "amciqadilvuran":
        st.button("Tarixi Təmizlə
                  
