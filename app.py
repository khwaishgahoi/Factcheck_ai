import streamlit as st
import pandas as pd

from utils.pdf_extractor import extract_text_from_pdf
from utils.docx_extractor import extract_text_from_docx
from utils.claim_extractor import extract_claims
from utils.verifier import verify_claim

st.set_page_config(page_title="Fact Check AI")

st.title("📄 AI Fact Checker")

uploaded_file = st.file_uploader(
    "Upload a PDF or Word Document",
    type=["pdf", "docx"]
)

if uploaded_file:

    st.success("File uploaded successfully!")

    # Extract text based on file type
    if uploaded_file.name.endswith(".pdf"):

        extracted_text = extract_text_from_pdf(uploaded_file)

    elif uploaded_file.name.endswith(".docx"):

        extracted_text = extract_text_from_docx(uploaded_file)

    else:

        st.error("Unsupported file type")
        st.stop()

    # Show extracted text
    st.subheader("Extracted Text")

    st.text_area(
        "Document Content",
        extracted_text,
        height=250
    )

    # Extract claims
    st.subheader("Extracted Claims")

    with st.spinner("Extracting factual claims..."):

        claims = extract_claims(extracted_text)

    for idx, claim in enumerate(claims, start=1):
        st.write(f"{idx}. {claim}")

    # Verify claims
    st.subheader("Fact Check Results")

    results = []

    for claim in claims:

        with st.spinner(f"Verifying: {claim}"):

            result = verify_claim(claim)

            results.append({
                "Claim": claim,
                "Verdict": result["verdict"],
                "Correct Info": result["correct_info"]
            })

    # Create table
    df = pd.DataFrame(results)

    # Display results
    st.table(df)