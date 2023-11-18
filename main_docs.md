# Natural Language to PostgreSQL

This Python package converts natural language queries into PostgreSQL commands. It uses OpenAI's GPT-3.5-turbo model to understand and translate the user's input into SQL queries. The package also includes functionalities for testing the accuracy of the model and generating mock data.

## Installation

To install the package, clone the repository and install the required dependencies.

## Usage

### Creating a Model

To create a model, use the `create_model` function. This function initializes the language model with the OpenAI API key and sets the temperature to 0.

```python
from src import create_model

model = create_model()
```

### Loading a Schema

To load a schema from a file, use the `load_schema_from_file` method. This method takes the absolute path of the schema file as an argument.

```python
model.load_schema_from_file('/path/to/schema.txt')
```

### Predicting SQL Queries

To predict a SQL query from a natural language input, use the `predict` method. This method takes a string as an argument and returns a `ModelOutput` object. The `ModelOutput` object has two properties: `message` and `is_final_output`. The `message` property contains the predicted SQL query, and the `is_final_output` property is a boolean that indicates whether the predicted SQL query is the final output.

```python
user_input = "How many total visitors have visited hardy.net domain?"
output = model.predict(user_input)

print("Query: ", output.message)
print("Is final output: ", output.is_final_output)
```

### Running Test Suites

To run test suites, use the `run_test_suites` function. This function lists all the test files for the user to select and runs the selected test file.

```python
from src import run_test_suites

run_test_suites()
```

### Creating Mock Data

To create mock data, use the `create_mock_data` function. This function lists all the data structure files for the user to select and asks how many number of fake data has to be generated. It then generates the specified number of fake data based on the selected data structure.

```python
from src import create_mock_data

create_mock_data()
```

## Testing

The package includes a test suite for the `website_aggregates` schema. The test suite is defined in the `website_aggregate_test.py` file. Each test case in the test suite is a dictionary with the following keys:

- `input`: The natural language input.
- `sql_output`: The expected SQL output.
- `description`: A description of the test case (optional).

To run the test suite, use the `run_test_suites` function and select the `website_aggregate_test.py` file.