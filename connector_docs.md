# Database Connector

`database_connector.py` contains 7 functions that makes interacting with PostgreSQL databases using the psycopg2 Python module easier. The functions currently present include functions for:

- Creating a table
- Deleting a table
- Selecting records from the table
- Inserting new records into an existing table
- Deleting records from an existing table
- Checking if a table exists
- Executing user-inputted commands yourself (recommended)

## Pre-requisites

Before using these functions, ensure that you complete the following beforehand:

1. **Install Python 3**  
Refer to platform-specific instructions for installing Python on your machine.

2. **Install Psycopg2 module**  
If you don't already have it, run `pip install psycopg2` or `pip install psycopg2-binary`. You may have to replace `pip` with `pip3` if the former does not work.

3. **Obtain access to a PostgreSQL server**  
These functions were designed specifically around Supabase's hosted database. You may need to alter the connection details to fit your needs.

4. **Obtain connection details**  
If you are using a PostgreSQL database hosted by Supabase, you'll need the database name, username, password, hostname, and port (optional) to connect to the database. It is recommended that you keep these details secret by placing them in a hidden .env file in the same directory.

5. **Import the functions**  
Import the functions like you would import anything else in Python, by placing this line at the top of your file: `import database_connector`. If you are experiencing difficulties with importing, try this instead:

```python
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from database_connector import *
```

## Executing user commands

### execute_command(command)

This function executes a SQL command passed to it as a string. Use this whenever possible.

- **Parameters:**  
`command`: A string that contains a valid SQL statement to be executed on the database.

- **Returns:**  
A list of tuples that contains the result of the query, or None if the query does not return any rows.

- **Exceptions:**  
If something goes wrong, such as a syntax error or a connection error, it prints the exception and returns None.

- **Example:**

```python
# Create a new table named table_1 with columns name, age, and country
execute_command("CREATE TABLE table_1 (name varchar(255), age int, country varchar(3))")

# Select the names from table_1 where age is greater than 30
result = execute_command("SELECT name FROM table_1 WHERE age > 30")
print(result)
# Output: []
```

## Creating a table

### create_table(table_name, *columns)

This function creates a named table with specified columns.

- **Parameters:**  
`table_name`: A string containing the name of the table to be created.  
`columns`: A string containing names of columns, ` ` (space), the data type of the column, separated by `, ` (comma space).

- **Returns:**  
None.

- **Exceptions:**  
If something goes wrong, such as a table already exists or an invalid data type, it prints the exception and does not create the table.

- **Example:**

```python
# Create a table named table_2 with columns name, age, and country
create_table("table_2", "name varchar(255), age int, country varchar(3)")
```

## Deleting a table

### drop_table(table_name)

This function deletes the table matching the table name.

- **Parameters:**  
`table_name`: A string containing the name of the table to be deleted.

- **Returns:**  
None.

- **Exceptions:**  
If something goes wrong, such as a table does not exist or a permission error, it prints the exception and does not drop the table.

- **Example:**

```python
# Delete table named table_1
drop_table("table_1")
```

## Selecting records

### select(table_name, column_names, selectors=None)

This function selects records from an existing table with optional selectors.

- **Parameters:**  
`table_name`: A string containing the name of the table to select from.  
`column_names`: A list of strings containing the names of columns to retrieve.  
`selectors`: Optional dictionary where the values are either values to match against or tuples of operators and values.

- **Returns:**  
A list of dictionaries representing the records that match the selectors, or all records if no selectors are provided.

- **Exceptions:**  
If something goes wrong, such as a table or a column does not exist or an invalid operator or value, it prints the exception and returns None.

- **Examples:**

```python
# Select records from the name and country column from table_2 where age is less than 30
columns = ["name", "country"]
selectors = {"age":("<", 30)}
result = select("table_2", columns, selectors)
print(result)
# Output: [{'name':'a name', 'country':'ABC'}, ...]

# Select records from the name and age column from table_2 where the country is the US
columns = ["name", "age"]
selectors = {"country":"US"}
result = select("test1", columns, selectors)
print(result)
# Output: [{'name':'a name', 'age':'number'}, ...]
```

## Inserting records

### insert_records(table_name, records)

This function inserts new records into an existing table.

- **Parameters:**  
`table_name`: A string containing the name of the table to insert into.  
`records`: A list of dictionaries where the key is the column name and the value is the value for that column. Each dictionary in the list is a new entry.

- **Returns:**  
None.

- **Exceptions:**  
If something goes wrong, such as a table or a column does not exist or a value does not match the data type, it prints the exception and does not insert the records.

- **Example:**

```python
# Insert two new records into table_2
records = [
			{"name":"John","age":"29","country":"US"},
			{"name":"Jane","age":"24","country":"CA"}
		  ]
insert_records("test1", records)
```

## Dropping records

### delete_records(table_name, selectors=None)

This function deletes records from an existing table using the selectors, or all records if none are specified.

- **Parameters:**  
`table_name`: A string containing the name of the table to drop records from.  
`selectors`: Optional dictionary where the values are either values to match against or tuples of operators and values.

- **Returns:**  
Integer representing the number of records deleted, or zero if no records match the selectors.

- **Exceptions:**  
If something goes wrong, such as a table or a column does not exist or an invalid operator or value, it prints the exception and returns None.

- **Example:**

```python
# Delete records from table_2 where age is less than 20
selectors = {"age": ("<", 20)}
delete_records("table_2", selectors)

# Delete records where name is John
selectors = {"name":"John"}
delete_records("table_2", selectors)

# Delete all records from table_2
delete_records("table_2")
```

## Existing table

### exists(table_name)

This function checks if a table with the given table name exists and returns a boolean.

- **Parameters:**  
`table_name`: A string containing the name of the table to check.

- **Returns:**  
True if a table with the name is found, False otherwise.

- **Exceptions:**  
If something goes wrong, such as a connection error or an invalid table name, it prints the exception and returns False.

- **Example:**

```python
# Check if table_1 exists
print(exists("table_1"))
# Output: False

# Check if table_2 exists
print(exists("table_2"))
# Output: True
```