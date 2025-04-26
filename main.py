from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import streamlit as st
import os
import re

# Directory for uploaded PDFs
pdfs_directory = '/Users/apple/downloads/'
FAISS_INDEX_PATH = "faiss_dental_ollama_index"  # Path to store/load FAISS index

# Embeddings and model
embeddings = OllamaEmbeddings(model="deepseek-r1:8b")
model = OllamaLLM(model="deepseek-r1:8b")  # Options: deepseek-v2:16b, deepseek-r1:8b, deepseek-r1:1.5b

# Prompt template for answering questions
template = """
You are a helpful dental health assistant. Using the following retrieved information from a dental document, answer the user's questions about dental health. If you don't know the answer based on the provided information, say that you don't know. Provide concise and informative answers, using up to three sentences.
Question: {question}
Context: {context}
Answer:
"""

# Function to remove <think>...</think> from displayed output
def remove_think_tags(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# Handle PDF upload
def upload_pdf(file):
    file_path = os.path.join(pdfs_directory, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return file_path

# Create FAISS vector store from PDF
def create_vector_store(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300)
    chunked_docs = text_splitter.split_documents(documents)
    db = FAISS.from_documents(chunked_docs, embeddings)
    db.save_local(FAISS_INDEX_PATH)
    return db

# Load existing FAISS vector store
def load_vector_store():
    try:
        db = FAISS.load_local(
            FAISS_INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        return db
    except Exception as e:
        print(f"Could not load existing FAISS index: {e}")
        return None

# Retrieve relevant documents
def retrieve_docs(db, query, k=4):
    if db:
        return db.similarity_search(query, k)
    else:
        return []

# Process question and return a cleaned output (without <think>)
def question_pdf(question, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    result = chain.invoke({"question": question, "context": context})

    # Clean only the final result shown to the user
    cleaned_result = remove_think_tags(result)

    return {"output_text": cleaned_result}

# Main backend indicator
if __name__ == "__main__":
    print("This is the main module for backend functionalities.")
    print("Run 'streamlit run streamlit.py' to start the application.")
