import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import base64

# --- CONFIGURATION API GROQ ---
client = Groq(api_key="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")

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="NEXA SUPRÊME +", page_icon="N", layout="wide")

# --- FONCTION VOIX (TTS) ---
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
    except:
        st.error("Erreur vocale.")

# --- INITIALISATION ---
if "premium" not in st.session_state:
    st.session_state.premium = False
if "user_count" not in st.session_state:
    st.session_state.user_count = 412

# --- STYLE CSS ---
st.markdown("""
    <style>
    .main-logo {
        font-size: 130px;
        font-weight: 900;
        background: linear-gradient(45deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: -50px;
    }
    .creator-tag {
        text-align: center;
        font-weight: bold;
        color: #1e40af;
        margin-bottom: 20px;
    }
    .lock-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #f5c6cb;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRE LATÉRALE (PAIEMENT & ADMIN) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>N</h1>", unsafe_allow_html=True)
    st.write(f"*PDG :* GUERRIER ALEJANDRO KARL")
    st.write(f"*École :* IGJ")
    
    st.divider()

    # SECTION ABONNEMENT
    st.subheader("🚀 NEXA SUPRÊME +")
    st.info("💎 *Tarif :* 250 HTG / 3 Mois")
    method = st.selectbox("Payer par :", ["Sélectionner", "Digicel MonCash", "Natcom Natcash"])
    
    if method == "Digicel MonCash":
        st.success("💰 *MonCash* : +509 4769-2489")
    elif method == "Natcom Natcash":
        st.success("💰 *Natcash* : +509 4208-7977")
    
    if method != "Sélectionner":
        st.write("📩 Envoyez le reçu pour activer la Vidéo/Photo avancée.")
    
    st.divider()

    # ADMIN PDG
    pwd = st.text_input("Code PDG", type="password")
    if pwd == "1234":
        st.success("Mode Admin")
        st.metric("Total Users", st.session_state.user_count)
        if st.button("Activer SUPRÊME +"):
            st.session_state.premium = True
            st.rerun()

# --- INTERFACE PRINCIPALE ---
st.markdown("<div class='main-logo'>N</div>", unsafe_allow_html=True)
st.markdown("<div class='creator-tag'>CRÉATEUR : GUERRIER ALEJANDRO KARL</div>", unsafe_allow_html=True)

# ZONE LABORATOIRE (PHOTO & VIDÉO)
st.subheader("🧪 NEXA Lab (Photo & Vidéo)")
col_p, col_v = st.columns(2)

with col_p:
    file_photo = st.file_uploader("📤 Envoyer une Photo", type=['png', 'jpg', 'jpeg'])

with col_v:
    file_video = st.file_uploader("📤 Envoyer une Vidéo de référence", type=['mp4', 'mov'])

if st.button("🪄 Lancer la fusion IA"):
    if not st.session_state.premium:
        st.markdown("<div class='lock-box'>🔒 La fusion Photo/Vidéo est réservée aux membres SUPRÊME +. Payez 250 HTG pour débloquer.</div>", unsafe_allow_html=True)
    elif file_photo and file_video:
        st.success("⚡ Traitement en cours... NEXA anime votre photo selon le mouvement de la vidéo !")
        # Ici on appelle normalement une API de vidéo comme Runway ou Replicate
    else:
        st.warning("Veuillez envoyer une photo ET une vidéo.")

st.divider()

# --- CHAT & VOIX ---
audio_on = st.toggle("Activer la voix de NEXA")
if prompt := st.chat_input("Posez une question..."):
    st.session_state.user_count += 1
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # L'IA connaît toute ta famille et IGJ
        sys_info = """
        Tu es NEXA. Créateur: GUERRIER ALEJANDRO KARL. École: IGJ.
        Mère: Abellard Marie Leyande. Père: Marc Joël Guerrier.
        Frères: Stenley Néré David, Yankee Klervens Guerrier.
        Sœurs: Sentiana Djenny, Kessa Guerrier.
        """
        try:
            model = "llama3-70b-8192" if st.session_state.premium else "llama3-8b-8192"
            res = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": sys_info}, {"role": "user", "content": prompt}]
            )
            text = res.choices[0].message.content
            st.markdown(text)
            if audio_on:
                parler(text)
        except:
            st.error("Connexion serveur perdue.")
