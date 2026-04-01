import streamlit as st
import os
import time

# --- KONFİQURASİYA ---
st.set_page_config(page_title="Luser Ai 1.0 Version", page_icon="🚀", layout="wide")

# --- TARGARYEN & LUSER PREMİUM CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle, #2a0000 0%, #000000 100%);
    }
    
    /* Luser Ai 1.0 Glow Başlıq */
    .luser-glow {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        color: #ff4500;
        text-shadow: 0 0 30px #ff4500, 0 0 10px #ffffff;
        letter-spacing: 10px;
        margin-bottom: 10px;
        font-family: 'Courier New', Courier, monospace;
    }

    [data-testid="stSidebar"] {
        border-right: 2px solid #ff4500 !important;
        background-color: #0d0d0d !important;
    }
    
    .stChatMessage {
        background: rgba(255, 69, 0, 0.05) !important;
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Ağıllı Loqo Tapma (Luser Markası Üçün) ---
def find_luser_logo():
    image_folder = "images"
    if os.path.exists(image_folder):
        for file in os.listdir(image_folder):
            # Adında 'luser' keçən hər hansı bir şəkli tap (png, jpg, jpeg)
            if "luser" in file.lower():
                return os.path.join(image_folder, file)
    return None

logo_path = find_luser_logo()

# --- ANA PANEL ---
st.markdown("<div class='luser-glow'>LUSER AI 1.0 VERSION</div>", unsafe_allow_html=True)

if logo_path:
    st.image(logo_path, use_column_width=True)
else:
    st.info("💡 İpucu: 'images' qovluğuna 'luser' adlı loqo yerləşdirərək vizualı tamamlaya bilərsiniz.")

st.markdown("<h3 style='text-align:center; color:white; opacity:0.7;'>Targaryen Core | Professional Artificial Intelligence</h3>", unsafe_allow_html=True)

# --- YAN MENYÜ (ÜYELİK SİSTEMİ) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ff4500;'>🚀 LUSER CORE</h2>", unsafe_allow_html=True)
    
    membership = st.radio(
        "Üyelik Səviyyəniz:",
        ["Free (15 san)", "Standard (10 san)", "Ultra (5 san)"],
        index=0
    )
    
    st.divider()
    st.markdown(f"**Sistem Statusu:** <span style='color:#ff4500;'>ACTIVE</span>", unsafe_allow_html=True)
    st.write(f"Səviyyə: {membership}")
    st.write("👤 Hazırladı: **Elmeddin**")

# --- ETİK FİLTR SİSTEMİ ---
def is_safe(text):
    # Təhlükəli və 18+ sözlər filtri
    banned = ["18+", "sex", "porn", "haqsızlıq", "pis_söz", "söyüş"]
    text_lower = text.lower()
    for word in banned:
        if word in text_lower:
            return False
    return True

# --- CHAT SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Luser Ai 1.0 üçün bir əmr ver..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # 1. Təhlükəsizlik Kontrolu
        if not is_safe(prompt):
            response = "Zəhmət olmasa daha düz bir şey yazın."
            st.warning(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            # 2. Üyəlik Müddəti Təyini
            if "Free" in membership: wait_time = 15
            elif "Standard" in membership: wait_time = 10
            else: wait_time = 5
                
            # 3. Düşünmə Animasiyası
            with st.status(f"📡 Luser Ai düşünür ({wait_time} san)...", expanded=True) as status:
                time.sleep(wait_time)
                status.update(label="✅ Analiz tamamlandı!", state="complete", expanded=False)
            
            # 4. Cavabın Çıxışı
            response = f"Luser Ai 1.0 (Targaryen Edition) cavabı: '{prompt}' sualınız üzrə analiz başa çatdı."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})