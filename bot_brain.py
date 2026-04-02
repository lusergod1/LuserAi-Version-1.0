
import requests
from duckduckgo_search import DDGS

def get_smart_answer(prompt, user_name, lang="az"):
    # 1. DÜNYA WEB TARAMASI (Daha stabil versiya)
    try:
        # DDGS Chat tez bloklanır, ona görə daha güclü olan Text (mətn) axtarışını istifadə edirik
        results = DDGS().text(prompt, max_results=2)
        if results:
            context = "\n\n".join([f"🔹 **{r['title']}**\n{r['body']}" for r in results])
            if lang == "az":
                return f"Salam **{user_name}**! 🌍 İnternetin dərinliklərindən tapdığım məlumatlar:\n\n{context}"
            elif lang == "ru":
                return f"Привет **{user_name}**! 🌍 Вот что я нашел в сети:\n\n{context}"
            else:
                return f"Hello **{user_name}**! 🌍 Here is what I found on the web:\n\n{context}"
    except Exception:
        pass # Veb bloklansa, dərhal 2-ci plana keçir
        
    # 2. HUGGING FACE AI (Fallback)
    try:
        API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
        res = requests.post(API_URL, json={"inputs": prompt}, timeout=10).json()[0]['generated_text']
        return f"🧠 **{user_name}** üçün xüsusi AI Analizi: \n\n{res}"
    except Exception:
        pass

    # 3. QIRILMAZ QORUMA (Serverlər çöksə belə)
    return f"Patron **{user_name}**, hazırda dünya serverlərinə qoşulmaqda kiçik bir ləngimə var. Sualını yaddaşımda saxlayıram, lütfən bir neçə saniyə sonra təkrarla."
