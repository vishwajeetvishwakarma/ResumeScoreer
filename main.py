import streamlit as st
import fitz # PyMuPDF
import docx
import io
from models.preprocessing import matched_skills


def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to extract text from a DOC
def extract_text_from_doc(doc_file):
    doc = docx.Document(doc_file)
    text = " ".join([paragraph.text for paragraph in doc.paragraphs])
    return text

# Function to handle file upload and text extraction
def handle_file_upload(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            text = extract_text_from_doc(uploaded_file)
        else: # Assuming plain text
            text = uploaded_file.read().decode("utf-8")
        return text
    return None

# Streamlit app
st.set_page_config(layout="wide")

st.title("Resume and Company Requirement Matcher")

# Create columns for resume and company requirements
col1, col2 = st.columns(2)


with col1:
    st.header("Resume")
    tab1 , tab2 = st.tabs(["File Upload" , "Text Input"])
    with tab1:
        resume_uploaded_file = st.file_uploader("Upload your resume (PDF, DOC, DOCX, or plain text)", type=["pdf", "doc", "docx", "txt"])

    with tab2:
        resume_text = st.text_area("Enter or paste your resume text here:")

with col2:
    st.header("Company Requirements")
    tab3, tab4 = st.tabs(["File Upload", "Text Input"])
    with tab3:
        company_uploaded_file = st.file_uploader("Upload your company requirements (PDF, DOC, DOCX, or plain text)", type=["pdf", "doc", "docx", "txt"])
    with tab4:
        company_desc = st.text_area("Enter or paste your company description text here:")

# Process uploaded files or use text inputs
if resume_uploaded_file:
    resume_text = handle_file_upload(resume_uploaded_file)
    if not resume_text:
        st.write("Failed to extract text from the uploaded resume document.")
elif company_uploaded_file:
    company_desc = handle_file_upload(company_uploaded_file)
    if not company_desc:
        st.write("Failed to extract text from the uploaded company requirements document.")


if st.button("Submit"):
    if resume_text and company_desc:
        person_skills, company_skills, total_matched, all_person_skills, all_company_skills = matched_skills(resume_text, company_desc)
        st.write(f"Total Person Skills: {person_skills}")
        st.write(f"Total Company Requirement Skills: {company_skills}")
        st.write(f"Total Matched Skills: {total_matched}")
        st.write(f"All Person Skills: {all_person_skills}")
        st.write(f"All Company Requirement Skills: {all_company_skills}")
    else:
        st.write("Please upload a document or enter text in the provided fields.")