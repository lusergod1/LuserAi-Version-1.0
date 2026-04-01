import streamlit as st
import time

# --- KONFİQURASİYA ---
st.set_page_config(page_title="Luser Ai 1.0", page_icon="🚀")

# --- STİL ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .main-title { font-size: 3rem; text-align: center; color: #ff4500; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'>LUSER AI 1.0 VERSION</div>", unsafe_allow_html=True)
st.write("---")

# --- YAN MENYÜ ---
st.sidebar.title("🚀 Luser Core")
membership = st.sidebar.radio("Üyelik:", ["Free", "Standard", "Ultra"])
st.sidebar.write(f"Patron: **Elmeddin**")

# --- CHAT SİSTEMİ ---
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
        # Üyəlik vaxtı
        wait = 15 if membership == "Free" else (10 if membership == "Standard" else 5)
        
        with st.status(f"📡 Düşünürəm ({wait} san)..."):
            time.sleep(wait)
        
        response = f"Luser Ai 1.0 aktivdir! Sizin '{prompt}' sualınız qəbul edildi. (API Key qoşulandan sonra real cavablar gələcək)."
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
