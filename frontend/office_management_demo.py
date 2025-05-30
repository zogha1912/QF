import streamlit as st
import requests

st.set_page_config(page_title="Office Management Assistant", layout="wide")
st.title(" Office Management Assistant")

# Session State for token
if "token" not in st.session_state:
    st.session_state["token"] = None

# --- Login Section ---
st.subheader(" Login")

with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

    if submit:
        res = requests.post("http://localhost:8000/auth/login/form", data={
            "username": email,
            "password": password
        })
        if res.status_code == 200:
            data = res.json()
            st.success("Logged in successfully")
            st.session_state["token"] = data["access_token"]
            st.session_state["user_info"] = data["user"]
        else:
            st.error("Invalid credentials")

# --- If logged in ---
if st.session_state["token"]:
    st.success(f"Welcome {st.session_state['user_info']['name']}")

    tabs = st.tabs([" Request Attestation", " Check Status"])

    # --- Tab 1: Request Attestation
    with tabs[0]:
        st.subheader("Request a Self Attestation")
        user_input = st.text_area("Type your request", placeholder="I need a proof of employment document...")

        if st.button("Submit Request"):
            headers = {"Authorization": f"Bearer {st.session_state['token']}"}
            res = requests.post(
                "http://localhost:8000/attestation/classify/",
                json={"user_input": user_input},
                headers=headers
            )

            if res.status_code == 200:
                if "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in res.headers.get("content-type", ""):
                    with open("attestation.docx", "wb") as f:
                        f.write(res.content)
                    st.success(" Attestation generated!")
                    with open("attestation.docx", "rb") as file:
                        st.download_button("📥 Download", file, file_name="attestation.docx")
                else:
                    st.json(res.json())
            else:
                st.error(res.text)

    # --- Tab 2: Check Status
    with tabs[1]:
        st.subheader("Query Request Status")
        query = st.text_area("Ask about your attestation", placeholder="What's the status of my request?")

        if st.button("Check Status"):
            headers = {"Authorization": f"Bearer {st.session_state['token']}"}
            res = requests.post(
                "http://localhost:8000/attestation/query-status",
                json={"user_input": query},
                headers=headers
            )
            if res.status_code == 200:
                st.success(res.json().get("message"))
                st.json(res.json())
            else:
                st.error(res.text)

else:
    st.warning("Please log in to continue.")
