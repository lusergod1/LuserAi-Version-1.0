import streamlit as st
import os
import time
import openai

# --- KONFİQURASİYA ---
st.set_page_config(page_title="Luser Ai 1.0 Version", page_icon="🚀", layout="wide")

# --- FULL DARK MODE & TARGARYEN CSS ---
st.markdown("""
    <style>
    /* Səhifəni qaralt və ağlıqları yox et */
    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(circle, #2a0000 0%, #000000 100%) !important;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Yazı rəngləri */
    .luser-glow {
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        color: #ff4500;
        text-shadow: 0 0 20px #ff4500;
        letter-spacing: 5px;
        padding: 20px 0;
    }

    /* Chat sahəsini tənzimlə */
    .stChatInputContainer {
        background-color: #050505 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOQO SİSTEMİ ---
def find_logo():
    image_folder = "images"
    if os.path.exists(image_folder):
        for f in os.listdir(image_folder):
            if "luser" in f.lower():
                return os.path.join(image_folder, f)
    return None

logo_path = find_logo()

# --- ANA PANEL ---
st.markdown("<div class='luser-glow'>LUSER AI 1.0 VERSION</div>", unsafe_allow_html=True)

if logo_path:
    st.image(logo_path, use_column_width=True)

# --- AI MÜHƏRRİKİ ---
client = None
if "OPENAI_API_KEY" in st.secrets:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    except:
        client = None

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
        if not client:
            res = "⚠️ API Key xətası! Streamlit Secrets bölməsini yoxlayın."
            st.error(res)
        else:
            with st.status("📡 Analiz edilir...", expanded=False):
                try:
                    chat_completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    )
                    res = chat_completion.choices[0].message.content
                except Exception as e:
                    res = f"Xəta: {str(e)}"
            
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
