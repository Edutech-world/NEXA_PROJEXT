import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

# --- 1. ACTIVATION DU MODE APPLICATION (PWA) ---
components.html(
    """
    <link rel="manifest" href="/manifest.json">
    <script>
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js');
      }
    </script>
    """,
    height=0,
)

# --- 2. CONFIGURATION NEXA PREMIUM ---
st.set_page_config(page_title="NEXA PREMIUM", page_icon="🔵")
st.title("🔵 NEXA PREMIUM")
st.caption("Moteur : Gemma 2 (Google-Groq) | PDG Alejandro Karl Guerrier")

# --- 3. CONNEXION API SÉCURISÉE ---
# On remplace ta clé "gsk_..." par ce code secret
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 4. GESTION DU CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Posez votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Appel à Groq (Gemma 2)
    with st.chat_message("assistant"):
        completion = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        )
        response = completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
       # Appel à Groq (Gemma 2)
    with st.chat_message("assistant"):
        try:  # <--- IL FAUT AJOUTER CE "try" ICI
            completion = client.chat.completions.create(
                model="gemma2-9b-it",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e: # <--- Maintenant le except est aligné avec le try
            st.error(f"Erreur : {e}")