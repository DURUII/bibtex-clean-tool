import streamlit as st
from utils.bib import parse_bib_file
from checker import update_entry, batch_check
from cleaner import main as clean_bibtex
import tempfile
import os

st.title("BibTeX Clean and Checker Tool")

st.sidebar.title("Options")
option = st.sidebar.selectbox("Choose a feature", ("Clean BibTeX", "Check BibTeX"))

if option == "Clean BibTeX":
    st.header("Clean BibTeX Entries")
    bib_file = st.file_uploader("Upload your .bib file", type=["bib"])
    tex_file = st.file_uploader("Upload your .tex file", type=["tex"])
    keep_unused = st.checkbox("Keep unused entries", value=True)

    if st.button("Clean BibTeX"):
        if bib_file and tex_file:
            with tempfile.NamedTemporaryFile(delete=False) as bib_temp, tempfile.NamedTemporaryFile(delete=False) as tex_temp:
                bib_temp.write(bib_file.read())
                tex_temp.write(tex_file.read())
                bib_temp.close()
                tex_temp.close()
                cleaned_bib_path = 'cleaned_' + os.path.basename(bib_temp.name)
                clean_bibtex(bib_temp.name, tex_temp.name, keep_unused)
                with open(cleaned_bib_path, 'r') as f:
                    cleaned_bib = f.read()
                st.text_area("Cleaned BibTeX", cleaned_bib, height=400)
                os.remove(bib_temp.name)
                os.remove(tex_temp.name)
                os.remove(cleaned_bib_path)
        else:
            st.error("Please upload both .bib and .tex files.")

elif option == "Check BibTeX":
    st.header("Check and Update BibTeX Entries")
    bib_file = st.file_uploader("Upload your .bib file", type=["bib"])
    num_entries = st.number_input("Number of entries to check", min_value=1, max_value=100, value=60)

    if st.button("Check BibTeX"):
        if bib_file:
            with tempfile.NamedTemporaryFile(delete=False) as bib_temp:
                bib_temp.write(bib_file.read())
                bib_temp.close()
                updated_bib_path = 'updated_' + os.path.basename(bib_temp.name)
                batch_check(bib_temp.name, num_entries)
                with open(updated_bib_path, 'r') as f:
                    updated_bib = f.read()
                st.text_area("Updated BibTeX", updated_bib, height=400)
                os.remove(bib_temp.name)
                os.remove(updated_bib_path)
        else:
            st.error("Please upload a .bib file.")
