import streamlit as st
import streamlit.components.v1 as components
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
from dotenv import load_dotenv
import os
#from connection import contract
from streamlit_extras.switch_page_button import switch_page

# Your other imports...

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

load_dotenv()

# Get URL query parameters
query_params = st.experimental_get_query_params()
print(query_params)
# Extract 'cert_id' parameter (hex string)
cert_id = query_params.get('cert_id', [None])[0]
ipfs_hash = query_params.get('ipfs_hash', [None])[0]

def render_page(cert_id,ipfs_hash):
    if cert_id and ipfs_hash:
        # Construct the URL to the certificate IPFS link
        redirect_url = f"https://plum-geographical-alpaca-624.mypinata.cloud/ipfs/{ipfs_hash}"

        st.title("View you certificate and validate it.")
        st.write(f"Verifying certificate with ID: {cert_id}")

        # Styled link as a button
        st.markdown(f'''
            <a href="{redirect_url}" style="
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                color: #fff;
                background-color: #4CAF50;
                border-radius: 4px;
                text-decoration: none;
                font-weight: bold;
                margin-top: 20px;
            ">View Certificate</a>
        ''', unsafe_allow_html=True)
        if st.button("Verify Certificate"):
            print(ipfs_hash)
            #result = contract.functions.isVerified(ipfs_hash).call()
            result = True
            if result:
                st.Write("Certificate Successfully validated!")
                print(result)
    else:
        st.write("No certificate ID provided.")

# Render the page
render_page(cert_id,ipfs_hash)

# Link back to home (or another page)
st.markdown(
    "[Go to home](?page=home)",
    unsafe_allow_html=True
)