import streamlit as st
import base64
import requests
import os
import certifi
from connection import contract


def apply_base_styles():
    # Single place to tune the app look and avoid scattered CSS hacks.
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Work+Sans:wght@300;400;500;600&display=swap');

        :root {
            --bg: #f6f4ef;
            --bg-accent: #e8f1ee;
            --ink: #1b1f24;
            --muted: #5b6772;
            --card: #ffffff;
            --accent: #0f766e;
            --accent-2: #e76f51;
            --border: #e3e7eb;
            --shadow: 0 14px 40px rgba(20, 32, 44, 0.12);
        }

        html, body, [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at 10% 20%, #ffffff 0%, var(--bg) 45%, var(--bg-accent) 100%);
            color: var(--ink);
            font-family: "Work Sans", sans-serif;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stSidebarNav"] {
            visibility: hidden;
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        [data-testid="stAppViewContainer"] > .main {
            padding-top: 2.5rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3, h4, h5 {
            font-family: "Space Grotesk", sans-serif;
            letter-spacing: -0.02em;
        }

        .eyebrow {
            text-transform: uppercase;
            letter-spacing: 0.2em;
            font-size: 0.7rem;
            color: var(--accent);
            font-weight: 600;
        }

        .hero {
            margin-bottom: 2rem;
        }

        .hero p {
            max-width: 720px;
            color: var(--muted);
            font-size: 1.05rem;
        }

        .app-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
        }

        .card-muted {
            color: var(--muted);
            font-size: 0.95rem;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            background: rgba(15, 118, 110, 0.12);
            color: var(--accent);
            font-size: 0.75rem;
            font-weight: 600;
        }

        .accent {
            color: var(--accent);
        }

        .accent-alt {
            color: var(--accent-2);
        }

        div.stButton > button {
            background: var(--accent);
            border: none;
            color: #ffffff;
            font-weight: 600;
            padding: 0.6rem 1.2rem;
            border-radius: 999px;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            box-shadow: 0 8px 18px rgba(15, 118, 110, 0.25);
        }

        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 12px 24px rgba(15, 118, 110, 0.3);
        }

        div.stButton > button:active {
            transform: translateY(0);
        }

        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div {
            border-radius: 14px;
            border-color: var(--border);
            background: #fbfbfc;
        }

        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea {
            font-family: "Work Sans", sans-serif;
        }

        .field-hint {
            color: var(--muted);
            font-size: 0.85rem;
            margin-top: -0.5rem;
        }

        .status-card {
            border-left: 4px solid var(--accent);
            padding: 0.8rem 1rem;
            background: rgba(15, 118, 110, 0.08);
            border-radius: 12px;
            font-size: 0.95rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


def get_certificate_ipfs_hash(certificate_id):
    if contract is None:
        raise RuntimeError("Smart contract not configured. Check deployment_config.json and build artifacts.")
    # Smart Contract Call
    result = contract.functions.getCertificate(certificate_id).call()
    return result[4]


def view_certificate(certificate_id):
    ipfs_hash = get_certificate_ipfs_hash(certificate_id)
    pinata_gateway_base_url = 'https://gateway.pinata.cloud/ipfs'
    content_url = f"{pinata_gateway_base_url}/{ipfs_hash}"
    # Allow disabling TLS verification for corporate/self-signed environments.
    verify_tls = os.getenv("PINATA_SSL_VERIFY", "true").lower() != "false"
    response = requests.get(content_url, verify=certifi.where() if verify_tls else False)
    with open("temp.pdf", 'wb') as pdf_file:
        pdf_file.write(response.content)
    displayPDF("temp.pdf")
    os.remove("temp.pdf")


def hide_icons():
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>"""
    st.markdown(hide_st_style, unsafe_allow_html=True)


def hide_sidebar():
    no_sidebar_style = """
                <style>
                div[data-testid="stSidebarNav"] {visibility: hidden;}
                </style>"""
    st.markdown(no_sidebar_style, unsafe_allow_html=True)


def remove_whitespaces():
    st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>""", unsafe_allow_html=True)
