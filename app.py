import streamlit as st
from checker import update_entry, batch_check
from cleaner import main as clean_bibtex
import tempfile
import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

if "show_welcome" not in st.session_state:
    st.session_state["show_welcome"] = True

st.sidebar.subheader("BibTeX Tools")
st.sidebar.caption("⚠️ Any program can make mistakes. Check important info.")
option = st.sidebar.selectbox("Choose a tool", ("BibTeX Cleaner", "BibTeX Double Checker (Preview)", "Donate"))

if option == "BibTeX Cleaner":
    cols = st.sidebar.columns(2)  # Two columns for file uploads
    with cols[0]:
        bib_file = st.file_uploader("Upload your .bib file", type=["bib"])
    with cols[1]:
        tex_file = st.file_uploader("Upload your .tex file", type=["tex"])
    keep_unused = st.sidebar.checkbox("Keep unused entries", value=True)
    # Added checkbox for wrap_text with default True
    wrap_text = st.sidebar.checkbox("Wrap the first word with \\text", value=True)

    if st.sidebar.button("**Run BibTeX Cleaner**", type="primary", use_container_width=True):
        st.session_state["show_welcome"] = False
        if bib_file and tex_file:
            with tempfile.NamedTemporaryFile(delete=False) as bib_temp, tempfile.NamedTemporaryFile(delete=False) as tex_temp:
                bib_temp.write(bib_file.read())
                tex_temp.write(tex_file.read())
                bib_temp.close()
                tex_temp.close()
                cleaned_bib_path = 'cleaned_' + os.path.basename(bib_temp.name)
                clean_bibtex(bib_temp.name, tex_temp.name, keep_unused, wrap_text)  # pass new parameter
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
    st.session_state["show_welcome"] = False
    bib_file = st.sidebar.file_uploader("Upload your .bib file", type=["bib"])
    num_entries = st.sidebar.number_input("Number of entries to check", min_value=1, max_value=100, value=2)
    remove_unselected = st.sidebar.checkbox("Remove unselected entries", value=False)

    if st.sidebar.button("**Run BibTeX Checker**", type="primary", use_container_width=True):
        if bib_file:
            progress_bar = st.progress(0, text="It takes time. Please wait or try local deployment.")  # created progress bar
            with tempfile.NamedTemporaryFile(delete=False) as bib_temp:
                bib_temp.write(bib_file.read())
                bib_temp.close()
                updated_bib_path = 'updated_' + os.path.basename(bib_temp.name)
                batch_check(bib_temp.name, num_entries, keep_unselected=not remove_unselected,
                            progress_object=progress_bar)  # pass progress object
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
    if st.session_state["show_welcome"]:
        st.session_state["show_welcome"] = False
    st.markdown("## Donate")
    st.markdown(
        """
        🌟 If you find this tool useful, please consider star [the GitHub repo](https://github.com/DURUII/bibtex-clean-tool)!
        
        ⛽️ Scan the QR code below to support via WeChat.
        """
    )
    col1, col2, col3 = st.columns([0.58, 0.02, 0.38])
    with col1:
        st.markdown(
            """
            <style>
                .donate-text {
                    font-family: 'Courier New', monospace;
                    border-left: 4px solid #2ecc71;
                    padding-left: 1rem;
                    line-height: 2.5;
                    margin: 1.5rem 0;
                }
            </style>

            <div class="donate-text">
            Your donation translates to:<br>
            🔧 3.2x faster bug fixes<br>
            📈 42% higher chance of new features<br>
            😴 1 all-nighter prevented<br>
            🥤 a cup of milk tea with 30% sugar.
            <br>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.image("assets/donate.jpg",
                 caption="It sucks, but you'll get through it.")

if st.session_state["show_welcome"]:
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
            font-size: 125px;
            line-height: 1.25;
            margin-bottom: 20px;
        }
        #text {
            font-size: 24px;
            margin-top: -10px;
        }
    </style>
    <div class="center-container">
        <div id="emoji">(°□°)</div>
        <div id="text">BibTeX Woes? Say goodbye to the nightmare.</div>
    </div>
    """,
        unsafe_allow_html=True
    )
