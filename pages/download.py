import streamlit as st

st.title(
    "Download the result here"
)

with open(f"resutl.csv", "rb") as file:
    btn = st.download_button(
        label=f"Download result",
        data=file,
        file_name=f"result.csv",
    )