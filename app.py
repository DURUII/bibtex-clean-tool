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
import argparse

if "show_welcome" not in st.session_state:
    st.session_state["show_welcome"] = True

st.sidebar.subheader("BibTeX Tools")
st.sidebar.caption("⚠️ No data stored! Check important info.")
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
    # New checkbox for removing textcolor commands
    remove_review_textcolor = st.sidebar.checkbox("Remove textcolor commands", value=False)

    if st.sidebar.button("**Run BibTeX Cleaner**", type="primary", use_container_width=True):
        st.session_state["show_welcome"] = False  # update here only on button click
        if bib_file and tex_file:
            with tempfile.NamedTemporaryFile(delete=False) as bib_temp, tempfile.NamedTemporaryFile(delete=False) as tex_temp:
                bib_temp.write(bib_file.read())
                tex_temp.write(tex_file.read())
                bib_temp.close()
                tex_temp.close()
                cleaned_bib_path = 'cleaned_' + os.path.basename(bib_temp.name)
                clean_bibtex(bib_temp.name, tex_temp.name, keep_unused, wrap_text, remove_review_textcolor)  # pass new parameter
                with open(cleaned_bib_path, 'r') as f:
                    cleaned_bib = f.read()
                st.text_area("Cleaned BibTeX", cleaned_bib, height=400)
                st.download_button("Download Cleaned BibTeX", cleaned_bib,
                                   file_name=cleaned_bib_path, mime="text/plain")
                # If textcolor commands were removed, load and offer the cleaned .tex file
                if remove_review_textcolor:
                    cleaned_tex_path = 'cleaned_' + os.path.basename(tex_temp.name)
                    with open(cleaned_tex_path, 'r') as f:
                        cleaned_tex = f.read()
                    st.text_area("Cleaned TeX", cleaned_tex, height=400)
                    st.download_button("Download Cleaned TeX", cleaned_tex,
                                       file_name=cleaned_tex_path, mime="text/plain")
                    os.remove(cleaned_tex_path)
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

    if st.sidebar.button("**Run BibTeX Checker**", type="primary", use_container_width=True):
        st.session_state["show_welcome"] = False  # update here on button click
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

my_text = "BibTeX Woes? Say goodbye to the nightmare."
text_length = len(my_text) - 3

if st.session_state["show_welcome"]:
    st.markdown(
        f"""
        <style>
            .center-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 60vh;
                width: 80%;
                margin: 0 auto;
                box-sizing: border-box;
                padding: 20px;
            }}
            #emoji {{
                font-size: 120px;
                margin-bottom: 20px;
                animation: nodding 2s infinite;
            }}
            @keyframes nodding {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(10px); }}
            }}
            /* Typewriter effect first, then wrap */
            #text {{
                font-size: 24px;
                margin-top: -10px;
                overflow: hidden;
                white-space: nowrap; /* phase 1: single line */
                border-right: .15em solid orange;
                width: 0ch;
                animation: typing 3s steps({text_length}, end) forwards,
                           blink-caret 0.75s step-end infinite;
            }}
            @keyframes typing {{
                0%   {{ width: 0ch; }}
                99%  {{ width: {text_length}ch; }}
                100% {{
                    width: auto;
                    white-space: normal; /* phase 2: allow wrapping */
                }}
            }}
            @keyframes blink-caret {{
                0%, 100% {{ border-color: transparent; }}
                50%      {{ border-color: orange; }}
            }}
            @media (max-width: 600px) {{
                #emoji {{ font-size: 80px; }}
                #text  {{ font-size: 18px; }}
            }}
        </style>
        <div class="center-container">
            <div id="emoji">(°□°)</div>
            <div id="text">{my_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )