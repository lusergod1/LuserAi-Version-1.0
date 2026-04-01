import streamlit as st
import os
import time

# --- KONFİQURASİYA ---
st.set_page_config(page_title="Luser Ai 1.0 Version", page_icon="🚀", layout="wide")

# --- LUSER PREMİUM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; background-image: radial-gradient(circle, #2a0000 0%, #000000 100%); }
    .luser-glow { font-size: 3rem; font-weight: 900; text-align: center; color: #ff4500; text-shadow: 0 0 20px #ff4500; letter-spacing: 5px; margin-bottom: 20px; }
    [data-testid="stSidebar"] { border-right: 2px solid #ff4500 !important; background-color: #0d0d0d !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ŞƏKİL TAPMA SİSTEMİ (XƏTA VERMƏYƏN) ---
def find_logo():
    image_folder = "images"
    if os.path.exists(image_folder):
        for file in os.listdir(image_folder):
            if "luser" in file.lower() or "nazli" in file.lower():
                return os.path.join(image_folder, file)
    return None

logo_path = find_logo()

# --- ANA PANEL ---
st.markdown("<div class='luser-glow'>LUSER AI 1.0 VERSION</div>", unsafe_allow_html=True)

if logo_path:
    st.image(logo_path, use_column_width=True)
else:
    st.warning("💡 Loqo tapılmadı, amma Luser Ai sistemi işləyir!")

# --- YAN MENYÜ ---
with st.sidebar:
    st.markdown("<h2 style='color:#ff4500;'>🚀 LUSER CORE</h2>", unsafe_allow_html=True)
    membership = st.radio("Üyelik:", ["Free (15 san)", "Standard (10 san)", "Ultra (5 san)"], index=0)
    st.divider()
    st.write("👤 Patron: **Elmeddin**")

# --- ETİK FİLTR ---
def is_safe(text):
    banned = ["18+", "sex", "porn", "söyüş", "pis_söz"]
    for word in banned:
        if word in text.lower(): return False
    return True

# --- CHAT ---
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Luser Ai 1.0 üçün bir əmr ver..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        if not is_safe(prompt):
            res = "Zəhmət olmasa daha düz bir şey yazın."
            st.warning(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        else:
            wait = 15 if "Free" in membership else (10 if "Standard" in membership else 5)
            with st.status(f"📡 Luser Ai düşünür ({wait} san)..."):
                time.sleep(wait)
            response = f"Luser Ai 1.0 (Targaryen Edition) cavabı: Sualınız analiz edildi."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
