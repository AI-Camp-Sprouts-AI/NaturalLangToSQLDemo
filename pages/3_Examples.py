import streamlit as st


st.markdown("""

## 1. Default Model Demo

Here is the python code for generating the PostgreSQL query using GPT-3.5 Turbo 16k model

```python
from text_to_sql import create_model, get_sql_query, execute_command

# set OPENAI_API_KEY in the environment variable 
model = create_model()

model.load_schema_from_file('<file_path>')

llm_output = get_sql_query(model, '<natural_language_query>')

print('SQL Query: ', llm_output.message)

if llm_output.is_final_output:
    print('SQL Output: ', execute_command(llm_output.message)))
```
### Terminal Output

```bash
Sample Terminal Output:

Enter your question here: "Give me all the users visiting meta.com in the year 2022"
SQL Query: "SELECT * FROM website_aggregates WHERE customer_domain ILIKE '%meta.com' AND dt >= '2022-01-01' AND dt <= '2022-12-31'"

```


## 2. Custom Model Demo

```python
from text_to_sql import create_model, get_sql_query
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())
api_key = getenv('OPENAI_API_KEY')
llm = ChatOpenAI(model="gpt-3.5-turbo",
                 openai_api_key=api_key, temperature=0)

model = create_model(llm)

query = input('Enter your question here: ')

model.load_schema_as_file(<file_path>)

output = get_sql_query(model, query)

print('SQL Query: ', output.message)

```

### Terminal Output

```bash
Enter your question here: "Show me the visitor count for the hardy.net domain"
SQL Query: "SELECT SUM(no_of_visiting_ips) AS visitor_count
FROM website_aggregates
WHERE customer_domain ILIKE 'hardy.net';"
```

## 3. Execute the Query in Database

```python
import os
from text_to_sql import create_model, \
    get_sql_query, \
    execute_command, \
    connect_and_execute_command
from pathlib import Path

# !IMPORTANT: OPENAI_API_KEY should be added in the environment variable before calling this function
model = create_model()

cwd = Path(__file__).parent

query = input('Enter your question here: ')

model.load_schema_from_file(cwd.joinpath('./schema.txt').absolute())

output = get_sql_query(model, query)

sql_query = output.message

print('SQL Query:', sql_query)

if output.is_final_output:  # A condition to prevent executing invalid queries
    
    # Before using this execute_command function, certain environmental variables must be set
    # DB_NAME = <name_of_database>
    # USERNAME = <user_name>
    # PASSWORD = <password>
    # HOST = <host url of the database>
    # PORT = <port number of the database>
    print('SQL Output with Mock Database:', execute_command(sql_query))

if output.is_final_output:  # A condition to prevent executing invalid queries
    params = {
        # Use Custom values instead of this environmental variables
        'dbname': os.environ.get("DB_NAME"),
        'user': os.environ.get("USERNAME"),
        'password': os.environ.get("PASSWORD"),
        'host': os.environ.get("HOST"),
        'port': os.environ.get("PORT")
    }
    print('SQL Output with Custom Database:',
          connect_and_execute_command(params, sql_query))

```

### Terminal Output
```bash
Enter your question here: "What is the sum total of visitors that have accessed lead domain meta.com within the $100k-$1M revenue range?"
SQL Query: "SELECT SUM(no_of_visiting_ips) 
FROM website_aggregates 
WHERE lead_domain = 'meta.com' 
AND annual_revenue >= 100000 
AND annual_revenue <= 1000000;"
SQL Output with Mock Database: "[(Decimal('290889'),)]"
SQL Output with Custom Database: "[(Decimal('290889'),)]"
```
""")
