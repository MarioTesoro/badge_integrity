import streamlit as st
from auth.firebase_app import login
from dotenv import load_dotenv
import os
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import apply_base_styles

st.set_page_config(page_title="Login | Badge Integrity", layout="wide", initial_sidebar_state="collapsed")
apply_base_styles()

load_dotenv()
profile = st.session_state.get("profile", "Verifier")

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Access</div>
        <h1>Welcome back.</h1>
        <p>Sign in to continue to your dashboard.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="app-card">', unsafe_allow_html=True)
form = st.form("login")
email = form.text_input("Email")
password = form.text_input("Password", type="password")
st.markdown('<p class="field-hint">Use the institute credentials from your .env when logging in as an institute.</p>', unsafe_allow_html=True)

if profile != "Institute":
    clicked_register = st.button("New user? Click here to register!")

    if clicked_register:
        switch_page("register")

submit = form.form_submit_button("Login")
if submit:
    if profile == "Institute":
        valid_email = os.getenv("institute_email")
        valid_pass = os.getenv("institute_password")
        if email == valid_email and password == valid_pass:
            switch_page("institute")
        else:
            st.error("Invalid credentials!")
    else:
        result = login(email, password)
        if result == "success":
            st.success("Login successful!")
            switch_page("verifier")
        else:
            st.error("Invalid credentials!")
st.markdown("</div>", unsafe_allow_html=True)
        
