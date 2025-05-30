import streamlit as st
import requests

st.set_page_config(page_title="Recruitment Agent Demo", layout="centered")
st.title(" Recruitment Agent Demo")

tab1, tab2, tab3, tab4 = st.tabs([
    " Recruiter Chat",
    " Clarify Request",
    " Resume Report Generator",
    " CV Classifier"
])

### --- TAB 1: Smart Recruiter Chat ---
with tab1:
    st.subheader(" Send a job request in natural language")

    recruiter_input = st.text_area("What do you want?", placeholder="E.g., I need a backend dev for our Django project...")
    
    if st.button("Process Request", key="process"):
        res = requests.post("http://localhost:8000/recruiter/process", json={"text": recruiter_input})
        data = res.json()

        st.json(data)

        if data.get("input_type") == "VAGUE":
            st.warning("The input was vague. Save this ID to clarify later:")
            st.code(data.get("clarification_id"))

### --- TAB 2: Clarify Vague Request ---
with tab2:
    st.subheader(" Clarify a previously vague request")

    clarification_id = st.text_input("Clarification ID")
    answer = st.text_area("Clarify your intent", placeholder="We need someone who knows FastAPI, 2 years experience...")

    if st.button("Submit Clarification", key="clarify"):
        res = requests.post("http://localhost:8000/recruiter/clarification/respond", json={
            "clarification_id": clarification_id,
            "answers": answer
        })
        st.json(res.json())

### --- TAB 3: Candidate Report Generator ---
with tab3:
    st.subheader(" Upload CVs to generate tailored reports")
    uploaded_files = st.file_uploader("Upload PDF resumes", type=["pdf"], accept_multiple_files=True)
    position = st.text_input("Position you're hiring for")

    if st.button("Generate Reports", key="report"):
        files = [("files", (f.name, f.getvalue(), "application/pdf")) for f in uploaded_files]
        response = requests.post(
            "http://localhost:8000/generate-reports/",
            data={"position": position},
            files=files
        )
        st.json(response.json())
### --- TAB 4: CV Classifier ---
with tab4:
    st.subheader(" Upload CVs and classify them against a job description")

    job_desc = st.text_area("Job Description", height=150, placeholder="E.g., We're hiring a frontend dev with React and Tailwind...")

    uploaded_files = st.file_uploader("Upload multiple CV PDFs", type=["pdf"], accept_multiple_files=True)

    if st.button("Classify CVs", key="classify"):
        if not uploaded_files or not job_desc:
            st.warning("Please provide both CVs and a job description.")
        else:
            files = [("files", (f.name, f.read(), "application/pdf")) for f in uploaded_files]

            response = requests.post(
                "http://localhost:8000/classify-multiple",
                files=files,
                data={"job_desc": job_desc}
            )

            if response.status_code == 200:
                results = response.json()["results"]
                st.success("Classification Results:")
                for result in results:
                    st.markdown(f"**📄 {result['file_name']}**")
                    st.json(result["classification"])
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
