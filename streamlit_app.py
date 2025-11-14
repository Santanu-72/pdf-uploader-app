import streamlit as st
import requests
import time

# --- Configuration ---

# PASTE YOUR N8N PRODUCTION WEBHOOK URL HERE
# This is the 'Production URL' from your n8n Webhook node
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/pdf-receiver"

# --- App Layout ---
st.set_page_config(page_title="PDF Submission Portal", layout="centered")

st.title("📄 PDF Submission Portal")
st.write("Upload your PDF document below. A confirmation email will be sent upon receipt.")

# Check if the webhook URL has been changed from default
if N8N_WEBHOOK_URL == "http://localhost:5678/webhook/pdf-receiver":
    st.error("Error: App is not configured. Please update the N8N_WEBHOOK_URL in the code.")
else:
    # File Uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # This is the "Submit" button
        if st.button("Submit PDF", type="primary"):
            
            # Show a spinner while processing
            with st.spinner('Submitting your file... Please wait.'):
                
                # --- This is the core logic ---
                try:
                    # We will send a JSON payload to the n8n webhook
                    # We are not sending the file itself, just a notification that it was received.
                    # This is faster, more reliable, and avoids webhook size limits.
                    payload = {
                        "filename": uploaded_file.name,
                        "file_size_bytes": uploaded_file.size,
                        "file_type": uploaded_file.type
                    }

                    # Make the POST request to the n8n webhook
                    response = requests.post(N8N_WEBHOOK_URL, json=payload)
                    
                    # --- Handle Response ---
                    if response.status_code == 200:
                        # Success!
                        st.success("Success! Your file submission has been received.")
                        st.balloons()
                        st.write(f"**Filename:** `{uploaded_file.name}`")
                        st.write("You will receive a confirmation email shortly.")
                    else:
                        # Handle errors from the n8n side
                        st.error(f"Error: Could not trigger workflow. (Status code: {response.status_code})")

                except requests.exceptions.RequestException as e:
                    # Handle network errors
                    st.error(f"An error occurred while connecting to the server: {e}")
                except Exception as e:
                    # Handle other unexpected errors

                    st.error(f"An unexpected error occurred: {e}")

