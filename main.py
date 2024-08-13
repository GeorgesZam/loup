import streamlit as st
import streamlit.components.v1 as components

st.title("Synthèse Vocale dans Streamlit")

# Texte à dire
texte_a_dire = st.text_input("Entrez le texte à dire", "Bonjour, bienvenue sur notre application!")

# Bouton pour déclencher la parole
if st.button("Dire le texte"):
    # Code HTML et JavaScript pour déclencher la synthèse vocale
    components.html(f"""
        <script type="text/javascript">
            var utterance = new SpeechSynthesisUtterance("{texte_a_dire}");
            window.speechSynthesis.speak(utterance);
        </script>
    """)

