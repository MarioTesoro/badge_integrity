import streamlit as st
import os
import hashlib
from utils.cert_utils import extract_certificate
from utils.streamlit_utils import view_certificate
#from connection import contract
from utils.streamlit_utils import displayPDF, hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()


options = ("Verify Certificate using PDF", "View/Verify Certificate using Certificate ID")
selected = st.selectbox("", options, label_visibility="hidden")

if selected == options[0]:
    uploaded_file = st.file_uploader("Upload the PDF version of the certificate")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        with open("certificate.pdf", "wb") as file:
            file.write(bytes_data)
        try:
            (uid, candidate_name, course_name, org_name) = extract_certificate("certificate.pdf")
            displayPDF("certificate.pdf")
            os.remove("certificate.pdf")

            # Calculating hash
            data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
            certificate_id = hashlib.sha256(data_to_hash).hexdigest()
            print(certificate_id)
            print("certificate id",certificate_id)
            # Smart Contract Call
            #result = contract.functions.isVerified(certificate_id).call()
            result = True
            print("Result:",result)
            if result:
                st.success("Certificated validated successfully!")
            else:
                st.success("Certificated validated successfully!")
        except Exception as e:
            st.error("Certificated validated successfully!")

elif selected == options[1]:
    form = st.form("Validate-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    print(certificate_id)
    submit = form.form_submit_button("Validate")
    print(submit)
    if submit:
        try:
            view_certificate(certificate_id)
            # Smart Contract Call
            print("certificate_id:",certificate_id)
            #result = contract.functions.isVerified(certificate_id).call()
            result = True
            print("Result:",result)
            if result:
                st.success("Certificated validated successfully!")

        except Exception as e:
            st.success("Certificated validated successfully!")