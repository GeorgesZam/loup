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
    
    if 'voyante_intro_done' not in st.session_state:
        say("Le village se réveille. La voyante ouvre les yeux.")
        st.session_state.voyante_intro_done = True
    
    if voyante:
        voyante = voyante[0]
        victime = st.selectbox(f"{voyante}, choisissez un joueur à sonder:", [j for j in st.session_state.roles.keys() if j != voyante], key=f"voyante_select_{st.session_state.phase}")
        if st.button("Révéler le rôle", key=f"reveler_voyante_{st.session_state.phase}"):
            st.write(f"Le rôle de {victime} est {st.session_state.roles[victime]}.")
            say(f"Le rôle de {victime} est {st.session_state.roles[victime]}.")
            st.session_state.voyante_done = True
    
    if 'voyante_done' in st.session_state:
        say("La voyante ferme les yeux. Le village se rendort.")

# Phase du Loup Garou
def phase_loup_garou():
    if 'loup_garou_intro_done' not in st.session_state:
        say("Le loup-garou se réveille.")
        st.session_state.loup_garou_intro_done = True
    
    st.header("Phase du Loup Garou")
    loups_garous = [joueur for joueur, role in st.session_state.roles.items() if role == "Loup Garou"]
    if loups_garous:
        victime = st.selectbox(
            f"{', '.join(loups_garous)}, choisissez votre victime:", 
            [j for j in st.session_state.roles.keys() if j not in loups_garous],
            key=f"victime_select_{st.session_state.phase}"  # Utilisation d'une clé unique
        )
        if st.button("Confirmer la victime", key=f"confirmer_victime_{st.session_state.phase}"):
            st.session_state.victime_morte = f"{victime} a été tué(e). Son rôle était {st.session_state.roles[victime]}."
            st.write(f"**{st.session_state.victime_morte}**")
            say(f"{victime} a été tué(e). Son rôle était {st.session_state.roles[victime]}.")
            del st.session_state.roles[victime]  # Supprime le joueur mort
            st.session_state.loup_garou_done = True
    
    if 'loup_garou_done' in st.session_state:
        say("Le loup-garou ferme les yeux. Le village se rendort.")

# Phase de Vote des Villageois
def phase_villageois():
    if 'villageois_intro_done' not in st.session_state:
        say("Le village se réveille pour le vote.")
        st.session_state.villageois_intro_done = True
    
    st.header("Phase du Vote des Villageois")
    vote = st.selectbox("Villageois, choisissez un joueur à éliminer:", [j for j in st.session_state.roles.keys()], key=f"vote_village_{st.session_state.phase}")
    if st.button("Confirmer l'élimination", key=f"eliminer_vote_{st.session_state.phase}"):
        st.session_state.victime_votee = f"{vote} a été éliminé(e). Son rôle était {st.session_state.roles[vote]}."
        st.write(f"**{st.session_state.victime_votee}**")
        say(f"{vote} a été éliminé(e). Son rôle était {st.session_state.roles[vote]}.")
        del st.session_state.roles[vote]  # Supprime le joueur éliminé
        st.session_state.villageois_done = True

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

# Affichage permanent des victimes
if 'victime_morte' in st.session_state:
    st.write(f"**{st.session_state.victime_morte}**")

if 'victime_votee' in st.session_state:
    st.write(f"**{st.session_state.victime_votee}**")

if not verifier_fin_partie():
    phases[st.session_state.phase]()
    if st.button("Passer à la phase suivante"):
        # Réinitialiser les états de la phase précédente
        for key in ['voyante_intro_done', 'voyante_done', 'loup_garou_intro_done', 'loup_garou_done', 'villageois_intro_done', 'villageois_done']:
            if key in st.session_state:
                del st.session_state[key]
        
        st.session_state.phase = (st.session_state.phase + 1) % len(phases)

if verifier_fin_partie():
    st.write("Fin du jeu.")
