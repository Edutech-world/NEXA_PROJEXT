import streamlit as st
import google.generativeai as genai
import urllib.parse

# --- 1. CONFIGURATION DU CERVEAU STABLE ---
# On utilise 'gemini-pro' qui est 100% compatible
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="NEXA PRO+", page_icon="💎", layout="wide")

# --- 2. STYLE ROUGE NÉON ---
st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .n-logo { font-size: 60px; font-weight: 900; color: #0ea5e9; text-shadow: 0 0 20px #0ea5e9; text-align: center; }
    /* Style pour les réponses en rouge */
    [data-testid="stChatMessage"] p { color: #ef4444 !important; text-shadow: 0 0 5px #ef4444; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BARRE LATÉRALE ---
with st.sidebar:
    st.markdown("### ⚙️ NEXA OS")
    email = st.text_input("📧 Votre Email")
    st.write("---")
    admin = st.text_input("🔑 Code Admin", type="password")
    if admin == "1234":
        st.success("Accès Maître autorisé")

# --- 4. INTERFACE PRINCIPALE ---
st.markdown('<div class="n-logo">N</div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>NEXA PRO+ SUPREME</h2>", unsafe_allow_html=True)

# Zone de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. LA BARRE DE COMMANDE (C'est elle qui va se débloquer !) ---
prompt = st.chat_input("Commandez ici, Monsieur le Président...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # On demande une réponse courte et puissante
            response = model.generate_content(f"Réponds en tant que NEXA, l'IA de Guerrier Karl Alejandro : {prompt}")
            res_text = response.text
            st.markdown(res_text)
            
            # Lecture Vocale
            q = urllib.parse.quote(res_text[:200])
            st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={q}&tl=fr&client=tw-ob", autoplay=True)
            
            st.session_state.messages.append({"role": "assistant", "content": res_text})
        except Exception as e:
            st.error(f"Erreur : {e}")