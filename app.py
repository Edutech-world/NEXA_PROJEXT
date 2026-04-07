import streamlit as st
import google.generativeai as genai
import base64
import urllib.parse

# --- 1. CONFIGURATION ÉLITE ---
st.set_page_config(page_title="NEXA PRO+ GOOGLE", page_icon="💎", layout="wide")

# CONNEXION AU NOUVEAU CERVEAU GOOGLE (Sécurisée via Secrets)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# DESIGN "NEXA DARK LUXE"
st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .n-logo { font-size: 70px; font-weight: 900; color: #0ea5e9; text-shadow: 0 0 25px #0ea5e9; text-align: center; }
    .stChatMessage[data-testid="stChatMessageAssistant"] .stChatMessageAvatar::after { content: "N"; font-weight: 900; color: #0ea5e9; }
    .lab-title { color: #f59e0b; font-weight: 900; text-shadow: 0 0 10px #f59e0b; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTION DE SESSION ---
if "pro_active" not in st.session_state: st.session_state.pro_active = False

# --- 3. BARRE LATÉRALE (PAIEMENT & ADMIN) ---
with st.sidebar:
    st.markdown('<div class="n-logo" style="font-size:30px;">N</div>', unsafe_allow_html=True)
    st.markdown("### 💳 ABONNEMENT PRO+")
    st.info("Frais : 200 HTG / 3 Mois\n- MonCash : 47 69 24 89\n- NatCash : 42 08 79 77")
    
    # Déblocage Client
    if st.text_input("Code Déblocage", type="password") == "234":
        st.session_state.pro_active = True
        st.success("💎 NEXA LAB ACTIF")

    st.write("---")
    # Panneau PDG (Contrôle des Users)
    if st.text_input("Admin Code", type="password") == "1234":
        st.metric("STATUT SYSTÈME", "OPTIMAL")
        st.write("Cerveau : Google Gemini 1.5")

# --- 4. INTERFACE PRINCIPALE ---
st.markdown('<div class="n-logo">N</div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>NEXA SUPREME OS</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("👁️ SCANNER")
    img = st.camera_input("CAPTURE")
    
    st.write("---")
    st.markdown('<h3 class="lab-title">🧪 NEXA LAB (PRO+)</h3>', unsafe_allow_html=True)
    if st.button("🖼️ TRAVAILLER PHOTO") or st.button("🎥 TRAVAILLER VIDÉO"):
        if not st.session_state.pro_active:
            st.error("🚨 Accès refusé. Payez 200 HTG et entrez le code '234'.")
        else:
            st.success("Ouverture du Lab Google...")

with col2:
    st.subheader("💬 INTERFACE GOOGLE AI")
    if "messages" not in st.session_state: st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    # Barre de message stylée
    cols = st.columns([1, 10, 1])
    with cols[0]: st.markdown("📷")
    with cols[1]: prompt = st.chat_input("Commandez ici, Monsieur le Président...")
    with cols[2]: st.markdown("🎙️")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Appel au nouveau cerveau Google
            response = model.generate_content(f"Tu es NEXA, l'IA créée par le Président Alejandro Karl. Réponds à : {prompt}")
            res_text = response.text
            st.markdown(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            # Voix auto
            q = urllib.parse.quote(res_text[:250])
            st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={q}&tl=fr&client=tw-ob", format="audio/mp3", autoplay=True)
        except Exception as e:
            st.error(f"Erreur de connexion Google : {e}")
