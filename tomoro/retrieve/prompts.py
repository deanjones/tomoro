from langchain_core.prompts import ChatPromptTemplate


rerank_system_message = """You are a helpful data analyst helping to query a SQL database. 
Your task is to identify which table in a sql database can be used to answer a user question. 
You will be given a user question and some SQL table information which shows the CREATE TABLE statement
for each table and some sample data.
You should identify the table that is most relevant to the user question and return the name of this table. 
"""

rerank_user_message = """
User question: {USER_QUESTION}
SQL table information: {TABLE_INFORMATION}
"""

rerank_prompt_template = ChatPromptTemplate([('system', rerank_system_message), ('user', rerank_user_message)])
