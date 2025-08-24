from Config import constants as const
import streamlit as st
import requests
import os

st.set_page_config(layout="wide")
st.title("📄 AI Document Assessor")

# API URL
API_URL = const.API_URL

# Default Guidelines
default_guidelines = const.DEFAULT_GUIDELINES

st.sidebar.header("Controls")
uploaded_file = st.sidebar.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])
guidelines = st.sidebar.text_area("Enter Assessment Guidelines", default_guidelines, height=300)

col1, col2 = st.columns(2)

with col1:
    st.header("Assessment")
    if st.button("Assess Document"):
        if uploaded_file is not None:
            with st.spinner("Assessing document..."):
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {'guidelines': guidelines}
                try:
                    response = requests.post(f"{API_URL}/assess/", files=files, data=data)
                    if response.status_code == const.STATUS_CODE["SUCCESS"]:
                        report = response.json().get('report', 'No report generated.')
                        st.subheader("Assessment Report")
                        st.markdown(report)
                        st.session_state.assessment_report = report
                    else:
                        st.error(f"Error from API: {response.text}")
                except requests.exceptions.ConnectionError as e:
                    st.error(f"Could not connect to the API. Make sure the FastAPI server is running. Details: {e}")
        else:
            st.warning("Please upload a document first.")

with col2:
    st.header("Modification")
    modification_request = st.text_input("Request for modification (e.g., 'Fix all grammar issues')", "Fix all issues based on the guidelines.")
    
    if st.button("Modify Document"):
        if uploaded_file is not None:
            with st.spinner("Modifying document..."):
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {'guidelines': guidelines, 'request': modification_request}
                try:
                    response = requests.post(f"{API_URL}/modify/", files=files, data=data)
                    if response.status_code == const.STATUS_CODE["SUCCESS"]:
                        modified_text = response.text
                        st.subheader("Modified Document Content")
                        st.text_area("Modified Text", modified_text, height=400)
                        
                        st.download_button(
                           label="Download Modified Text",
                           data=modified_text,
                           file_name=f"modified_{uploaded_file.name}.txt",
                           mime="text/plain",
                        )
                    else:
                        st.error(f"Error from API: {response.text}")
                except requests.exceptions.ConnectionError as e:
                    st.error(f"Could not connect to the API. Make sure the FastAPI server is running. Details: {e}")
        else:
            st.warning("Please upload a document first.")
