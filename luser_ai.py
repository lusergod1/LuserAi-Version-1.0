import streamlit as st
import os
import requests
import time
import json
import logging
from datetime import datetime

# --- 1. LOGGİNG VƏ SİSTEM AYARLARI ---
# Bu hissə proqramın arxa fonda necə işlədiyini izləmək üçündür.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 2. ANA KONFİQURASİYA ---
st.set_page_config(
    page_title="Luser Ai 1.0 - Vercel Master Edition", 
    page_icon="🐉", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. GENİŞLƏNDİRİLMİŞ PREMİUM CSS (Vercel + Targaryen Red) ---
# Burada Vercel-in sadəliyi ilə Targaryen-in qırmızı parıltısını birləşdirdim.
st.markdown("""
    <style>
    /* Ana Fon tənzimləmələri */
    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(circle at 50% 50%, #1a0000 0%, #000000 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    
    /* Gereksiz Streamlit hissələrini gizlə */
    header, footer, [data-testid="stHeader"] { visibility: hidden; }
    
    /* Vercel Hero Bölməsi - SS-dəki kimi */
    .hero-container {
        padding: 80px 0 40px 0;
        text-align: center;
    }
    .hero-title {
        font-size: clamp(2.8rem, 8vw, 5rem);
        font-weight: 800;
        background: linear-gradient(180deg, #ffffff 0%, #888888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -4px;
        line-height: 1;
        margin-bottom: 25px;
    }
    .hero-subtitle {
        font-size: 1.3rem;
        color: #a1a1a1;
        max-width: 800px;
        margin: 0 auto 50px auto;
        line-height: 1.6;
        font-weight: 400;
    }

    /* Statistika Kartları - SS-dəki 4-lü sistem */
    .stat-wrapper {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 25px;
        margin-bottom: 70px;
    }
    .stat-card {
        background: rgba(12, 12, 12, 0.7);
        border: 1px solid #252525;
        border-radius: 14px;
        padding: 35px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stat-card:hover {
        border-color: #ff4500;
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(255, 69, 0, 0.15);
    }
    .stat-value {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 5px;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #777;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }

    /* Chat UI - Professional dizayn */
    .stChatInputContainer {
        border: 1px solid #333 !important;
        background-color: #080808 !important;
        border-radius: 16px !important;
        padding: 12px !important;
        margin-bottom: 20px !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #ff4500 !important;
        box-shadow: 0 0 15px rgba(255, 69, 0, 0.2) !important;
    }

    /* Footer dizaynı - SS-dəki linklər */
    .footer-main {
        margin-top: 120px;
        padding: 80px 0;
        border-top: 1px solid #1a1a1a;
    }
    .footer-heading {
        color: #ffffff;
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .footer-link {
        color: #666;
        text-decoration: none;
        font-size: 0.9rem;
        display: block;
        margin-bottom: 12px;
        transition: color 0.3s;
    }
    .footer-link:hover { color: #ff4500; }
    
    /* Button stilləri */
    .stButton>button {
        background-color: transparent !important;
        color: #ffffff !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        transition: all 0.3s !important;
        width: 100%;
    }
    .stButton>button:hover {
        border-color: #ff4500 !important;
        color: #ff4500 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA İDARƏETMƏ VƏ TƏHLÜKƏSİZLİK (IP LOCK) ---
ADMIN_IPS = ["94.20.98.116"]
STATS_FILE = "stats.json"

def get_visitor_ip():
    """Ziyarətçinin real IP-sini çəkir."""
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except Exception as e:
        logger.error(f"IP retrieval error: {e}")
        return "Unknown"

def init_stats_structure():
    """Statistikaların default şablonu."""
    return {
        "total_requests": 1200000,
        "weekly_active_bots": 5,
        "contributors": 1,
        "models_supported": 100,
        "last_sync": str(datetime.now())
    }

def load_or_sync_stats(increment=False):
    """Statistikaları oxuyur və KeyError-ləri fixləyir."""
    default_data = init_stats_structure()
    if not os.path.exists(STATS_FILE):
        current_data = default_data
    else:
        try:
            with open(STATS_FILE, "r") as f:
                current_data = json.load(f)
                # Eksik olan hər şeyi doldur ki xəta verməsin
                for k, v in default_data.items():
                    if k not in current_data:
                        current_data[k] = v
        except Exception as e:
            logger.error(f"JSON Load error: {e}")
            current_data = default_data
            
    if increment:
        current_data["total_requests"] += 1
        current_data["last_sync"] = str(datetime.now())
        try:
            with open(STATS_FILE, "w") as f:
                json.dump(current_data, f)
        except Exception as e:
            logger.error(f"JSON Save error: {e}")
            
    return current_data

# İlkin datanı yüklə
user_ip = get_visitor_ip()
current_stats = load_or_sync_stats()

# --- 5. UI: HEADER VƏ LOQO ---
def render_site_header():
    st.markdown("<div class='hero-container'>", unsafe_allow_html=True)
    
    # Loqo axtarışı (Luser/Nazlı)
    if os.path.exists("images"):
        for file in os.listdir("images"):
            if any(name in file.lower() for name in ["luser", "nazli"]):
                st.image(os.path.join("images", file), width=90)
                break
    
    st.markdown("<div class='hero-title'>Universal AI layer for<br>building frameworks and agents</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>A unified Luser SDK for building AI apps with modern streaming, and multi-model support—powered by Elmeddin OSS.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

render_site_header()

# Statistika Paneli (Dinamik Kartlar)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{current_stats.get('total_requests', 0)/1000000:.1f}M</div><div class='stat-label'>Weekly downloads</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>23.2K</div><div class='stat-label'>GitHub stars</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{current_stats.get('contributors', 1)}</div><div class='stat-label'>Contributors</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='stat-card'><div class='stat-value'>{current_stats.get('models_supported', 100)}+</div><div class='stat-label'>Models supported</div></div>", unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: #1a1a1a;'><br>", unsafe_allow_html=True)

# --- 6. SÜRATLİ CHAT SİSTEMİ (TinyLlama - 10s Limit) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👨" if msg["role"] == "user" else "🐉"):
        st.markdown(msg["content"])

# Mesaj girişi
if prompt := st.chat_input("Luser Ai-a bir şey soruş..."):
    # Sayğacı artır
    load_or_sync_stats(increment=True)
    
    # User mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨"):
        st.markdown(prompt)
    
    # Assistant mesajı
    with st.chat_message("assistant", avatar="🐉"):
        with st.status("📡 Analiz edilir...", expanded=False) as status:
            # Sürətli model və 10 saniyə timeout
            API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
            try:
                # Sənin koddakı o SYNTAX ERROR burda düzəldi (mötərizə bağlandı)
                payload = {
                    "inputs": f"<|system|>\nYou are Luser Ai, created by Elmeddin. Respond concisely.<|user|>\n{prompt}<|assistant|>\n",
                    "parameters": {"max_new_tokens": 300, "temperature": 0.7}
                }
                response = requests.post(API_URL, json=payload, timeout=10)
                
                if response.status_code == 200:
                    output = response.json()[0]['generated_text']
                    final_text = output.split("<|assistant|>\n")[-1].strip()
                    status.update(label="✅ Hazırdır", state="complete")
                else:
                    final_text = "Luser Ai: Server hazırda cavab vermir, bir azdan yoxlayın."
                    status.update(label="❌ Server Xətası", state="error")
            except requests.exceptions.Timeout:
                final_text = "Luser Ai: Patron, 10 saniyə doldu, server gecikdi. Yenidən cəhd edək?"
                status.update(label="⏱️ Zaman Aşımı", state="error")
            except Exception as e:
                final_text = f"Luser Ai: Sistemdə bir xəta baş verdi."
                status.update(label="❌ Xəta", state="error")
        
        st.markdown(final_text)
        st.session_state.messages.append({"role": "assistant", "content": final_text})

# --- 7. FOOTER: SOSİAL VƏ ŞİRKƏT LİNKLƏRİ ---
st.markdown(f"""
    <div class='footer-main'>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 60px;'>
            <div>
                <div class='footer-heading'>Resources</div>
                <a class='footer-link' href='#'>Documentation</a>
                <a class='footer-link' href='#'>AI Reference</a>
                <a class='footer-link' href='#'>Blog</a>
            </div>
            <div>
                <div class='footer-heading'>Community</div>
                <a class='footer-link' href='https://instagram.com/lusergod' target='_blank'>Instagram</a>
                <a class='footer-link' href='https://tiktok.com/@lusergod' target='_blank'>TikTok</a>
                <a class='footer-link' href='https://discordapp.com/users/lusergod' target='_blank'>Discord Account</a>
            </div>
            <div>
                <div class='footer-heading'>Company</div>
                <a class='footer-link' href='#'>About Elmeddin OSS</a>
                <a class='footer-link' href='#'>Privacy Policy</a>
                <a class='footer-link' href='#'>Terms of Service</a>
            </div>
        </div>
        <div style='text-align: center; margin-top: 80px; color: #444; font-size: 0.8rem;'>
            © 2026 Luser Ai, Elmeddin Inc. All rights reserved.<br>
            Current Node IP: <span style='color: #ff4500;'>{user_ip}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 8. ADMIN DASHBOARD (Yalnız Sənə Görünür) ---
if user_ip in ADMIN_IPS:
    with st.sidebar:
        st.markdown("<h2 style='color: #ff4500;'>🐉 LUSER CONTROL</h2>", unsafe_allow_html=True)
        st.markdown(f"**Vəziyyət:** Stabil ✅")
        st.markdown(f"**IP:** {user_ip}")
        
        if st.button("Söhbət Tarixini Sıfırla"):
            st.session_state.messages = []
            st.rerun()
            
        if st.button("Statistikaları Yenilə"):
            st.rerun()
            
        with st.expander("Debug Məlumatları"):
            st.json(current_stats)
else:
    with st.sidebar:
        st.markdown("<h3 style='color: #444;'>Luser Ai 1.0</h3>", unsafe_allow_html=True)
        st.caption("Universal AI Layer")
