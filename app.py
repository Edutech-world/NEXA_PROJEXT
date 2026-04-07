import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import base64

# --- CONFIGURATION ---
client = Groq(api_key="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")
st.set_page_config(page_title="NEXA PRO+ 💎", page_icon="🚀", layout="wide")
# --- INITIALISATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "counter" not in st.session_state:
    st.session_state.counter = 150
if "is_pro" not in st.session_state:
    st.session_state.is_pro = False 

# --- FONCTION VOIX ---
def parler(texte):
    try:
        tts = gTTS(text=texte, lang='fr')
        tts.save("response.mp3")
        with open("response.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
            st.markdown(md, unsafe_allow_html=True)
        os.remove("response.mp3")
    except: pass

# --- DESIGN CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stChatInput input { color: white !important; background-color: #262730 !important; }
    .main-logo {
        font-size: 70px; font-weight: 900;
        background: linear-gradient(45deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .pro-active-box {
        background-color: #16a34a; color: white; padding: 10px; 
        border-radius: 10px; text-align: center; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h1 style='color: #3b82f6; text-align: center;'>NEXA</h1>", unsafe_allow_html=True)
    st.write(f"*PDG :* ALEJANDRO KARL")
    st.divider()
    
    # Section NEXA PRO+
    st.subheader("💎 NEXA PRO+")
    if not st.session_state.is_pro:
        st.write("💰 *250 HTG / 3 Mois*")
        st.info("Payez via MonCash (+509 4769-2489) ou Natcash (+509 4208-7977)")
        
        # Le code d'activation client est maintenant 234
        activation_input = st.text_input("🔑 Code d'activation", type="password")
        if activation_input == "234":
            st.session_state.is_pro = True
            st.success("Accès PRO+ débloqué !")
            st.rerun()
    else:
        st.markdown("<div class='pro-active-box'>MEMBRE PRO+ ACTIF ✅</div>", unsafe_allow_html=True)

    st.divider()
    
    # Ton Code Secret Admin (1234)
    admin_input = st.text_input("⚙️ Admin", type="password")
    if admin_input == "1234":
        st.warning(f"📊 Utilisateurs : {st.session_state.counter}")
        if st.button("Reset Stats"):
            st.session_state.counter = 0

# --- INTERFACE PRINCIPALE ---
st.markdown("<div class='main-logo'>NEXA</div>", unsafe_allow_html=True)

# Affichage des outils de vision si PRO
if st.session_state.is_pro:
    st.markdown("### 📸 Espace Multimédia PRO+")
    col1, col2 = st.columns(2)
    with col1:
        st.file_uploader("Analyser une Photo", type=['jpg', 'png', 'jpeg'])
    with col2:
        st.file_uploader("Analyser une Vidéo", type=['mp4', 'mov'])
else:
    st.warning("🔒 Les fonctions Photo et Vidéo sont réservées aux membres PRO+. Activez-les dans le menu.")

# Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pose ta question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.counter += 1
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        )
        response = completion.choices[0].message.content
        st.markdown(response)
        parler(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
