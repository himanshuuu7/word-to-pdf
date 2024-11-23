import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import io

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000/convert"

st.title("Word to PDF Converter with Authentication")
st.write("Upload a Word file, enter your credentials, and we'll convert it to a PDF for you!")

# Input username and password
username = st.text_input("Username", type="default")
password = st.text_input("Password", type="password")

# File uploader
uploaded_file = st.file_uploader("Upload a Word document", type=["docx", "doc"])

if uploaded_file is not None and username and password:
    # Display file name
    st.write(f"Uploaded file: {uploaded_file.name}")

    # Convert button
    if st.button("Convert to PDF"):
        try:
            # Convert the uploaded file to a BytesIO object to avoid `SpooledTemporaryFile` issues
            file_content = uploaded_file.read()
            file_buffer = io.BytesIO(file_content)

            # Send the file to the backend with Basic Auth
            files = {
                "file": (uploaded_file.name, file_buffer, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            }
            response = requests.post(
                BACKEND_URL,
                files=files,
                auth=HTTPBasicAuth(username, password)
            )

            if response.status_code == 200:
                # Provide a download link for the converted PDF
                pdf_file = response.content
                converted_file_name = uploaded_file.name.replace(".docx", "_converted.pdf").replace(".doc", "_converted.pdf")
                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name=converted_file_name,
                    mime="application/pdf"
                )
            elif response.status_code == 401:
                st.error("Authentication failed! Please check your username and password.")
            elif response.status_code == 400:
                st.error("Bad request! Please upload a valid Word document.")
            else:
                st.error(f"Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    if not username or not password:
        st.warning("Please enter your username and password.")
