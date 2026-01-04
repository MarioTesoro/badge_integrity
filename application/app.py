import streamlit as st
from PIL import Image
from utils.streamlit_utils import apply_base_styles
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Badge Integrity", layout="wide", initial_sidebar_state="collapsed")
apply_base_styles()

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Badge Integrity</div>
        <h1>Certificate trust, without the paper chase.</h1>
        <p>Issue verifiable credentials, anchor them on-chain, and give employers a simple way to validate in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Role selector cards.
col1, col2 = st.columns(2, gap="large")
institite_logo = Image.open("../assets/institute_logo.png")
with col1:
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.image(institite_logo, output_format="jpg", width=210)
    st.markdown("### Institute Portal")
    st.markdown('<p class="card-muted">Generate certificates, pin PDFs to IPFS, and register hashes on-chain.</p>', unsafe_allow_html=True)
    clicked_institute = st.button("Enter as Institute", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

company_logo = Image.open("../assets/company_logo.jpg")
with col2:
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.image(company_logo, output_format="jpg", width=210)
    st.markdown("### Verifier Portal")
    st.markdown('<p class="card-muted">Validate credentials with a certificate ID or PDF upload.</p>', unsafe_allow_html=True)
    clicked_verifier = st.button("Enter as Verifier", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

if clicked_institute:
    st.session_state.profile = "Institute"
    switch_page('login')
elif clicked_verifier:
    st.session_state.profile = "Verifier"
    switch_page('login')

# import subprocess
# import sys

# # Path to your Streamlit app
# app_path = 'app.py'

# # Run Streamlit app
# subprocess.run([sys.executable, '-m', 'streamlit', 'run', app_path])
