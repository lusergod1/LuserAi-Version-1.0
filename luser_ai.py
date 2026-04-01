import streamlit as st
import os
import requests
import json

# --- 1. KONFİQURASİYA ---
st.set_page_config(
    page_title="Luser Ai 1.0", 
    page_icon="🐉", 
    layout="wide"
)

# --- 2. STABİL CSS (Qara ekranı aradan qaldırır) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #000000 !important;
        color: white !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        color: white;
        padding-top: 20px;
    }
    .stat-card {
        background-color: #0d0d0d;
        border: 1px solid #333333;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .stat-value { font-size: 2.5rem; font-weight: 700; color: #ff4500; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. TƏHLÜKƏSİZLİK VƏ STATİSTİKA ---
ADMIN_IPS = ["94.20.98.116"]

def get_real_ip():
    try: return requests.get('https://api.ipify.org', timeout=5).text
    except: return "Unknown"

user_ip = get_real_ip()

# Statistika faylı
STATS_FILE = "stats.json"
def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"total_requests": 1500, "active_bots": 1, "contributors": 1}
    with open(STATS_FILE, "r") as f: return json.load(f)

stats = load_stats()

# --- 4. ANA SƏHİFƏ GÖRÜNTÜSÜ ---
st.markdown("<div class='hero-title'>LUSER AI 1.0</div>", unsafe_allow_html=True)

# Statistika kartları (Qısa və stabil)
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats['total_requests']}</div><div>Requests</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats['active_bots']}</div><div>Active Bots</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-card'><div class='stat-value'>{stats['contributors']}</div><div>Contributors</div></div>", unsafe_allow_html=True)

st.write("---")

# --- 5. CHAT SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Analiz edilir..."):
            # Hugging Face Pulsuz Model
            API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
            try:
                # Statistikanı artır
                stats["total_requests"] += 1
                with open(STATS_FILE, "w") as f: json.dump(stats, f)
                
                response = requests.post(API_URL, json={"inputs": prompt}, timeout=10)
                res = response.json()[0]['generated_text']
            except:
                res = "Luser Ai: Hazırda cavab verə bilmirəm, bir azdan yoxla."
        
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

# --- 6. FOOTER LİNKLƏR ---
st.markdown(f"""
    <div style='text-align: center; padding: 50px; color: #888;'>
        <a href='https://instagram.com/lusergod' style='color:#888; margin:10px;'>Instagram</a> | 
        <a href='https://tiktok.com/@lusergod' style='color:#888; margin:10px;'>TikTok</a> | 
        <a href='https://discordapp.com/users/lusergod' style='color:#888; margin:10px;'>Discord</a>
        <p>© 2026 Elmeddin OSS</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Admin
if user_ip in ADMIN_IPS:
    st.sidebar.success(f"Patron! IP: {user_ip}")
    if st.sidebar.button("Söhbəti təmizlə"):
        st.session_state.messages = []
        st.rerun()
