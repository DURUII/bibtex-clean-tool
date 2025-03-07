import streamlit as st
from utils.bib import parse_bib_file
from checker import update_entry, batch_check
from cleaner import main as clean_bibtex
import tempfile
import os

st.sidebar.title("BibTeX Tool")
# Option selection
option = st.sidebar.selectbox("Choose a feature", ("Clean BibTeX", "Check BibTeX"))

# Add description caption in the main content area
st.markdown(
    """
    <div style="font-size: 14px; line-height: 1.5;">
      <p>
        <strong>1. BibTeX Cleaner & Formatter (<code>cleaner.py</code>)</strong> - Reorders <code>.bib</code> entries based on citation order in the <code>.tex</code> file, removes duplicates, and appends unused references at the end. This is adapted from the repo <a href="https://github.com/SFRL/clean_bibtex" target="_blank">SFRL/clean_bibtex</a>.
      </p>
      <p>
        <strong>2. Double-Checker (<code>checker.py</code>)</strong> - Searches IEEE Xplore for accurate BibTeX citations and updates <code>.bib</code> entries while preserving the original keys. This is necessary because sources like Google Scholar often have incorrect years, incomplete metadata, or lack authoritative information.
      </p>
    </div>
    """, unsafe_allow_html=True
)

if option == "Clean BibTeX":
    st.sidebar.subheader("Clean BibTeX Options")
    cols = st.sidebar.columns(2)  # Two columns for file uploads
    with cols[0]:
        bib_file = st.file_uploader("Upload your .bib file", type=["bib"])
    with cols[1]:
        tex_file = st.file_uploader("Upload your .tex file", type=["tex"])
    keep_unused = st.sidebar.checkbox("Keep unused entries", value=True)

    if st.sidebar.button("Run Clean BibTeX"):
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
                st.download_button("Download Cleaned BibTeX", cleaned_bib,
                                   file_name=cleaned_bib_path, mime="text/plain")
                os.remove(bib_temp.name)
                os.remove(tex_temp.name)
                os.remove(cleaned_bib_path)
        else:
            st.error("Please upload both .bib and .tex files.")

elif option == "Check BibTeX":
    # st.sidebar.subheader("Check BibTeX Options")
    bib_file = st.sidebar.file_uploader("Upload your .bib file", type=["bib"])
    num_entries = st.sidebar.number_input("Number of entries to check", min_value=1, max_value=100, value=60)
    remove_unselected = st.sidebar.checkbox("Remove unselected entries", value=False)

    if st.sidebar.button("Run Check BibTeX"):
        if bib_file:
            with tempfile.NamedTemporaryFile(delete=False) as bib_temp:
                bib_temp.write(bib_file.read())
                bib_temp.close()
                updated_bib_path = 'updated_' + os.path.basename(bib_temp.name)
                batch_check(bib_temp.name, num_entries, keep_unselected=not remove_unselected)
                with open(updated_bib_path, 'r') as f:
                    updated_bib = f.read()
                st.text_area("Updated BibTeX", updated_bib, height=400)
                st.download_button("Download Updated BibTeX", updated_bib,
                                   file_name=updated_bib_path, mime="text/plain")
                os.remove(bib_temp.name)
                os.remove(updated_bib_path)
        else:
            st.error("Please upload a .bib file.")
