import random
import streamlit as st
import streamlit.components.v1 as components

# Liste des joueurs
joueurs = ["Georges", "Cécile", "Isabelle", "Alix"]

# Liste des rôles disponibles (1 rôle par joueur)
roles_disponibles = ["Loup Garou", "Sorcière", "Voyante", "Villageois"]

# Attribution des rôles de manière aléatoire
if 'roles' not in st.session_state:
    roles = {}
    for joueur in joueurs:
        role = random.choice(roles_disponibles)
        roles[joueur] = role
        roles_disponibles.remove(role)
    st.session_state.roles = roles

# Fonction pour la synthèse vocale
def say(text):
    components.html(f"""
        <script type="text/javascript">
            var utterance = new SpeechSynthesisUtterance("{text}");
            window.speechSynthesis.speak(utterance);
        </script>
    """, height=0)

# Afficher les rôles des joueurs restants
def afficher_roles():
    st.header("Rôles des joueurs restants")
    for joueur, role in st.session_state.roles.items():
        with st.expander(f"Voir le rôle de {joueur}"):
            st.write(f"{joueur} est {role}.")
