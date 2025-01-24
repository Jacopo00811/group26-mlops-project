import os

import requests
import streamlit as st
from google.cloud import run_v2


@st.cache_resource
def get_backend_url():
    """Get the URL of the backend service."""
    parent = "projects/adroit-chemist-447918-n1/locations/europe-west1"
    client = run_v2.ServicesClient()
    services = client.list_services(parent=parent)
    for service in services:
        if service.name.split("/")[-1] == "api":
            return service.uri
    name = os.environ.get("BACKEND", None)
    return name


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
# FastAPI backend URL
API_URL = get_backend_url()

# Title of the app
st.title("Danish to English Translator using LLMs")

# Instructions
st.markdown("Enter some Danish text below, and click 'Process' to see the output.")

# Input: Text
input_text = st.text_area("Input Danish", height=150)

# Button to trigger processing
if st.button("Process"):
    if input_text:
        # Send the request to the FastAPI backend
        response = requests.post(API_URL + "/process-text/", json={"text": input_text})

        if response.status_code == 200:
            # Get the output from the API response
            processed_text = response.json()["text"]
            st.subheader("Processed Text")
            st.write(processed_text)
        else:
            st.error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
    else:
        st.warning("Please enter some text to process.")
