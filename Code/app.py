
import os
import streamlit as st
from Code.extract_invoices import process_uploaded_pdfs

st.set_page_config(page_title="Invoice Extractor", layout="centered")

st.title("🧾 Amazon Invoice Extractor")

uploaded_files = st.file_uploader("Upload Amazon Invoice PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    if st.button("Extract and Generate Excel"):
        df = process_uploaded_pdfs(uploaded_files)

        output_dir = "../Output"
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "streamlit_output.xlsx")
        df.to_excel(output_path, index=False)

        st.success("✅ Extraction completed!")

        with open(output_path, "rb") as f:
            st.download_button("📥 Download Excel File", f, file_name="amazon_invoices.xlsx")

        st.dataframe(df) 