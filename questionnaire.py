import pandas as pd
from datetime import datetime
import streamlit as st

# Définir le fichier CSV local pour enregistrer les réponses
csv_file = "questionnaire_responses.csv"

# Charger ou créer le fichier CSV
try:
    questionnaire_df = pd.read_csv(csv_file)
except FileNotFoundError:
    questionnaire_df = pd.DataFrame(columns=["Date", "Nom", "Satisfaction (%)", "Commentaires"])

st.title("Questionnaire de Satisfaction")

# Formulaire pour le questionnaire
with st.form("questionnaire_form"):
    nom = st.text_input("Votre prénom (optionnel)")
    satisfaction = st.slider("Êtes-vous satisfait(e) du congé menstruel ?", 0, 100, 50)
    commentaires = st.text_area("Commentaires ou suggestions")
    submitted = st.form_submit_button("Soumettre")

    if submitted:
        # Ajouter une nouvelle réponse sous forme de DataFrame temporaire
        new_response = pd.DataFrame({
            "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Nom": [nom],
            "Satisfaction (%)": [satisfaction],
            "Commentaires": [commentaires]
        })
        # Concaténer les données
        questionnaire_df = pd.concat([questionnaire_df, new_response], ignore_index=True)
        # Sauvegarder les données mises à jour dans le fichier CSV
        questionnaire_df.to_csv(csv_file, index=False)
        st.success("Merci pour votre retour !")

# Afficher les réponses existantes
if not questionnaire_df.empty:
    st.write("### Réponses soumises")
    st.dataframe(questionnaire_df)
