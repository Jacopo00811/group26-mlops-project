import requests
import streamlit as st

# FastAPI backend URL
API_URL = "http://localhost:8000/process-text/"

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
st.title(
    "This was supposed to be Danish to English but our model never got trained and the DA-EN Helenski transformers package didn't work"
)

# Instructions
st.markdown("Enter some English text below, and click 'Process' to see the output.")

# Input: Text
input_text = st.text_area("Input English", height=150)

# Button to trigger processing
if st.button("Process"):
    if input_text:
        # Send the request to the FastAPI backend
        response = requests.post(API_URL, json={"text": input_text})

        if response.status_code == 200:
            # Get the output from the API response
            processed_text = response.json()["text"]
            st.subheader("Processed Text")
            st.write(processed_text)
        else:
            st.error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
    else:
        st.warning("Please enter some text to process.")
