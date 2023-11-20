import streamlit as st
from langchain.chat_models import ChatOpenAI
from llm import initialize_model


api_key = st.secrets['OPENAI_API_KEY']
llm = ChatOpenAI(model="gpt-3.5-turbo-16k",
                 openai_api_key=api_key, temperature=0)

# with open('dashboard.md', 'r') as file:
#     dashboard_md = file.read()

# with open('main_docs.md', 'r') as file:
#     main_docs = file.read()

# with open('connector_docs.md', 'r') as file:
#     connector_docs = file.read()

# documentation_md = main_docs + '\n\n' + connector_docs


def display_chatbot(schema, guidelines):
    st.header('Text to SQL AI')
    st.markdown("""##### For example:""")
    st.write("List the top 5 industries with the count of maximum estimated employee within a rolling window of 14 days.")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if not st.session_state.processing:
        if prompt := st.chat_input("Enter your input here..."):
            st.session_state.processing = True

            if prompt == "reset":
                st.session_state.clear_chat_history()
                st.session_state.processing = False
            else:
                with st.chat_message("user"):
                    st.markdown(prompt)
                    st.session_state.messages.append(
                        {"role": "user", "content": prompt})
                with st.chat_message("ai"):
                    st.session_state['model'].load_schema_as_string(
                        f"{schema}\n{guidelines}")
                    response = st.session_state['model'].predict(
                        prompt).message.replace('\n', '  \n')
                    st.markdown(response)
                    st.session_state.messages.append(
                        {"role": "ai", "content": response})
                    st.session_state.processing = False


def main():

    if 'model' not in st.session_state:
        st.session_state['model'] = initialize_model(
            llm=llm, options={'memory': 3})

    with st.sidebar:
        schema = st.text_area(
            "Database Schema", height=300, value=client_schema)
        guidelines = st.text_area(
            "Guidelines", height=150, value=client_guidelines)

    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "messages" not in st.session_state:
        st.session_state.messages = []
    display_chatbot(schema, guidelines)
    # Main content area


# Default values for text areas
client_schema = """CREATE TABLE website_aggregates (
    id SERIAL PRIMARY KEY,
    dt DATE,
    customer_domain VARCHAR(255),
    lead_domain VARCHAR(255),
    ip_country VARCHAR(255),
    no_of_visiting_ips BIGINT,
    no_of_hits BIGINT,
    lead_domain_name VARCHAR(255),
    industry VARCHAR(255),
    estimated_num_employees INT,
    city VARCHAR(255),
    state VARCHAR(255),
    company_country VARCHAR(255),
    annual_revenue FLOAT,
    total_funding FLOAT,
    latest_funding_stage VARCHAR(255),
    status VARCHAR(255),
    decayed_inbound_score DOUBLE,
    decayed_intent_score DOUBLE,
    decayed_clubbed_score DOUBLE,
    last_visit_date DATE,
    employee_range VARCHAR(255),
    revenue_range VARCHAR(255)
);"""
client_guidelines = """GUIDELINES:
- for count/total/number of visitors you must return sum of no_of_visiting_ips
- for count/total/number of hits you must return sum of no_of_hits
- if just domain is mentioned, always compare it with customer_domain
- if 'lead' is mentioned before domain name, compare it lead_domain
- if country name is abbreviated, use full name of the country
- industry name should always be in lowercase
- visitors and users can be used interchangeably 
- For employee ranges always use estimated number of employees to compare
- For revenue ranges always use annual revenue to compare, don't use revenue_range
- For rolling window type questions, remember to use partition by 
"""

if __name__ == '__main__':
    main()
