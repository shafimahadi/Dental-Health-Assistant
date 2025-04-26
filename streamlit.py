import streamlit as st
import main as main
import os
import logging

# It configures the logging settings for the application.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# It sets the title of the Streamlit application.
st.title("Dental Health Assistant")

# It initializes the session state for managing messages and the greeting status.
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    st.session_state["greeted"] = False
# It initializes the session state for the vector database, loading it if it exists.
if "db" not in st.session_state:
    st.session_state.db = main.load_vector_store()

# It greets the user upon the first interaction.
if not st.session_state["greeted"]:
    st.session_state["messages"].append({"role": "assistant", "content": "Hello! I'm your dental health assistant. How can I help you today?"})
    st.session_state["greeted"] = True

# It sets the uploaded files to None, effectively disabling the file uploader functionality in this version.
uploaded_files = None

# It provides the chat interface if the vector database is loaded successfully.
if "db" in st.session_state and st.session_state.db is not None:
    question = st.chat_input("Ask me anything about dental health!")
    if question:
        st.session_state["messages"].append({"role": "user", "content": question})
        st.chat_message("user").write(question)

        # It displays a spinner while searching for relevant information in the database.
        with st.spinner("Searching for relevant information..."):
            related_docs = main.retrieve_docs(st.session_state.db, question)

        # It displays a spinner while generating the answer based on the retrieved information.
        with st.spinner("Generating answer..."):
            answer = main.question_pdf(question, related_docs)
        st.session_state["messages"].append({"role": "assistant", "content": answer["output_text"]})
        st.chat_message("assistant").write(answer["output_text"])

# It displays the chat history to the user.
st.subheader("Chat History:")
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# It provides an informational message if the vector database has not been loaded.
else:
    st.info("Ask me any Dental Health related questions...")