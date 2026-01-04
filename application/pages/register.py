import streamlit as st
from auth.firebase_app import register
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import apply_base_styles

st.set_page_config(page_title="Register | Badge Integrity", layout="wide", initial_sidebar_state="collapsed")
apply_base_styles()

profile = st.session_state.get("profile", "Verifier")

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Register</div>
        <h1>Create your verifier account.</h1>
        <p>Get started with secure certificate validation in minutes.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="app-card">', unsafe_allow_html=True)
form = st.form("login")
email = form.text_input("Email")
password = form.text_input("Password", type="password")
clicked_login = st.button("Already registered? Click here to login!")

if clicked_login:
    switch_page("login")
    
submit = form.form_submit_button("Register")
if submit:
    result = register(email, password)
    if result == "success":
        st.success("Registration successful!")
        if profile == "Institute":
            switch_page("institute")
        else:
            switch_page("verifier")
    else:
        st.error("Registration unsuccessful!")
st.markdown("</div>", unsafe_allow_html=True)
