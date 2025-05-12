from langchain_core.language_models.base import BaseLanguageModel
from langchain_community.utilities import SQLDatabase
from .prompts import ddl_prompt_template, dml_prompt_template, dql_prompt_template
from pydantic import BaseModel, Field


class CreateTable(BaseModel):
    """
        Generated SQL CREATE TABLE statement.
    """
    create_table_statement: str = Field(description='The CREATE TABLE statement')


class InsertData(BaseModel):
    """ 
        Generated SQL INSERT statements.
    """
    insert_data_statements: list[str] = Field(description='INSERT statements to populate the table')
    

class GeneratedQuery(BaseModel):
    """Generated SQL SELECT query"""
    query: str = Field(description='Syntactically valid SQL SELECT query.')


class SQLGenerator:
    """
        Uses an LLM to generate SQL statements.
    """

    def __init__(self, db_path: str, llm: BaseLanguageModel):
        self.db = SQLDatabase.from_uri(db_path)
        self.llm = llm    

    def generate_ddl(self, html_table: str, table_name: str) -> str:
        """
            Generates SQL CREATE TABLE statements.
        """
        prompt = ddl_prompt_template.invoke({'DIALECT': self.db.dialect, 'TABLE_NAME': table_name, 'HTML_TABLE': html_table})
        structured_llm = self.llm.with_structured_output(CreateTable)
        result = structured_llm.invoke(prompt)
        return result.create_table_statement

    def generate_dml(self, html_table: str, table_schema: str) -> str:
        """
            Generates SQL INSERT statements.
        """
        prompt = dml_prompt_template.invoke({'DIALECT': self.db.dialect, 'TABLE_SCHEMA': table_schema, 'HTML_TABLE': html_table})
        structured_llm = self.llm.with_structured_output(InsertData)
        result = structured_llm.invoke(prompt)
        return result.insert_data_statements

    def generate_dql(self, question: str, table_name: str, table_schema: str) -> str:
        """
            Generate SQL SELECT query statements.
        """
        prompt = dql_prompt_template.invoke({'DIALECT': self.db.dialect, 'USER_QUESTION': question, 'TABLE_NAME': table_name, 'TABLE_SCHEMA': table_schema})
        structured_llm = self.llm.with_structured_output(GeneratedQuery)
        result = structured_llm.invoke(prompt)
        return result.query
    