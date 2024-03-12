import io
import os
import subprocess
import streamlit as st
from PIL import Image
from openai import OpenAI

import api_handler
from api_handler import send_query_get_response
from chat_gen import generate_html
from file_upload import upload_files_to_assistant, attach_files_to_assistant, check_and_upload_files


c1, c2 = st.columns([0.9, 3.2])

with c1:
    st.caption('')
    st.caption('')
    # st.image(logo,width=120)

with c2:

    st.title('AI Tutor Prototype')


# api_key = st.text_input(label='Enter your OpenAI API Key', type='password')
    
api_key = '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'

if api_key:
    # If API key is entered, initialize the OpenAI client and proceed with app functionality
    client = OpenAI(api_key=api_key)
    assistant_id = 'asst_6gOb3dy0j8LiwZZww5YTuY0P'

    # File Handling Section
    files_info = check_and_upload_files(client, assistant_id)
    
    st.markdown(f'Number of files uploaded in the assistant: :blue[{len(files_info)}]')
    st.divider()

    st.sidebar.header('AI-Tutor')
    # st.sidebar.image(logo,width=120)
    # st.sidebar.caption('Made by D')
    # Adding a button in the sidebar to delete all files from the assistant
    if st.sidebar.button('Delete All Files from Assistant'):
        # Retrieve all file IDs associated with the assistant
        assistant_files_response = client.beta.assistants.files.list(assistant_id=assistant_id)
        assistant_files = assistant_files_response.data

        # Delete each file
        for file in assistant_files:
            file_id = file.id
            client.beta.assistants.files.delete(assistant_id=assistant_id, file_id=file_id)
            st.sidebar.success(f'Deleted file: {file_id}')

    if st.sidebar.button('Generate Chat History'):
    html_data = generate_html(st.session_state.messages, in_lecture_mode=True)  # 传递 in_lecture_mode 参数
    st.sidebar.download_button(label="Download Chat History as HTML",
                                data=html_data,
                                file_name="chat_history.html",
                                mime="text/html")


    # Main Chat Interface
    st.subheader('Q&A record with AI-Tutor 📜')
    # st.caption('You can choose to download the chat history in either PDF or HTML format using the options in the sidebar on the left.')
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    if prompt := st.chat_input("Welcome and ask a question to the AI tutor"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar='👨🏻‍🏫'):
            message_placeholder = st.empty()
            with st.spinner('Thinking...'):
                response = send_query_get_response(client,prompt,assistant_id)
            message_placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# else:
#     # Prompt for API key if not entered
#     st.warning("Please enter your OpenAI API Key to use EduMentor.")
