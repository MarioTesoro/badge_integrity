import streamlit as st
import os
import hashlib
from utils.cert_utils import extract_certificate
from utils.streamlit_utils import get_certificate_ipfs_hash
from connection import contract
from utils.streamlit_utils import displayPDF, apply_base_styles

st.set_page_config(page_title="Verifier | Badge Integrity", layout="wide", initial_sidebar_state="collapsed")
apply_base_styles()

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Verifier Console</div>
        <h1>Confirm credentials with confidence.</h1>
        <p>Validate a certificate using the PDF or by entering the certificate ID.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs(["Verify by PDF", "Verify by Certificate ID"])

with tabs[0]:
    # Validate by extracting data from the PDF and recomputing the hash.
    uploaded_file = st.file_uploader("Upload the certificate PDF", type=["pdf"])
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        with open("certificate.pdf", "wb") as file:
            file.write(bytes_data)
        try:
            (uid, candidate_name, course_name, org_name) = extract_certificate("certificate.pdf")
            displayPDF("certificate.pdf")
            os.remove("certificate.pdf")

            data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode("utf-8")
            certificate_id = hashlib.sha256(data_to_hash).hexdigest()
            if contract is None:
                st.error("Smart contract not configured. Check deployment and connection.")
            else:
                result = contract.functions.isVerified(certificate_id).call()
                if result:
                    st.success("Certificate validated successfully.")
                else:
                    st.error("Certificate not found on-chain.")
        except Exception:
            st.error("Certificate validation failed.")

with tabs[1]:
    # Validate directly using a provided certificate ID.
    form = st.form("Validate-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Validate Certificate", use_container_width=True)
    if submit:
        try:
            ipfs_hash = get_certificate_ipfs_hash(certificate_id)
            pinata_gateway_base_url = "https://gateway.pinata.cloud/ipfs"
            content_url = f"{pinata_gateway_base_url}/{ipfs_hash}"
            if contract is None:
                st.error("Smart contract not configured. Check deployment and connection.")
            result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Certificate validated successfully.")
            else:
                st.error("Certificate not found on-chain.")
        except Exception:
            st.error("Certificate validation failed.")
