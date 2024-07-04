import streamlit as st
import os
from main import response_generator
from PIL import Image


im = Image.open("logo.png")
st.set_page_config(
    page_title="Oracle Wiki",
    page_icon=im
)
st.title("Oracle Wiki")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = response_generator(prompt,'')
        response = st.write(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})