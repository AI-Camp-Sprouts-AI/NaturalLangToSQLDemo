from enum import Enum
from langchain.schema.language_model import BaseLanguageModel
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ModelOutput:
    message: str
    is_final_output: bool = False


class IBaseClass(ABC):
    @abstractmethod
    def predict(self, user_input: str) -> ModelOutput:
        pass

# Enumerators
OutputTypes = Enum('OutputTypes', [
    'SQL',
    # 'API' # This is for a later use case
])

from enum import Enum
from langchain.schema.language_model import BaseLanguageModel
from langchain.schema import HumanMessage, SystemMessage, AIMessage

# Enumerators
OutputTypes = Enum('OutputTypes', [
    'SQL',
    # 'API' # This is for a later use case
])

class NLP2SQL(IBaseClass):
    """
    This class implements the Natural Language to the SQL 
    functionality of the package
    """
    system_prompt: str
    schema: str
    options: dict
    llm: BaseLanguageModel

    def __init__(self, llm, options) -> None:
        self.llm = llm
        self.options = options

        self.schema = ''

        self.relevancy_prompt = """
            As an experienced data analyst with expertise in PostgreSQL, your role is to assess the relevance of a human prompt in relation to a given database schema, focusing on flexibility and practical interpretations. 
            Determine if the schema can plausibly support answering the question in the prompt.

            Respond with 'yes' or 'no':
            - 'Yes' if it is reasonably possible to answer the prompt using the given schema, erring on the side of a broader interpretation of column names and data types.
            - 'No' only if the prompt clearly cannot be answered with the available schema information.
            Remember to include yes or no in your responses.

            Use common database naming conventions and industry practices as a guide, but lean towards inclusive interpretations. Avoid overly stringent verification or requests for clarification unless absolutely necessary.

            Database Schema:
            {schema}
        """.replace('  ', '').strip()

        self.generation_prompt = """
            As a proficient SQL developer, your task is to create a PostgreSQL query based on a human prompt, with reference to the provided database schema. 
            Your expertise in SQL syntax and database querying techniques is essential for developing a valid SQL query.

            The response must strictly consist of the PostgreSQL query. Exclude all additional commentary or explanation. 
            The query should be concise, well-structured, and adhere to standard PostgreSQL practices, ensuring optimized execution.

            Focus exclusively on the database schema's structure, fields, relationships, and other relevant details when formulating your query. 

            Database Schema:
            {schema}

            Formulate an appropriate PostgreSQL query in direct response to the human prompt. Your response should contain solely the SQL query, with no text other than the query itself.
        """.replace('  ', '').strip()

        self.review_prompt = """
            As an expert in SQL and database management, your task is to review a provided PostgreSQL query and determine its impact on the database. 
            Specifically, assess whether the query modifies the database in any way (such as through INSERT, UPDATE, DELETE, or ALTER statements).

            Your response should be a simple 'yes' or 'no'. 
            Answer 'yes' if the query does not modify the database. 
            Answer 'no' if the query does modify the database.

            Database Schema:
            {schema}

            Review the query and respond with 'yes' if it is safe in terms of not modifying the database and not including external elements, or 'no' if it fails to meet these criteria.
        """.replace('  ', '').strip()

        self.clarification_prompt = """
            Given that the human prompts provided for SQL query generation are known to be invalid (either due to ambiguity, incompleteness, or potential malicious intent), your role is to systematically request additional information or clarification. 
            Your response should aim to guide the prompt provider towards supplying the necessary details for formulating a valid and secure SQL query.

            For each prompt, identify key areas where information is lacking, ambiguous, or potentially harmful, and formulate a precise request for the needed information. 
            Your goal is to engage constructively with the prompt provider, guiding them to refine their request into a clear, complete, and secure format suitable for SQL query generation.

            Upon receiving an invalid prompt, respond with specific questions or requests that address the shortcomings of the prompt, ensuring that your response facilitates the creation of a valid SQL query while maintaining database security and integrity.

            Database Schema:
            {schema}

            Assess the prompt and respond with targeted requests for clarification or additional details, guiding the prompt provider towards a valid and secure SQL query formulation.
            LIMIT YOUR RESPONSES TO UNDER THREE SENTENCES IN LENGTH.
        """.replace('  ', '').strip()

        self.chat_history = []
        self.memory_length = options['memory']*2 if 'memory' in options else 0

    def predict(self, user_input: str) -> ModelOutput:
        if len(self.schema) == 0:
            return ModelOutput("Schema not loaded", True)
        if len(user_input) == 0:
            return ModelOutput("I'm sorry, I don't understand your question.", False)
        if user_input[-1] not in '.;:?!':
            user_input += '.'

        final_output = False

        relevancy_prompt = self.relevancy_prompt.format(schema=self.schema)
        messages = [SystemMessage(content=relevancy_prompt), HumanMessage(content=user_input)]
        response = self.llm.predict_messages(messages=(self.chat_history + messages)).content
        #print("Relevancy:\n"+response)

        if 'yes' in response.lower():
            generation_prompt = self.generation_prompt.format(schema=self.schema)
            messages = [SystemMessage(content=generation_prompt), HumanMessage(content=user_input)]
            response = self.llm.predict_messages(messages=(self.chat_history + messages)).content
            #print("SQL:\n"+response)

            review_prompt = self.review_prompt.format(schema=self.schema)
            messages = [SystemMessage(content=review_prompt), HumanMessage(content=response)]
            review_response = self.llm.predict_messages(messages=messages).content
            #print("Review:\n"+review_response)
            if 'yes' in review_response.lower():
                final_output = True
            else:
                response = "I'm sorry, I don't understand your question."
        else:
            clarification_prompt = self.clarification_prompt.format(schema=self.schema)
            messages = [SystemMessage(content=clarification_prompt), HumanMessage(content=user_input)]
            response = self.llm.predict_messages(messages=(self.chat_history + messages)).content

        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=response))
        if len(self.chat_history) > self.memory_length:
            excess = len(self.chat_history) - self.memory_length
            self.chat_history = self.chat_history[excess:]

        return ModelOutput(response.strip(), final_output)

    def override_system_prompt(self, new_system_prompt: str) -> None:
        if '{schema}' in new_system_prompt:
            self.system_prompt = new_system_prompt

    def override_review_prompt(self, new_review_prompt: str) -> None:
        self.review_prompt = new_review_prompt

    def load_schema_from_file(self, file_path: str) -> bool:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
            self.load_schema_as_string(contents)

    def load_schema_as_string(self, schema: str) -> bool:
        self.schema = schema

    def clear_chat_history(self) -> None:
        self.chat_history = []

# Can be implemented later


# class NLP2API(IBaseClass):
#     def __init__(self) -> None:
#         pass

#     def predict(self, user_input: str) -> ModelOutput:
#         pass

#     def load_context_from_file(self, file_path: str) -> bool:
#         pass

#     def load_context_as_string(self, context: str) -> bool:
#         pass


output_type_class_map = {
    OutputTypes.SQL: NLP2SQL,
    # OutputTypes.API: NLP2API,
}


def initialize_model(llm, options={}, output_type: OutputTypes = OutputTypes.SQL):
    """
    Based on the Output Type the Model will be instantiated
    """

    model_class = output_type_class_map[output_type]
    model_instance = model_class(llm, options)
    return model_instance