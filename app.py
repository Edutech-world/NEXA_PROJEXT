import streamlit as st
import google.generativeai as genai
import urllib.parse
from PIL import Image

# --- CONFIGURATION CERVEAU ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.set_page_config(page_title="NEXA SUPREME", page_icon="💎", layout="wide")

# --- DESIGN CSS (Interface Alignée + Filigrane) ---
st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .n-logo { font-size: 60px; font-weight: 900; color: #0ea5e9; text-shadow: 0 0 20px #0ea5e9; text-align: center; }
    
    /* Réponses en rouge néon */
    [data-testid="stChatMessage"] p { color: #ef4444 !important; text-shadow: 0 0 5px #ef4444; }

    /* --- FILIGRANE N SUR IMAGE --- */
    .image-container { position: relative; display: inline-block; width: 100%; border-radius: 15px; overflow: hidden; }
    .watermark {
        position: absolute; bottom: 15px; right: 15px;
        color: #0ea5e9; font-size: 40px; font-weight: 900;
        text-shadow: 0 0 15px #0ea5e9; background: rgba(2, 6, 23, 0.4);
        padding: 5px 15px; border-radius: 10px; pointer-events: none;
    }
    
    /* Cacher les labels inutiles pour gagner de la place */
    label { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
if "users_list" not in st.session_state:
    st.session_state.users_list = []

# --- BARRE LATÉRALE (EMAIL & LAB) ---
with st.sidebar:
    st.markdown('<div class="n-logo" style="font-size:30px;">N</div>', unsafe_allow_html=True)
    st.markdown("### 👤 CONNEXION")
    email_user = st.text_input("Email", placeholder="votre@email.com")
    if email_user and email_user not in st.session_state.users_list:
        st.session_state.users_list.append(email_user)

    st.write("---")
    st.info("MonCash: 47692489 | Natcom: 42087977")
    
    st.write("---")
    st.markdown("### 🧪 NEXA LAB")
    lab_code = st.text_input("Code Maître", type="password")
    if lab_code == "234":
        st.success("BIENVENUE PRÉSIDENT")
        st.write(f"Utilisateurs : {len(st.session_state.users_list)}")
        for u in st.session_state.users_list: st.text(f"• {u}")

# --- INTERFACE PRINCIPALE ---
st.markdown('<div class="n-logo">N</div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>NEXA SUPREME OS</h2>", unsafe_allow_html=True)

# --- BARRE DE COMMANDE (COMME GEMINI/MICROSOFT) ---
# On crée 3 colonnes : Caméra | Texte | Micro
col_cam, col_input, col_mic = st.columns([1, 4, 1])

with col_cam:
    cam_file = st.camera_input("📸", label_visibility="collapsed")

with col_input:
    prompt = st.chat_input("Demande à NEXA...")

with col_mic:
    st.markdown("<h1 style='text-align:center; cursor:pointer;'>🎤</h1>", unsafe_allow_html=True)
    voice_on = st.toggle("Vocal", value=True)

# --- LOGIQUE DE RÉPONSE ---
if prompt or cam_file:
    with st.chat_message("assistant"):
        # Détection Image
        img_keywords = ["génère", "fait moi", "dessine", "image de", "crée"]
        is_img = prompt and any(k in prompt.lower() for k in img_keywords)

        if is_img:
            clean_p = prompt.lower()
            for k in img_keywords: clean_p = clean_p.replace(k, "").strip()
            img_url = f"https://source.unsplash.com/featured/?{urllib.parse.quote(clean_p)}"
            st.markdown(f"""
                <div class="image-container">
                    <img src="{img_url}" style="width:100%; border-radius:15px;">
                    <div class="watermark">N</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            try:
                content = ["Tu es NEXA. Créateur: Guerrier Karl Alejandro. Réponds en rouge."]
                if prompt: content.append(prompt)
                if cam_file:
                    img = Image.open(cam_file)
                    content.append(img)
                    st.image(img, width=250)
                
                response = model.generate_content(content)
                st.markdown(response.text)
                
                # Voix automatique si activé
                if voice_on:
                    q = urllib.parse.quote(response.text[:250])
                    st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={q}&tl=fr&client=tw-ob", autoplay=True)
            except:
                st.error("Erreur Système. Vérifiez l'API.")