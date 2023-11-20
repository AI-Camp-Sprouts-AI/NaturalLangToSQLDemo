import streamlit as st
import plotly.express as px
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="Text to SQL",
    page_icon="👋",
)

st.markdown("""# Natural Language to PostgreSQL Convertor""")
st.markdown(
    '##### AI tool to convert natural language text to PostgreSQL commands with 94% accuracy')


open_chatbot = st.button("Open Chatbot", key="top_button", type="primary")
if open_chatbot:
    switch_page("chatbot")

st.header('Project Overview')

st.markdown("""
Our project aimed to create a Python package that can interpret natural language and convert it into PostgreSQL commands. This package can be used to interact with a PostgreSQL database using natural language, making it more accessible and user-friendly.

The main components of our project include:

- A chatbot interface for user interaction
- A natural language processing module for interpreting user input
- A database connector for executing PostgreSQL commands
- A mock data generator for testing and demonstration purposes

""")

st.header('Demo')

st.video('./assets/demo.webm', format="video/webm", start_time=10)

st.header('Workflows')

st.markdown('### Our Complete Workflow')

st.image('assets/Workflow.png',
         caption='Complete Workflow of the model')

"---"

st.markdown(f'### Internals of the Package')

st.image('assets/Workflow-Text2SQL.png',
         caption='Internals of the Text to SQL')

"---"

st.header('Progress and Achievements')


st.markdown("""
            
Despite a challenging start, our team managed to pull together and complete the project within the final few weeks. Here are some of our key achievements:

- Developed a Python package that successfully translates natural language into PostgreSQL commands
- Created a chatbot interface for user interaction
- Built a database connector that can execute PostgreSQL commands
- Generated mock data for testing and demonstration purposes
- Collaborated effectively as a team and learned a lot in the process

""")

st.header("Testing Results")
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    st.markdown("""
    - Test Categories : 18
    - Input Variants / Category  : 20
    - Repetitions / Input    : 10
    - Assertions / Test : 2
    
    ##### Total Assertions : 7200
    ##### Passed Assertions : 6778 (94%)
    ##### Failed Assertions : 4222 (6%)
    """)

with col2:
    data = {
        'value': [6778, 422],
        'label': ['Passed', 'Failed']
    }
    fig = px.pie(data,
                 values="value",
                 names='label',
                 title="Status of Assertions")
    fig.update_layout(
        width=200
    )
    st.plotly_chart(fig, theme="streamlit")


