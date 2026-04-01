import streamlit as st
import os
import time
import openai

# --- KONFİQURASİYA ---
st.set_page_config(page_title="Luser Ai 1.0 Version", page_icon="🚀", layout="wide")

# --- SƏNİN ÖZ RƏNGLƏRİN VƏ STİLİN ---
st.markdown("""
    <style>
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle, #2a0000 0%, #000000 100%);
    }
    .luser-glow {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        color: #ff4500;
        text-shadow: 0 0 30px #ff4500, 0 0 10px #ffffff;
        letter-spacing: 10px;
        margin-bottom: 20px;
        font-family: 'Courier New', Courier, monospace;
    }
    [data-testid="stSidebar"] {
        border-right: 2px solid #ff4500 !important;
        background-color: #0d0d0d !important;
    }
    .stChatMessage {
        background: rgba(255, 69, 0, 0.05) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 69, 0, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOQO SİSTEMİ ---
def find_logo():
    image_folder = "images"
    if os.path.exists(image_folder):
        for file in os.listdir(image_folder):
            if "luser" in file.lower():
                return os.path.join(image_folder, file)
    return None

logo_path = find_logo()

# --- ANA PANEL ---
st.markdown("<div class='luser-glow'>LUSER AI 1.0 VERSION</div>", unsafe_allow_html=True)

if logo_path:
    st.image(logo_path, use_column_width=True)

# --- YAN MENYÜ ---
with st.sidebar:
    st.markdown("<h2 style='color:#ff4500;'>🚀 LUSER CORE</h2>", unsafe_allow_html=True)
    membership = st.radio("Üyelik Səviyyəniz:", ["Free (15 san)", "Standard (10 san)", "Ultra (5 san)"], index=0)
    st.divider()
    st.write("👤 Patron: **Elmeddin**")
    if st.button("Söhbəti Təmizlə"):
        st.session_state.messages = []
        st.rerun()

# --- AI MÜHƏRRİKİ (OPENAI BAĞLANTISI) ---
client = None
if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
        # Üyəlik vaxtını hesabla
        wait_time = 15 if "Free" in membership else (10 if "Standard" in membership else 5)
        
        with st.status(f"📡 Luser Ai analiz edir ({wait_time} san)...", expanded=True) as status:
            time.sleep(wait_time)
            
            if client:
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "system", "content": "Sən Luser Ai 1.0-san. Yaradıcın Elmeddindir. Professional və köməkçisən."}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    )
                    full_response = response.choices[0].message.content
                except Exception as e:
                    full_response = "Bağlantı xətası! API Key-i yoxlayın."
            else:
                full_response = "Sistem aktivdir, amma API Key daxil edilməyib."
            
            status.update(label="✅ Analiz tamamlandı!", state="complete", expanded=False)
        
        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
