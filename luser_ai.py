import streamlit as st
import os
import requests
import json
from gtts import gTTS
from io import BytesIO
import datetime

# ==========================================
# 1. KONFİQURASİYA VƏ MOBİL FİX
# ==========================================
st.set_page_config(
    page_title="AI Programlan",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Mobil və PC üçün eyni qara dizayn (Ağ ekranı ləğv edir)
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    .stApp { background-color: #000000 !important; }
    
    /* Başlıq və Dizayn (image_9.png stili) */
    .hero-title { font-size: 3rem; font-weight: 800; text-align: center; color: white; padding-top: 30px; }
    .hero-subtitle { text-align: center; color: #888; margin-bottom: 20px; }
    
    /* Mod Düymələri */
    .mode-container { display: flex; justify-content: center; gap: 10px; margin: 20px 0; }
    .mode-btn { border: 1px solid white; padding: 10px; border-radius: 5px; text-align: center; min-width: 100px; }
    
    /* Chat girişini və artını (+) düzəltmək */
    .stChatInputContainer { border: 1px solid #ffffff !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DATA VƏ LOGİSTİKA (Local Host Data)
# ==========================================
LOG_FILE = "user_logs.json"
def log_user_data(ip, email="Anonim"):
    data = {"time": str(datetime.datetime.now()), "ip": ip, "identity": email}
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f: logs = json.load(f)
    logs.append(data)
    with open(LOG_FILE, "w") as f: json.dump(logs, f)

def get_ip():
    try: return requests.get('https://api.ipify.org').text
    except: return "127.0.0.1"

user_ip = get_ip()
log_user_data(user_ip) # Giriş edəni gizlicə qeyd edir

# ==========================================
# 3. DİL VƏ SƏS SİSTEMİ
# ==========================================
if "lang" not in st.session_state: st.session_state.lang = "az"

def speak(text, lang):
    tts_lang = 'tr' if lang == "az" else lang # gTTS-də az yoxdur, tr ən yaxın səslənişdir
    try:
        tts = gTTS(text=text, lang=tts_lang)
        fp = BytesIO()
        tts.write_to_fp(fp)
        return fp
    except: return None

# ==========================================
# 4. MODLAR VƏ QİYMƏTLƏR
# ==========================================
st.markdown("<div class='hero-title'>AI Programlan</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Universal SDK by Elmeddin</div>", unsafe_allow_html=True)

# Dil Seçimi
col_l1, col_l2, col_l3 = st.columns([4,4,4])
if col_l1.button("AZ"): st.session_state.lang = "az"
if col_l2.button("EN"): st.session_state.lang = "en"
if col_l3.button("RU"): st.session_state.lang = "ru"

st.write("---")

# Mod Seçimi
selected_mode = st.radio("Süni İntellekt Modu Seçin:", 
    ["Hızlı (Sınırsız)", "Pro (15 AZN)", "Düşünməli (10 AZN)"], horizontal=True)

# ==========================================
# 5. FAYL YÜKLƏMƏ (+) SİSTEMİ
# ==========================================
uploaded_file = st.file_uploader("Fayl, PDF və ya Şəkil əlavə et (+)", type=['png', 'jpg', 'pdf', 'jpeg'])
if uploaded_file:
    st.success(f"{uploaded_file.name} yükləndi!")

# ==========================================
# 6. CHAT VƏ AI (Məntiq düzəldildi)
# ==========================================
if "messages" not in st.session_state: st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.write(prompt)

    with st.chat_message("assistant"):
        # Modlara görə sürət və keyfiyyət imitasiyası
        status_text = "Tez cavab hazırlanır..." if "Hızlı" in selected_mode else "Dərin analiz edilir (Pro)..."
        with st.spinner(status_text):
            # Burda xəta verməməsi üçün analiz mətni gizlədildi, birbaşa cavab gəlir
            API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
            try:
                res = requests.post(API_URL, json={"inputs": prompt}).json()[0]['generated_text']
            except:
                res = "Bağışlayın, hazırda cavab verə bilmirəm."
            
            # Dilə görə xüsusi salamlaşma
            if st.session_state.lang == "az": res = f"Luser Ai: {res}"
            elif st.session_state.lang == "ru": res = f"Luser Ai (RU): {res}"
            
            st.write(res)
            audio = speak(res, st.session_state.lang)
            if audio: st.audio(audio)
            st.session_state.messages.append({"role": "assistant", "content": res})

# ==========================================
# 7. SOSİAL LİNKLƏR (GÜNCƏL)
# ==========================================
st.markdown(f"""
    <div style='text-align: center; margin-top: 50px;'>
        <a href='https://instagram.com/luser4x' style='color:white; margin:15px;'>INSTAGRAM</a>
        <a href='https://tiktok.com/@luser4x' style='color:white; margin:15px;'>TIKTOK</a>
        <p style='color:#333; font-size:10px;'>User IP: {user_ip}</p>
    </div>
""", unsafe_allow_html=True)
