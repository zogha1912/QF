import streamlit as st
import requests

st.set_page_config(page_title="Office Management Assistant", layout="wide")

# --- Session State Initialization ---
if "token" not in st.session_state:
    st.session_state.token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# --- LOGIN PAGE ---
if not st.session_state.token:
    st.title("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            res = requests.post("http://localhost:8000/auth/login/form", data={
                "username": email,
                "password": password
            })

            if res.status_code == 200:
                data = res.json()
                st.session_state.token = data["access_token"]
                st.session_state.user_info = data["user"]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

# --- MAIN APP AFTER LOGIN ---
else:
    role = st.session_state.user_info["role"]
    name = st.session_state.user_info["name"]
    st.sidebar.write(f"👤 Logged in as: {name} ({role})")

    # Employee Page
    if role == "employee":
        st.title("Employee: Attestation Portal")
        tabs = st.tabs(["Request Attestation", "Check Status"])

        with tabs[0]:
            st.subheader("Request a Self Attestation")
            user_input = st.text_area("Type your request", placeholder="I need a proof of employment...")

            if st.button("Submit Request"):
                headers = {"Authorization": f"Bearer {st.session_state['token']}"}
                res = requests.post(
                    "http://localhost:8000/attestation/classify/",
                    json={"user_input": user_input},
                    headers=headers
                )

                if res.status_code == 200:
                    if "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in res.headers.get("content-type", ""):
                        st.success("Your attestation has been submitted for approval.")
                    else:
                        st.json(res.json())
                else:
                    st.error(res.text)

        with tabs[1]:
            st.subheader("Query Request Status")
            query = st.text_area("Ask about your attestation", placeholder="What's the status of my attestation?")

            if st.button("Check Status"):
                headers = {"Authorization": f"Bearer {st.session_state['token']}"}
                res = requests.post(
                    "http://localhost:8000/attestation/query-status",
                    json={"user_input": query},
                    headers=headers
                )
                if res.status_code == 200:
                    st.success(res.json().get("message"))
                else:
                    st.error(res.text)

    # Office Manager Page
    elif role == "office_manager":
        st.title("Office Manager Dashboard")

        st.subheader("Pending Attestation Requests")
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        res = requests.get("http://localhost:8000/attestation/pending", headers=headers)

        if res.status_code == 200:
            requests_list = res.json()
            for req in requests_list:
                with st.expander(f"{req['employee_name']} - {req['job_title']}"):
                    st.write(f" Request Date: {req['current_request_date']}")
                    st.write(f" Last Request: {req['last_request_date'] or 'N/A'}")
                    
                    col1, col2 = st.columns(2)
                    if col1.button(" Approve", key=f"approve_{req['request_id']}"):
                        res_approve = requests.post(
                            f"http://localhost:8000/attestation/approve/{req['request_id']}",
                            headers=headers
                        )
                        if res_approve.status_code == 200:
                            st.success("Approved. Attestation generated.")
                            st.download_button(
                                label=" Download Attestation",
                                data=res_approve.content,
                                file_name=f"attestation_{req['employee_name']}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                        else:
                            st.error(res_approve.text)


                    if col2.button(" Reject", key=f"reject_{req['request_id']}"):
                        res_reject = requests.post(
                            f"http://localhost:8000/attestation/reject/{req['request_id']}",
                            headers=headers
                        )
                        if res_reject.status_code == 200:
                            st.warning("Request rejected.")
                        else:
                            st.error(res_reject.text)

        else:
            st.error("Failed to fetch pending requests.")

    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.user_info = None
        st.rerun()
