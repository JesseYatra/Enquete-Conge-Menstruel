import pandas as pd
from datetime import datetime
import streamlit as st
import gdown

# ID du fichier Google Drive
file_id = "1hJvFX7xmJhUOBsuUbx1lw5Sf55Q3Vt8okspMHS5YX4Y"
download_url = f"https://drive.google.com/uc?id={file_id}"

# Télécharger le fichier CSV depuis Google Drive
csv_file = "questionnaire_responses.csv"
try:
    gdown.download(download_url, csv_file, quiet=False)
    questionnaire_df = pd.read_csv(csv_file)
except Exception as e:
    st.warning("Impossible de télécharger le fichier. Un fichier vierge sera créé.")
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
        # Sauvegarder les données mises à jour dans le fichier local
        questionnaire_df.to_csv(csv_file, index=False)
        
        # Réupload du fichier vers Google Drive
        try:
            gdown.upload(csv_file, file_id)
            st.success("Merci pour votre retour ! Les données ont été mises à jour.")
        except Exception as e:
            st.error("Erreur lors de la mise à jour du fichier sur Google Drive.")
            st.write(e)

# Afficher les réponses existantes
if not questionnaire_df.empty:
    st.write("### Réponses soumises")
    st.dataframe(questionnaire_df)
