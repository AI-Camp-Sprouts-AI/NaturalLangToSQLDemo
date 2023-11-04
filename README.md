# Text-to-SQL Query Demo

## Overview
This project demonstrates a Language Model (LLM) that can interpret natural language queries and generate corresponding PostgreSQL queries. The project is implemented in Python and uses the langchain package to interface with a suitable language model, which could be any of the GPT models provided by OpenAI or other language models that support the same interface.

## Files:
 - **'llm.py'**: Contains the core logic for converting text to SQL queries.
 - **'main.py'**: A Streamlit application that provides a user-friendly interface for interacting with the model.

 ## Features
 - **Natural Language Understanding**: Accepts user input in natural language and interprets the intent behind the text.
 - **SQL Generation**: Produces PostgreSQL queries based on the provided input.
 - **Schema Aware**: Takes a database schema as input to generate context-specific queries.
 - **Interactive Chat**: Utilizes a chat interface for receiving user input and displaying the generated SQL queries.
 - **State Management**: Maintains conversation state to allow for context-aware query generation.
 - **Review Mode**: A mechanism to review and ensure that the generated content strictly contains SQL queries.