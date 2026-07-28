import streamlit as st

from utils.folder_picker import select_folder
from utils.scanner import scan_folder
from utils.comparer import get_new_files
from utils.report import (
    create_dataframe,
    save_excel,
    save_csv
)

st.set_page_config(
    page_title="Folder Difference Finder",
    layout="wide"
)

st.title("📁 Folder Difference Finder")

# -----------------------
# Session State
# -----------------------

if "old_folder" not in st.session_state:
    st.session_state.old_folder = ""

if "new_folder" not in st.session_state:
    st.session_state.new_folder = ""

# -----------------------
# OLD
# -----------------------

col1, col2 = st.columns([5,1])

with col1:
    st.text_input(
        "Old Folder",
        value=st.session_state.old_folder,
        disabled=True
    )

with col2:

    if st.button("Browse Old"):

        folder = select_folder("Select OLD Folder")

        if folder:
            st.session_state.old_folder = folder
            st.rerun()

# -----------------------
# NEW
# -----------------------

col1, col2 = st.columns([5,1])

with col1:

    st.text_input(
        "New Folder",
        value=st.session_state.new_folder,
        disabled=True
    )

with col2:

    if st.button("Browse New"):

        folder = select_folder("Select NEW Folder")

        if folder:
            st.session_state.new_folder = folder
            st.rerun()

# -----------------------
# Compare
# -----------------------

if st.button("Compare Folders", use_container_width=True):

    if not st.session_state.old_folder:

        st.error("Select OLD folder.")

    elif not st.session_state.new_folder:

        st.error("Select NEW folder.")

    else:

        with st.spinner("Scanning folders..."):

            old_files = scan_folder(
                st.session_state.old_folder
            )

            new_files = scan_folder(
                st.session_state.new_folder
            )

            new_added = get_new_files(
                old_files,
                new_files
            )

            df = create_dataframe(new_added)

        st.success(f"Found {len(df)} new files.")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Old Files",
            len(old_files)
        )

        c2.metric(
            "New Files",
            len(new_files)
        )

        c3.metric(
            "Added Files",
            len(new_added)
        )

        st.dataframe(
            df,
            use_container_width=True,
            height=500
        )

        excel = save_excel(df)
        csv = save_csv(df)

        c1, c2 = st.columns(2)

        with c1:

            with open(excel, "rb") as f:

                st.download_button(
                    "Download Excel",
                    f,
                    "NewFiles.xlsx"
                )

        with c2:

            with open(csv, "rb") as f:

                st.download_button(
                    "Download CSV",
                    f,
                    "NewFiles.csv"
                )