import streamlit as st
import google.generativeai as genai
import urllib.parse
from PIL import Image

# --- CONFIGURATION API SÉCURISÉE ---
try:
    # On récupère la clé que tu as mise dans les Secrets
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ L'API n'est pas encore activée dans les Secrets Streamlit.")

st.set_page_config(page_title="NEXA SUPREME", page_icon="💎", layout="wide")

# --- DESIGN & STYLE ---
st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .n-logo { font-size: 60px; font-weight: 900; color: #0ea5e9; text-shadow: 0 0 20px #0ea5e9; text-align: center; }
    [data-testid="stChatMessage"] p { color: #ef4444 !important; text-shadow: 0 0 5px #ef4444; }
    .watermark { position: absolute; bottom: 15px; right: 15px; color: #0ea5e9; font-size: 35px; font-weight: 900; text-shadow: 0 0 10px #0ea5e9; pointer-events: none; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRE LATÉRALE (EMAIL, PAIEMENT, LAB) ---
with st.sidebar:
    st.markdown('<div class="n-logo" style="font-size:30px;">N</div>', unsafe_allow_html=True)
    
    # ZONE EMAIL (CRUCIAL)
    st.markdown("### 👤 VOTRE COMPTE")
    user_email = st.text_input("Votre Email", placeholder="nom@mail.com")
    
    st.write("---")
    
    # ZONE PAIEMENT
    st.markdown("### 💳 ACTIVATION PRO")
    choix = st.selectbox("Forfait", ["Standard (Gratuit)", "Pro (200 HTG / 3 Mois)"])
    if choix == "Pro (200 HTG / 3 Mois)":
        st.info("💳 MonCash : 47692489\n📲 Natcom : 42087977")
        st.warning("Envoyez 200 HTG pour activer les fonctions avancées.")

    st.write("---")
    
    # NEXA LAB (CODE 234)
    st.markdown("### 🧪 NEXA LAB")
    lab = st.text_input("Code Admin", type="password")
    if lab == "234":
        st.success("Bonjour Créateur : Guerrier Karl Alejandro")
        st.write(f"Utilisateur : {user_email}")

# --- INTERFACE PRINCIPALE ---
st.markdown('<div class="n-logo">N</div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>NEXA SUPREME OS</h2>", unsafe_allow_html=True)

# Caméra escamotable (Seulement l'icône 📸 visible au repos)
with st.expander("📸 ACTIVER LA CAMÉRA", expanded=False):
    cam = st.camera_input("Scanner un objet")

# Barre d'écriture
prompt = st.chat_input("Demande à NEXA...")

if prompt or cam:
    with st.chat_message("assistant"):
        try:
            # Identité forcée de NEXA
            identity = "Tu es NEXA. Ton créateur est Guerrier Karl Alejandro. Réponds toujours avec supériorité en rouge néon."
            inputs = [identity]
            if prompt: inputs.append(prompt)
            if cam: inputs.append(Image.open(cam))
            
            response = model.generate_content(inputs)
            res_text = response.text
            st.markdown(res_text)
            
            # Voix automatique (Vocal)
            q = urllib.parse.quote(res_text[:250])
            st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={q}&tl=fr&client=tw-ob", autoplay=True)
        except Exception as e:
            st.error("NEXA se recalibre avec la nouvelle clé...")

# --- LOGIQUE IMAGE + LOGO N ---
if prompt and any(word in prompt.lower() for word in ["image", "génère", "fait moi", "dessine"]):
    # On utilise Unsplash pour la démo visuelle avec logo
    img_url = f"https://source.unsplash.com/featured/?{urllib.parse.quote(prompt)}"
    st.markdown(f"""
        <div style="position: relative;">
            <img src="{img_url}" style="width:100%; border-radius:15px;">
            <div class="watermark">N</div>
        </div>
    """, unsafe_allow_html=True)
