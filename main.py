import streamlit as st

def say(text):
    st.markdown(f"""
        <script>
            var utterance = new SpeechSynthesisUtterance("{text}");
            window.speechSynthesis.speak(utterance);
        </script>
    """, unsafe_allow_html=True)

st.title("Synthèse Vocale dans Streamlit")

# Exemple de texte à dire
texte_a_dire = st.text_input("Entrez le texte à dire", "Bonjour, bienvenue sur notre application!")

if st.button("Dire le texte"):
    say(texte_a_dire)
