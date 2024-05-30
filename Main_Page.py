import streamlit as st

st.set_page_config(
    page_title="Fire Emblem Dashboard",
    page_icon="🗡️"
)

st.sidebar.success("Select a Page above!")
with open("README.md") as f:
    main_blurb = f.read()

st.markdown(main_blurb)
