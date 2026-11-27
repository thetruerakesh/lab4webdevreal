import os
import streamlit as st
from pydantic_ai import Agent

st.title("ProstheticMatch AI Assistant")
st.write("Ask general questions about prosthetic technologies, functionality, and treatment concepts.")

if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

instructions = (
    "You are a helpful biomedical engineering assistant for ProstheticMatch. "
    "Explain general concepts about prosthetic devices, including mechanical, body-powered, "
    "myoelectric, and microprocessor-controlled prosthetics, as well as general differences in "
    "functionality, intended use, amputation levels, and typical cost ranges. "
    "Keep your answers clear, friendly, and concise. "
    "Do not give medical advice or diagnose patients. "
    "You do not have access to any live database, API, or external dataset. "
    "If the user asks you to look up specific FDA records, product codes, or GUDID device listings, "
    "politely explain that you cannot look up live data and suggest they use the Data Page."
)

agent = Agent("google:gemini-3.8-flash", instructions=instructions)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pydantic_history" not in st.session_state:
    st.session_state.pydantic_history = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask a question about prosthetics...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        result = agent.run_sync(prompt, message_history=st.session_state.pydantic_history)
        reply = result.output
        st.session_state.pydantic_history = result.all_messages()
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
    except Exception as e:
        st.error(e)
        error_text = "Sorry, something went wrong while generating a response. Please try again."
        st.session_state.messages.append({"role": "assistant", "content": error_text})
        with st.chat_message("assistant"):
            st.write(error_text)