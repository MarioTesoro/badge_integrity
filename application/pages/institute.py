import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import hashlib
from utils.cert_utils import generate_certificate
from utils.streamlit_utils import view_certificate
from connection import contract, w3
from utils.streamlit_utils import apply_base_styles

st.set_page_config(page_title="Institute | Badge Integrity", layout="wide", initial_sidebar_state="collapsed")
apply_base_styles()

load_dotenv()

api_key = os.getenv("PINATA_API_KEY")
api_secret = os.getenv("PINATA_API_SECRET")


def upload_to_pinata(file_path, api_key, api_secret):
    # Pin a PDF to IPFS via Pinata.
    # Set up the Pinata API endpoint and headers
    pinata_api_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": api_key,
        "pinata_secret_api_key": api_secret,
    }

    # Prepare the file for upload
    with open(file_path, "rb") as file:
        files = {"file": (file.name, file)}

        # Make the request to Pinata
        response = requests.post(pinata_api_url, headers=headers, files=files)
        print(response)
        # Parse the response
        result = json.loads(response.text)
        print(result)
        if "IpfsHash" in result:
            ipfs_hash = result["IpfsHash"]
            print(f"File uploaded to Pinata. IPFS Hash: {ipfs_hash}")
            return ipfs_hash
        else:
            print(f"Error uploading to Pinata: {result.get('error', 'Unknown error')}")
            return None


st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Institute Console</div>
        <h1>Issue and manage verified certificates.</h1>
        <p>Create a certificate, pin it to IPFS, and register the hash on-chain. You can also view an existing certificate by ID.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs(["Generate Certificate", "View Certificates"])

with tabs[0]:
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    if not api_key or not api_secret:
        st.warning("Missing PINATA_API_KEY or PINATA_API_SECRET. Uploads will fail.")
    # Certificate creation workflow.
    form = st.form("Generate-Certificate")
    uid = form.text_input(label="Student UID")
    candidate_name = form.text_input(label="Candidate Name")
    course_name = form.text_input(label="Course Name")
    org_name = form.text_input(label="Organization Name")

    submit = form.form_submit_button("Generate Certificate", use_container_width=True)
    if submit:
        pdf_file_path = "certificate.pdf"
        institute_logo_path = "../assets/logo.jpg"
        generate_certificate(pdf_file_path, uid, candidate_name, course_name, org_name, institute_logo_path)

        # Upload the PDF to Pinata
        ipfs_hash = upload_to_pinata(pdf_file_path, api_key, api_secret)
        os.remove(pdf_file_path)
        data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode("utf-8")
        certificate_id = hashlib.sha256(data_to_hash).hexdigest()

        if not ipfs_hash:
            st.error("IPFS upload failed. Check your Pinata credentials.")
        elif contract is None:
            st.error("Smart contract not configured. Check deployment and connection.")
        else:
            contract.functions.generateCertificate(
                certificate_id,
                uid,
                candidate_name,
                course_name,
                org_name,
                ipfs_hash,
            ).transact({"from": w3.eth.accounts[0]})
            st.success(
                "Certificate generated and recorded on-chain."
            )
            st.markdown(
                f'<div class="status-card">Share link: http://127.0.0.1:8501/verify_certificate?ipfs_hash={ipfs_hash}&cert_id={certificate_id}</div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[1]:
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    # Lookup by certificate ID.
    form = st.form("View-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("View Certificate", use_container_width=True)
    if submit:
        try:
            view_certificate(certificate_id)
        except Exception:
            st.error("Invalid Certificate ID!")
    st.markdown("</div>", unsafe_allow_html=True)
        
