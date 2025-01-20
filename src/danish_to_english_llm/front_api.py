# streamlit_app.py
import requests
import streamlit as st

# FastAPI backend URL (adjust this if you're deploying locally or on a server)
API_URL = "http://localhost:8000/translate/"

# Streamlit page configuration
st.set_page_config(page_title="Danish to English Translator", layout="wide")
st.markdown(
    """
    <style>
    * {
        font-family: "Comic Sans MS", "Comic Sans", cursive !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Title of the app
st.title("Danish to English Translation")

# Instructions
st.markdown("Enter some Danish text below, and click 'Translate' to get the English translation.")

# Input: Danish text
danish_text = st.text_area("Danish Text", height=150)

# Button to trigger translation
if st.button("Translate"):
    if danish_text:
        # Send the request to the FastAPI backend for translation
        response = requests.post(API_URL, json={"danish_text": danish_text})

        if response.status_code == 200:
            # Get the translation from the API response
            english_text = response.json()["english_text"]
            st.subheader("Translated Text")
            st.write(english_text)
        else:
            st.error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
    else:
        st.warning("Please enter some Danish text to translate.")
