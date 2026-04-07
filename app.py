import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import base64

# --- CONFIGURATION API GROQ ---
# Ta clé est insérée ici directement
client = Groq(api_key="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")

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="NEXA SUPRÊME +", page_icon="N", layout="wide")

# --- INITIALISATION DES VARIABLES ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .main-title {
        font-size: 50px;
        font-weight: 900;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 20px;
    }
    .stChatInput {
        border-top: 2px solid #1e3a8a;
    }
    </style>
    <div class="main-title">🚀 NEXA SUPRÊME +</div>
    """, unsafe_allow_html=True)

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>N</h2>", unsafe_allow_html=True)
    st.write(f"**PDG :** GUERRIER ALEJANDRO KARL")
    st.write(f"**École :** Institution Guillaume Jovin (IGJ)")
    
    st.divider()

    # SECTION ADMIN : Pour regarder les utilisateurs
    st.subheader("🔐 Espace Admin")
    admin_code = st.text_input("Code de vérification", type="password", placeholder="Entrez le code...")
    
    if admin_code == "1234":
        st.success("Accès autorisé ✅")
        st.write("👥 **Liste des Utilisateurs (412)**")
        # Tu peux lister tes utilisateurs ici
        st.write("- Jean-Rony")
        st.write("- Marie-Claire")
        st.write("- Stevenson")
    elif admin_code != "":
        st.error("Code incorrect")

    st.divider()

    # SECTION PAIEMENT
    st.subheader("💎 NEXA SUPRÊME +")
    st.info("Abonnement : 250 HTG / 3 Mois")
    method = st.selectbox("Mode de paiement :", ["Sélectionner", "Digicel MonCash", "Natcom Natcash"])
    
    if method == "Digicel MonCash":
        st.success("💰 **MonCash** : +509 4769-2489")
    elif method == "Natcom Natcash":
        st.success("💰 **Natcash** : +509 4208-7977")

# --- INTERFACE : CAMÉRA ET VOCAL ---
col_cam, col_voice = st.columns(2)

with col_cam:
    st.write("📸 **Vision Caméra**")
    st.camera_input("Scanner", label_visibility="collapsed")

with col_voice:
    st.write("🔊 **Contrôle Vocal**")
    if st.button("📢 LIRE LA DERNIÈRE RÉPONSE"):
        if st.session_state.messages:
            # Récupère le dernier message de l'IA
            last_msg = [m["content"] for m in st.session_state.messages if m["role"] == "assistant"]
            if last_msg:
                text_to_speak = last_msg[-1]
                tts = gTTS(text=text_to_speak, lang='fr')
                tts.save("voice.mp3")
                with open("voice.mp3", "rb") as f:
                    data = f.read()
                    b64 = base64.b64encode(data).decode()
                    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
                os.remove("voice.mp3")
        else:
            st.warning("Aucun message à lire.")

st.divider()

# --- AFFICHAGE DE LA CONVERSATION ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LA ZONE POUR ÉCRIRE (CHAT INPUT) ---
# Elle est placée ici pour être toujours visible en bas
prompt = st.chat_input("Écrivez votre message ici pour NEXA...")

if prompt:
    # 1. Ajouter le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Générer la réponse avec Groq
    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}]
            )
            reponse = completion.choices[0].message.content
            st.markdown(reponse)
            # Sauvegarder la réponse
            st.session_state.messages.append({"role": "assistant", "content": reponse})
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")
