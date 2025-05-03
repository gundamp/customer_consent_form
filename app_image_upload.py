import streamlit as st
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# --- Load credentials from Streamlit secrets ---
creds_dict = st.secrets["gcp_service_account"]
folder_id = st.secrets["drive_folder_id"]

# --- Authenticate ---
scope = ["https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
gauth = GoogleAuth()
gauth.credentials = creds
drive = GoogleDrive(gauth)

# --- Streamlit Form ---
st.title("Upload Image to Google Drive")

with st.form("upload_form"):
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    submit = st.form_submit_button("Upload")

    if uploaded_file and submit:
        # Save to temp file
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Upload to Google Drive
        file_drive = drive.CreateFile({
            'title': uploaded_file.name,
            'parents': [{"id": folder_id}]
        })
        file_drive.SetContentFile(uploaded_file.name)
        file_drive.Upload()

        # Cleanup
        os.remove(uploaded_file.name)

        st.success(f"Uploaded: {uploaded_file.name}")
        st.markdown(f"[View on Google Drive]({file_drive['alternateLink']})")





