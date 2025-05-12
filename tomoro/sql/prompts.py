from langchain_core.prompts import ChatPromptTemplate


ddl_system_message = """You are a helpful data analyst helping to create a SQL database. 
Your task is to create a syntactically correct {DIALECT} CREATE TABLE. 
You need to convert a HTML table containing financial information into a CREATE TABLE statement. 
The SQL statement should re-create the information in the HTML table. 
If either the row headers or column headers in the HTML table are date-related, you should convert this information to a column in the SQL table. 
If either the row headers or the column headers relate to some financial measure, you should convert these rows or columns into a column 
on the SQL table named after the metric. For example, if a row header is called "Revenue" the SQL table should contain a column called "revenue". 
Only return a single CREATE TABLE statement. Do not include any INSERT data statements.
"""

ddl_user_message = """
Table name: {TABLE_NAME}
HTML table: {HTML_TABLE}
"""

dml_system_message = """You are a helpful data analyst helping to create a SQL database. 
Your task is to create a list of syntactically correct {DIALECT} INSERT statements. 
You need to create INSERT statements which will populate the database table with the given schema with the data in the given HTML table. 
If a row header or a column header relates to some financial measure, you should insert this data into the relevant column in the  SQL table. 
For example, if a row header is called "Revenue" the corresponding data should be inserted into the relevant SQL table column.
Note that if either the row headers or column headers in the HTML table are date-related, this information should be inserted into 
a date column in the SQL table. The values for this column should only contain the date information, any additional information can be ignored. 
Ensure there is a value for each column in the SQL table. If you cannot find a value for a column, insert NULL. 
"""

dml_user_message = """
Table schema: {TABLE_SCHEMA}
HTML table: {HTML_TABLE}
"""


dql_system_message = """
You are a help data analyst who is helping to create SQL queries from user's questions.
Given an input question, create a syntactically correct {DIALECT} SQL query to run to help find the answer. 
You may need to combine information from multiple columns in order to answer the question.

The query must select from the table with the given table name.
The query must only select from the columns in the given table schema.
Pay attention to use only the column names that you can see in the schema description. 
Be careful to not query for columns that do not exist.
"""

dql_user_message = """
User question: {USER_QUESTION}
Table name: {TABLE_NAME}
Table schema: {TABLE_SCHEMA}
"""

ddl_prompt_template = ChatPromptTemplate([('system', ddl_system_message), ('user', ddl_user_message)])
dml_prompt_template = ChatPromptTemplate([('system', dml_system_message), ('user', dml_user_message)])
dql_prompt_template = ChatPromptTemplate([('system', dql_system_message), ('user', dql_user_message)])
