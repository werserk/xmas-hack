import streamlit as st
import base64
from document_processing import check_file


def displayPDF(file, is_bytes=False):
    file = check_file(file)
    if not is_bytes:
        file = base64.b64encode(file.getvalue()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{file}" width="700" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)
