import openai
import streamlit as st
import time

# Load API keys from Streamlit secrets
client = openai

openai.api_key = st.secrets["openai"]["api_key"]
assistant_id = st.secrets["openai"]["assistant_id"]
vector_store_id = st.secrets["openai"]["vector_store_id"]

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.set_page_config(page_title="InterviewGPT", page_icon=":speech_balloon:")

openai.api_key = "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"

if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

st.title("Interview Assistant")
st.write("Semiconductor Equipment And process technology Interviewer")

if st.button("Exit Chat"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.start_chat = False  # Reset the chat state
    st.session_state.thread_id = None

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4-1106-preview"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Let's start an interview!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )
        
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id
        )

        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages 
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)

else:
    st.write("Click 'Start Chat' to begin.")
