from llm import NLP2SQL, initialize_model
from dotenv import load_dotenv
from os import getenv
from langchain.chat_models import ChatOpenAI
import streamlit as st

load_dotenv()
api_key = getenv('OPENAI_API_KEY')
llm = ChatOpenAI(model="gpt-4", openai_api_key=api_key, temperature=0)

with open('dashboard.md', 'r') as file:
    dashboard_md = file.read()

with open('main_docs.md', 'r') as file:
    main_docs = file.read()
with open('connector_docs.md', 'r') as file:
    connector_docs = file.read()
documentation_md = main_docs + '\n\n' + connector_docs

def display_chatbot(schema_box, info_box):
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if not st.session_state.processing:
        if prompt := st.chat_input("Enter a question"):
            st.session_state.processing = True

            if prompt == "reset":
                st.session_state.clear_chat_history()
                st.session_state.processing = False
            else:
                with st.chat_message("user"):
                    st.markdown(prompt)
                    st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("ai"):
                    st.session_state['model'].load_schema_as_string(f"{schema_box}\n{info_box}")
                    response = st.session_state['model'].predict(prompt).message.replace('\n', '  \n')
                    st.markdown(response)
                    st.session_state.messages.append({"role": "ai", "content": response})
                    st.session_state.processing = False

def main():
    
    if 'model' not in st.session_state:
        st.session_state['model'] = initialize_model(llm=llm, options={'memory': 3})

    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'Dashboard'

    # Sidebar buttons for navigation
    with st.sidebar:
        if st.button('Dashboard'):
            st.session_state['current_page'] = 'Dashboard'
        if st.button('Chatbot'):
            st.session_state['current_page'] = 'Chatbot'
        if st.button('Documentation'):
            st.session_state['current_page'] = 'Documentation'

        # Chatbot schema and other info text areas in the sidebar
        if st.session_state['current_page'] == 'Chatbot':
            schema_box = st.text_area("Database Schema", height=300, value=default_schema)
            info_box = st.text_area("Other Info", height=150, value=default_info)

    # Main content area
    if st.session_state['current_page'] == 'Dashboard':
        st.markdown(dashboard_md)

    elif st.session_state['current_page'] == 'Chatbot':
        st.title("Chatbot")
        display_chatbot(schema_box, info_box)

    elif st.session_state['current_page'] == 'Documentation':
        st.markdown(documentation_md)

    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "messages" not in st.session_state:
        st.session_state.messages = []

# Default values for text areas
default_schema = """TABLE DomainRecords (
    DomainID INT PRIMARY KEY,
    WebsiteID INT,
    DomainName VARCHAR(255),
    Registrar VARCHAR(255),
    PurchaseDate DATE,
    ExpiryDate DATE,
    AutoRenew BOOLEAN,
);"""
default_info = "None of the values should be NULL."

if __name__ == '__main__':
    main()