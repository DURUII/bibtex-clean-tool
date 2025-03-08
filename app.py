import streamlit as st
from utils.bib import parse_bib_file
from checker import update_entry, batch_check
from cleaner import main as clean_bibtex
import tempfile
import os

import streamlit as st

st.sidebar.subheader("BibTeX Tools")
option = st.sidebar.selectbox("Choose a tool", ("BibTex Cleaner", "BibTeX Double Checker (Preview)", "Donate"), index=None,
                              placeholder="I am here.")

if option == "BibTex Cleaner":
    # st.sidebar.subheader("BibTex Cleaner Options")
    cols = st.sidebar.columns(2)  # Two columns for file uploads
    with cols[0]:
        bib_file = st.file_uploader("Upload your .bib file", type=["bib"])
    with cols[1]:
        tex_file = st.file_uploader("Upload your .tex file", type=["tex"])
    keep_unused = st.sidebar.checkbox("Keep unused entries", value=True)

    if st.sidebar.button("**Run BibTeX Cleaner**", type="primary", use_container_width=True):
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
            st.balloons()  # Raise balloons after cleaner operation completes
        else:
            st.error("Please upload both .bib and .tex files.")

elif option == "BibTeX Double Checker (Preview)":
    bib_file = st.sidebar.file_uploader("Upload your .bib file", type=["bib"])
    num_entries = st.sidebar.number_input("Number of entries to check", min_value=1, max_value=100, value=2)
    remove_unselected = st.sidebar.checkbox("Remove unselected entries", value=False)

    if st.sidebar.button("**Run Check BibTeX**", type="primary", use_container_width=True):
        if bib_file:
            progress_bar = st.progress(0, text="Operation in progress. Please wait.")  # created progress bar
            with tempfile.NamedTemporaryFile(delete=False) as bib_temp:
                bib_temp.write(bib_file.read())
                bib_temp.close()
                updated_bib_path = 'updated_' + os.path.basename(bib_temp.name)
                batch_check(bib_temp.name, num_entries, keep_unselected=not remove_unselected, progress_object=progress_bar)  # pass progress object
                with open(updated_bib_path, 'r') as f:
                    updated_bib = f.read()
                st.text_area("Updated BibTeX", updated_bib, height=400)
                st.download_button("Download Updated BibTeX", updated_bib,
                                   file_name=updated_bib_path, mime="text/plain")
                os.remove(bib_temp.name)
                os.remove(updated_bib_path)
            st.balloons()  # Raise balloons after checker operation completes
        else:
            st.error("Please upload a .bib file.")
elif option == "Donate":
    pass
else:
    st.markdown(
        """
    <style>
        .center-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            width: 100%;
        }
        #emoji {
            font-size: 200px;
            line-height: 1.25;
            margin-bottom: 20px;
        }
        #text {
            font-size: 24px;
            font-weight: bold;
            margin-top: -10px;
        }
    </style>
    <div class="center-container">
        <div id="emoji">(╯°□°)╯</div>
        <div id="text">BibTeX Woes? Say goodbye to the nightmare.</div>
    </div>
    """,
        unsafe_allow_html=True
    )
