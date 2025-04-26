# Dental-Health-Assistant
This project is an intelligent Dental Health Assistant powered by Retrieval-Augmented Generation (RAG). It leverages a combination of natural language processing and a domain-specific knowledge base to provide accurate, context-aware answers to user queries about dental health.
The system consists of:

main.py – Handles backend logic for document retrieval, embedding, and generation, integrating with an LLM to produce relevant responses.

streamlit.py – Provides an intuitive, interactive web interface built with Streamlit, allowing users to ask dental health questions and receive informative responses in real time.

🔍 Key Features
RAG-powered architecture for more factual and grounded answers

User-friendly web interface for seamless interaction

Designed for accessibility and educational purposes in dental health

🚀 How to Run the Dental Health Assistant Locally
1. Clone the repository
git clone https://github.com/shafimahadi/Dental-Health-Assistant.git
cd your-repo-name
3. Set up a Python environment
It's recommended to use a virtual environment:

python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate

3. Install dependencies
Make sure you have installed requirements.txt.

pip install -r requirements.txt

4. Run Ollama in background.


5. Run the Streamlit app
streamlit run streamlit.py
This will open the web app in your browser at http://localhost:8501.

⚡ Quick Summary
main.py = Backend logic (RAG system, retrieval, LLM)

streamlit.py = Frontend UI (user input, output display)

