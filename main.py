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

# Phase de la Voyante
def phase_voyante():
    st.header("Phase de la Voyante")
    voyante = [joueur for joueur, role in st.session_state.roles.items() if role == "Voyante"]
    if voyante:
        voyante = voyante[0]
        victime = st.selectbox(f"{voyante}, choisissez un joueur à sonder:", [j for j in st.session_state.roles.keys() if j != voyante])
        if st.button("Révéler le rôle"):
            st.write(f"Le rôle de {victime} est {st.session_state.roles[victime]}.")
    else:
        st.write("Il n'y a pas de Voyante dans cette partie.")

# Phase du Loup Garou
def phase_loup_garou():
    st.header("Phase du Loup Garou")
    loup_garou = [joueur for joueur, role in st.session_state.roles.items() if role == "Loup Garou"]
    if loup_garou:
        loup_garou = loup_garou[0]
        victime = st.selectbox(f"{loup_garou}, choisissez votre victime:", [j for j in st.session_state.roles.keys() if j != loup_garou])
        if st.button("Confirmer la victime"):
            st.write(f"{victime} a été tué(e). Son rôle était {st.session_state.roles[victime]}.")
            say(f"{victime} a été tué(e). Son rôle était {st.session_state.roles[victime]}.")
            del st.session_state.roles[victime]  # Supprime le joueur mort
    else:
        st.write("Il n'y a pas de Loup Garou dans cette partie.")

# Phase de Vote des Villageois
def phase_villageois():
    st.header("Phase du Vote des Villageois")
    vote = st.selectbox("Villageois, choisissez un joueur à éliminer:", [j for j in st.session_state.roles.keys()])
    if st.button("Confirmer l'élimination"):
        st.write(f"{vote} a été éliminé(e). Son rôle était {st.session_state.roles[vote]}.")
        say(f"{vote} a été éliminé(e). Son rôle était {st.session_state.roles[vote]}.")
        del st.session_state.roles[vote]  # Supprime le joueur éliminé

# Vérification des conditions de fin de partie
def verifier_fin_partie():
    loup_garou_restant = [joueur for joueur, role in st.session_state.roles.items() if role == "Loup Garou"]
    villageois_restants = [joueur for joueur, role in st.session_state.roles.items() if role != "Loup Garou"]
    
    if not loup_garou_restant:
        st.write("Les villageois ont gagné. Tous les Loups Garous sont morts.")
        say("Les villageois ont gagné. Tous les Loups Garous sont morts.")
        return True
    elif len(villageois_restants) <= 1:
        st.write("Les Loups Garous ont gagné. Ils ont pris le contrôle du village.")
        say("Les Loups Garous ont gagné. Ils ont pris le contrôle du village.")
        return True
    return False

# Jeu principal
st.title("Jeu de Loup Garou")
if 'phase' not in st.session_state:
    st.session_state.phase = 0

phases = [phase_voyante, phase_loup_garou, phase_villageois]

# Affichage des rôles avant chaque phase
afficher_roles()

if not verifier_fin_partie():
    phases[st.session_state.phase]()
    if st.button("Passer à la phase suivante"):
        st.session_state.phase = (st.session_state.phase + 1) % len(phases)

if verifier_fin_partie():
    st.write("Fin du jeu.")
