import streamlit as st
import requests
from datetime import datetime
if "access_token" not in st.session_state:
    st.title(" Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post("http://localhost:8000/auth/login/form", data={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            st.session_state["access_token"] = response.json()["access_token"]
            st.success("Login successful. Reloading...")
            st.rerun()
        else:
            st.error("Login failed. Please check your credentials.")

    st.stop()  # Stop here until user logs in

st.title(" Attestation Approval Dashboard")

token = st.session_state.get("access_token")
headers = {"Authorization": f"Bearer {token}"}

response = requests.get("http://localhost:8000/attestation/pending", headers=headers)

if response.status_code == 200:
    pending_requests = response.json()

    for req in pending_requests:
        st.subheader(f"Request ID: {req['request_id']}")
        st.write(f" Employee: {req['employee_name']}")
        st.write(f" Job Title: {req['job_title']}")
        st.write(f" Requested on: {req['current_request_date']}")
        if req['last_request_date']:
            st.write(f" Previous request: {req['last_request_date']}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f" Approve {req['request_id']}"):
                res = requests.post(f"http://localhost:8000/attestation/approve/{req['request_id']}", headers=headers)
                st.success(res.json()["message"])
        with col2:
            if st.button(f" Reject {req['request_id']}"):
                res = requests.post(f"http://localhost:8000/attestation/reject/{req['request_id']}", headers=headers)
                st.success(res.json()["message"])
else:
    st.error("Error fetching requests.")
