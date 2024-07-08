import streamlit as st
import os
from main import response_generator,query_csv_db
from PIL import Image
import pandas as pd

im = Image.open("logo.png")
st.set_page_config(
    page_title="Oracle Wiki",
    page_icon=im,
    layout='centered'
)
st.title("Oracle Wiki")
options =st.selectbox('Choose One',options=['Query an SQL DB','OIC Chatbot','SOA Chatbot','OSB Chatbot','Query a CSV DB'],index = 1)

if options in ['OIC Chatbot','SOA Chatbot','OSB Chatbot']:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"],avatar=im):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user",avatar=im):
            st.markdown(prompt)

        with st.chat_message("assistant",avatar=im):
            response,output_docs = response_generator(prompt,'')
            st.markdown(response)


        st.session_state.messages.append({"role": "assistant", "content": response})
elif options=='Query a CSV DB':
    csv_files = st.file_uploader('Enter csv files to Query',accept_multiple_files=True)
    if csv_files:
        query =  st.text_input('**:red[Enter the Query]**')
        if st.button(':red[Submit]'):
            result = query_csv_db(csv_files,query)['output']
            st.write(result)


else:
    st.selectbox('Choose the database you want to Query',options=['HCM OFS','SCM OFS'])