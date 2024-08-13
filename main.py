import random
import streamlit as st
import streamlit.components.v1 as components

# Liste des joueurs
joueurs = ["Georges", "Cécile", "Isabelle", "Alix"]

# Liste des rôles disponibles (1 rôle par joueur)
roles_disponibles = ["Loup Garou", "Sorcière", "Voyante", "Villageois"]

# Attribution des rôles de manière aléatoire
roles = {}
for joueur in joueurs:
    role = random.choice(roles_disponibles)
    roles[joueur] = role
    roles_disponibles.remove(role)

# Fonction pour la synthèse vocale
def say(text):
    components.html(f"""
        <script type="text/javascript">
            var utterance = new SpeechSynthesisUtterance("{text}");
            window.speechSynthesis.speak(utterance);
        </script>
    """, height=0)

# Affichage des rôles des joueurs dans l'interface Streamlit
st.title("Jeu de Loup Garou")
st.header("Rôles des joueurs")

for joueur, role in roles.items():
    st.write(f"{joueur} est {role}.")
    say(f"{joueur} est {role}.")

# Fonction pour gérer le choix du loup-garou
def choisir_victime():
    victime = st.text_input("Loup Garou, entrez le nom de votre victime:")
    if victime:
        if victime in roles:
            st.write(f"{victime} a été tué(e). Son rôle était {roles[victime]}.")
            say(f"{victime} a été tué(e). Son rôle était {roles[victime]}.")
            del roles[victime]  # Supprime le joueur mort
        else:
            st.write("Ce joueur n'existe pas.")
            say("Ce joueur n'existe pas.")
    
    return victime

# Interface pour la phase du loup-garou
st.header("Phase du Loup Garou")
victime = choisir_victime()

# Vérification des conditions de fin de partie
def verifier_fin_partie():
    loup_garou_restant = [joueur for joueur, role in roles.items() if role == "Loup Garou"]
    villageois_restants = [joueur for joueur, role in roles.items() if role != "Loup Garou"]
    
    if not loup_garou_restant:
        st.write("Les villageois ont gagné. Tous les Loups Garous sont morts.")
        say("Les villageois ont gagné. Tous les Loups Garous sont morts.")
        return True
    elif len(villageois_restants) <= 1:
        st.write("Les Loups Garous ont gagné. Ils ont pris le contrôle du village.")
        say("Les Loups Garous ont gagné. Ils ont pris le contrôle du village.")
        return True
    return False

# Vérification de la fin de la partie
if verifier_fin_partie():
    st.write("Fin du jeu.")
else:
    st.write("Le jeu continue.")
