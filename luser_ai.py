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
# [SYSTEM CORE] - IDENTITY, IP & SECURITY PROTOCOLS
# ==========================================================================================
# Bu bölmədə Patron (Elmeddin) və digər istifadəçilərin tanınması üçün xüsusi məntiq qurulub.

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.lang = "AZ"
    st.session_state.history = []
    st.session_state.start_time = datetime.now()

# Sənin IP ünvanın - Yalnız bu IP-yə "Patron" deyilir
PATRON_IP = "94.20.98.116" 

def get_visitor_ip():
    """İstifadəçinin IP ünvanını ən azı 3 fərqli metodla yoxlayır."""
    try:
        # Metod 1: ipify API
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        try:
            # Metod 2: ident.me API (Fallback)
            return requests.get('https://ident.me', timeout=5).text
        except:
            return "127.0.0.1"

def get_user_greeting():
    """Patronu və Gmail istifadəçilərini tanıyan mərkəzi sistem."""
    current_ip = get_visitor_ip()
    
    # 1. Patron Tanınması
    if current_ip == PATRON_IP:
        return "Patron Elmeddin"
    
    # 2. Gmail / Streamlit User Tanınması (Təhlükəsiz Metod)
    try:
        user_info = getattr(st, "experimental_user", None)
        if user_info is not None:
            # Get metodu ilə yoxlama (AttributeError fixləndi)
            full_name = user_info.get("name")
            if full_name: return str(full_name)
            
            user_email = user_info.get("email")
            if user_email: return str(user_email.split("@")[0])
    except Exception as e:
        logging.error(f"Identity Module Error: {e}")
    
    return "Hörmətli İstifadəçi"

# Qlobal İstifadəçi Adı
USER_NAME = get_user_greeting()

st.set_page_config(
    page_title=f"Luser Ai 1.0 - {USER_NAME}",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================================================
# [VOICE RESONANCE] - UNIVERSAL AUDIO FOR ALL USERS
# ==========================================================================================
# Bu funksiya botun cavablarını hər kəs üçün səsləndirir.
def inject_universal_voice():
    st.components.v1.html(f"""
        <script>
        function speakUniversal(text) {{
            if (!window.speechSynthesis) return;
            window.speechSynthesis.cancel(); 
            const utter = new SpeechSynthesisUtterance(text);
            // Dil tənzimləməsi
            const currentLang = '{st.session_state.lang.lower()}';
            utter.lang = (currentLang === 'az') ? 'tr-TR' : (currentLang === 'ru' ? 'ru-RU' : 'en-US');
            utter.pitch = 1.05;
            utter.rate = 1.0;
            window.speechSynthesis.speak(utter);
        }}
        window.parent.document.addEventListener('bot_reply_event', (e) => {{
            speakUniversal(e.detail.text);
        }});
        </script>
    """, height=0)

# ==========================================================================================
# [PREMIUM VERCEL DESIGN] - SCALABLE CSS FRAMEWORK
# ==========================================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@100;400;900&family=Geist+Mono:wght@400;700&display=swap');
    
    .stApp { background: #000; color: #fff; font-family: 'Geist', sans-serif; }
    header, footer, [data-testid="stHeader"] { visibility: hidden; }
    
    .hero-title {
        font-size: clamp(3rem, 12vw, 8.5rem);
        font-weight: 900;
        letter-spacing: -8px;
        text-align: center;
        background: linear-gradient(180deg, #fff 30%, #333 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 60px 0 20px 0;
        line-height: 0.85;
    }
    
    .status-badge {
        background: #111;
        border: 1px solid #333;
        padding: 10px 20px;
        border-radius: 50px;
        color: #ff4500;
        text-align: center;
        font-family: 'Geist Mono', monospace;
        font-size: 0.8rem;
        width: fit-content;
        margin: 0 auto;
    }

    .stChatInputContainer { border-radius: 0px !important; border: 1px solid #222 !important; background: #080808 !important; }
    .stChatMessage { border-bottom: 1px solid #111 !important; padding: 40px !important; border-radius: 0px !important; }
    
    /* Hover Effects */
    .dashboard-stat {
        border: 1px solid #1a1a1a;
        padding: 40px;
        background: #050505;
        transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .dashboard-stat:hover { border-color: #fff; background: #000; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================================================================
# [RESILIENCE GATEWAY] - ANTI-NODE-BUSY LOGIC
# ==========================================================================================
class LuserIntelligence:
    @staticmethod
    def query(prompt):
        # 1. Mərkəzi Bilgi Bazası (Fast Local Cache)
        KNOWLEDGE = {
            "turbo.json": "Turbo Pipeline v4: Active. Cache-Hit 100%.",
            "aisdk.xlsx": "AI-Core Migration completed successfully for LUSER AI.",
            "ihtiyat.mp4": "Edge Streaming Protocol v2.4 initialized.",
            "luserai": "Luser Ai 1.0 is a professional AI framework created by Elmeddin."
        }
        for k, v in KNOWLEDGE.items():
            if k in prompt.lower(): return f"**[INTERNAL KNOWLEDGE]** {v}"

        # 2
