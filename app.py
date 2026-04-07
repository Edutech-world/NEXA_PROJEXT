import streamlit as st
import google.generativeai as genai
import base64
import urllib.parse

# --- CONFIGURATION CERVEAU ---
# On utilise la clé que tu as mise dans les Secrets tout à l'heure
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- DESIGN NEXA ---
st.set_page_config(page_title="NEXA PRO+", page_icon="💎", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .n-logo { font-size: 70px; font-weight: 900; color: #0ea5e9; text-shadow: 0 0 25px #0ea5e9; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

if "pro_active" not in st.session_state: st.session_state.pro_active = False

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.markdown('<div class="n-logo" style="font-size:30px;">N</div>', unsafe_allow_html=True)
    if st.text_input("Code Déblocage", type="password") == "234":
        st.session_state.pro_active = True
        st.success("💎 NEXA LAB ACTIF")
    
    st.write("---")
    if st.text_input("Admin Code", type="password") == "1234":
        st.write("Cerveau : Google Gemini 1.5")

# --- INTERFACE ---
st.markdown('<div class="n-logo">N</div>', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>NEXA SUPREME OS</h2>", unsafe_allow_html=True)

prompt = st.chat_input("Commandez ici, Monsieur le Président...")

if prompt:
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"Tu es NEXA, l'IA du Président Alejandro Karl. Réponds à : {prompt}")
            st.markdown(response.text)
            # Voix (via une méthode qui ne demande pas gTTS dans requirements)
            q = urllib.parse.quote(response.text[:250])
            st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={q}&tl=fr&client=tw-ob")
        except Exception as e:
            st.error(f"Erreur : {e}")
