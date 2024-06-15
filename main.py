import openai
import streamlit as st
import os

# Load API keys from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]
assistant_id = st.secrets["openai"]["assistant_id"]
vector_store_id = st.secrets["openai"]["vector_store_id"]

if not openai.api_key:
    st.error("API key is not set. Please set the API key in Streamlit secrets.")
    st.stop()

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

st.set_page_config(page_title="CatGPT", page_icon=":speech_balloon:")

if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True

st.title("Interview Assistant")
st.write("Semiconductor Equipment And process technology Interviewer")

if st.button("Exit Chat"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.start_chat = False  # Reset the chat state

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "text-davinci-003"  # Use a valid model name
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Let's start an interview!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = openai.Completion.create(
                model=st.session_state.openai_model,
                prompt=prompt,
                max_tokens=150
            )
            reply = response.choices[0].text.strip()
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)
        except Exception as e:
            st.error(f"Error communicating with OpenAI: {str(e)}")
else:
    st.write("Click 'Start Chat' to begin.")
