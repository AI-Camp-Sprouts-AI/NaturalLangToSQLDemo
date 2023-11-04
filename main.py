from llm import NLP2SQL, initialize_model
from dotenv import load_dotenv
from os import getenv
from langchain.chat_models import ChatOpenAI
import streamlit as st

# streamlit run main.py

def main():
    st.title("Text To Query")

    with st.sidebar:
        default_schema = """TABLE DomainRecords (
    DomainID INT PRIMARY KEY,
    WebsiteID INT,
    DomainName VARCHAR(255),
    Registrar VARCHAR(255),
    PurchaseDate DATE,
    ExpiryDate DATE,
    AutoRenew BOOLEAN,
);"""
        schema_box = st.text_area("Database Schema", height=300, value=default_schema)
        default_info = "None of the values should be NULL."
        box2 = st.text_area("Other Info", height=300, value=default_info)

    if "model" not in st.session_state:
        load_dotenv()
        api_key = getenv('OPENAI_API_KEY')
        st.session_state.llm = ChatOpenAI(model="gpt-4", openai_api_key=api_key, temperature=0)
        st.session_state.model = initialize_model(llm=st.session_state.llm, options={'memory': 3, 'review': True})

    if "processing" not in st.session_state:
        st.session_state.processing = False

    if "messages" not in st.session_state:
        st.session_state.messages = []

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
                    st.session_state.model.load_schema_as_string(f"{schema_box}\n{box2}")
                    response = st.session_state.model.predict(prompt).message.replace('\n', '  \n')
                    st.markdown(response)
                    st.session_state.messages.append({"role": "ai", "content": response})
                    st.session_state.processing = False


if __name__ == '__main__':
    main()
