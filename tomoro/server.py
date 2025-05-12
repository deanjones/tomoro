from fastapi import FastAPI
from .config import get_env_var
from .vector_store import get_store
from langchain_community.utilities import SQLDatabase
from .retrieve import Retriever
from .sql import SQLGenerator
from .utils import get_llm
from pydantic import BaseModel
from typing import Any


class Question(BaseModel):
    question: str


class Response(BaseModel):
    question: str
    answer: str


app = FastAPI()


VECTOR_STORE_TYPE = get_env_var('VECTOR_STORE')
VECTOR_DB_PATH = get_env_var('VECTOR_DB_PATH')
VECTOR_DB_COLLECTION_NAME = get_env_var('VECTOR_DB_COLLECTION_NAME')
SQL_DB_NAME = get_env_var('SQL_DB_NAME')
LLM_TYPE = get_env_var('LLM')


vector_store = get_store(VECTOR_STORE_TYPE, db_path=VECTOR_DB_PATH, collection_name=VECTOR_DB_COLLECTION_NAME)
sqlite_uri = f'sqlite:///{SQL_DB_NAME}'
sql_db = SQLDatabase.from_uri(sqlite_uri)
llm = get_llm(LLM_TYPE)
sql_generator = SQLGenerator(sqlite_uri, llm)
retriever = Retriever(vector_store, llm, sql_db, sql_generator)


@app.post("/query/", response_model=Response)
def query(question: Question) -> Any:
    question_text = question.question
    answer = retriever.retrieve(question_text)
    return {'question': question_text, 'answer': str(answer)}
