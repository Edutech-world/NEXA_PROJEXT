import streamlit as st
from groq import Groq
import base64
import urllib.parse

# --- 1. CONFIGURATION ÉLITE & DESIGN ---
st.set_page_config(page_title="NEXA PRO+", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .n-logo { font-size: 70px; font-weight: 900; color: #0ea5e9; text-shadow: 0 0 25px #0ea5e9; text-align: center; }
    .stChatMessage[data-testid="stChatMessageAssistant"] .stChatMessageAvatar::after { content: "N"; font-weight: 900; color: #0ea5e9; }
    .stButton>button { border-radius: 15px !important; background: linear-gradient(90deg, #0ea5e9, #6366f1) !important; color: white !important; font-weight: bold; }
    .lab-title { color: #f59e0b; font-weight: 900; text-shadow: 0 0 10px #f59e0b; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTION DES VARIABLES DE SESSION ---
if "pro_active" not in st.session_state: st.session_state.pro_active = False
if "user_list" not in st.session_state: st.session_state.user_list = []

# --- 3. BARRE LATÉRALE (PAIEMENT & ADMIN) ---
with st.sidebar:
    st.markdown('<div class="n-logo" style="font-size:30px;">N</div>', unsafe_allow_html=True)
    st.markdown("### 💳 ABONNEMENT NEXA PRO+")
    st.info("""
    *Frais : 200 HTG / 3 Mois*
    - MonCash : 47 69 24 89
    - NatCash : 42 08 79 77
    Envoyez le code '234' après paiement.
    """)
    
    # Activation par le client
    user_code = st.text_input("Entrez votre code de déblocage", type="password")
    if user_code == "234":
        st.session_state.pro_active = True
        st.success("💎 NEXA LAB DÉBLOQUÉ")
    
    st.write("---")
    # PANNEAU ADMIN PDG (CODE 1234)
    admin_pass = st.text_input("Contrôle PDG (Admin)", type="password")
    if admin_pass == "1234":
        st.subheader("📊 GESTION DES USERS")
        st.write(f"Utilisateurs connectés : {len(st.session_state.user_list)}")
        if st.button("Réinitialiser le système"):
            st.session_state.pro_active = False
            st.rerun()

# --- 4. INTERFACE PRINCIPALE ---
st.markdown('<div class="n-logo">N</div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>NEXA SUPREME OS</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748b;'>Institution Guillaume Jovin</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("👁️ CAPTEURS")
    st.camera_input("Scanner")
    
    st.write("---")
    st.markdown('<h3 class="lab-title">🧪 NEXA LAB</h3>', unsafe_allow_html=True)
    
    # Boutons visibles mais conditionnels
    btn_image = st.button("🖼️ TRAVAILLER PHOTO")
    btn_video = st.button("🎥 TRAVAILLER VIDÉO")
    
    if (btn_image or btn_video) and not st.session_state.pro_active:
        st.error("🚨 Accès refusé. Veuillez payer 200 HTG et entrer le code '234'.")
    elif (btn_image or btn_video) and st.session_state.pro_active:
        st.balloons()
        st.success("Ouverture du laboratoire PRO+...")

with col2:
    st.subheader("💬 INTERFACE NEURONALE")
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    # BARRE DE MESSAGE AVEC ICÔNES
    input_col, cam_col, mic_col = st.columns([10, 1, 1])
    with cam_col: st.markdown("📷")
    with input_col: 
        prompt = st.chat_input("Commandez ici...")
    with mic_col: st.markdown("🎙️")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    client = Groq(api_key="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")
    try:
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Tu es NEXA, l'IA du Président Alejandro Karl."}] + 
                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        reponse = chat.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reponse})
        st.rerun()
    except Exception as e: st.error(f"Erreur : {e}")
