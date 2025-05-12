from ..vector_store import DocumentStore
from ..sql import SQLGenerator
from .prompts import rerank_prompt_template
from langchain_core.language_models.base import BaseLanguageModel
from langchain_community.utilities import SQLDatabase
from pydantic import BaseModel, Field


class TableSelection(BaseModel):
    table_name: str = Field(description='The name of the table that can be used to answer the question')


class Retriever:
    """
        Find the SQL table that can be used to answer to a user's question, then generate the SQL query to get the answer.
    """
        
    def __init__(self, vector_store: DocumentStore, llm: BaseLanguageModel, sql_db: SQLDatabase, sql_generator: SQLGenerator):
        self.vector_store = vector_store
        self.llm = llm
        self.sql_db = sql_db
        self.sql_generator = sql_generator

    def retrieve(self, question: str, k: int = 10) -> str:
        """
            Queries the vector to identify the set of potential tables can be used to answer the question,
            then tries to identify the best table from the set of potential tables. Finally, generates a SQL
            query to get the answer from the selected table.
        """
        results =  self.vector_store.retrieve(question, k)
        # query the table(s) to get the answer
        table_names = [result.metadata['table_name'] for result in results]

        # identify which table(s) can be used to answer the question
        # get the table schemas
        table_info = self.sql_db.get_table_info_no_throw(table_names)
        best_table_name = self.get_best_table_name(question, table_info)
        # generate the SQL query against the selected table
        best_table_info = self.sql_db.get_table_info_no_throw([best_table_name])
        sql_query = self.sql_generator.generate_dql(question, best_table_name, best_table_info)
        # get the answer from the selected table
        try:
            db_result = self.sql_db.run_no_throw(sql_query)
        except Exception as e:  # this happens frequently e.g. when LLM has generated an invalid query
            db_result = None
        result = ''
        if db_result and not db_result.startswith('Error'):
            try:
                evald_result = eval(db_result)  # result is a list of tuples represented as a string
                result = evald_result[0][0]
            except Exception as e:
                pass
        return result

    def get_best_table_name(self, question: str, table_info: str) -> str:
        """
            Given the user question and the table information, ask LLM to 
            identify the best table that can be used to answer the question.
        """
        prompt = rerank_prompt_template.invoke({'USER_QUESTION': question, 'TABLE_INFORMATION': table_info})
        structured_llm = self.llm.with_structured_output(TableSelection)
        result = structured_llm.invoke(prompt)
        return result.table_name
