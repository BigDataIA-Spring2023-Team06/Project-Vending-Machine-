import streamlit as st
import pdfplumber
import os

def read_pdf(file):
    # Load PDF file
    with pdfplumber.open(file) as pdf:
        # Extract text from all pages
        text = ""
        for i in range(len(pdf.pages)):
            text += pdf.pages[i].extract_text()

    return text

def main():
    st.title("Resume Analysis")

    # Upload resume
    st.write("Upload your resume (PDF):")
    resume_file = st.file_uploader("Choose a file", type="pdf")
    if resume_file:
        resume_text = read_pdf(resume_file)

        # Job description input
        st.write("Enter a job description:")
        job_description = st.text_area("Job Description")

        # Submit button
        submitted = st.button("Submit")

        if submitted:
            # Data science and engineering projects
            st.write("Here are some data science and engineering projects you can work on:")
            ds_projects = ["Project 1", "Project 2", "Project 3"]
            de_projects = ["Project A", "Project B", "Project C"]

            # Buttons for data science and data engineering projects
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Work on Data Science", key="ds"):
                    os.system("python datascienceUI.py")

            with col2:
                if st.button("Work on Data Engineering", key="de"):
                    os.system("python dataengineeringUI.py")
                    

if __name__ == "__main__":
    main()
