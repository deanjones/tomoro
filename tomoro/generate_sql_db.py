from tomoro.record import read_records
from tomoro.config import get_env_var
from tomoro.sql import SQLGenerator
from .utils import make_table_name, get_llm
from sqlalchemy import create_engine, Engine
from langchain_core.language_models.base import BaseLanguageModel
import sqlite3
from sqlite3 import Connection
from tqdm import tqdm


def create_table(connection: Connection, table_name: str, create_table_stmt: str):
    cursor = connection.cursor()
    cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
    cursor.execute(create_table_stmt)


def insert_data(connection: Connection, insert_data_stmt: str):
    cursor = connection.cursor()
    cursor.execute(insert_data_stmt)


def main():
    """"
        Reads in the data from train.json, and generates a SQLite database, one table per record.
        Uses an LLM to generate the CREATE TABLE and INSERT statements, based on the HTML table 
        in the record.

    """
    data_path = get_env_var('DATA_PATH')
    records = read_records(data_path)
    print(f'Loaded {len(records)} records from {data_path}')
    llm_type = get_env_var('LLM')
    llm = get_llm(llm_type)
    db_name = get_env_var('SQL_DB_NAME')
    sql_generator = SQLGenerator(f'sqlite:///{db_name}', llm)
    with sqlite3.connect(db_name) as connection:
        for record in tqdm(records):
            table_name = make_table_name(record.id)
            create_table_stmt = sql_generator.generate_ddl(record.table, table_name)
            insert_data_stmts = sql_generator.generate_dml(record.table, create_table_stmt)
            try:
                create_table(connection, table_name, create_table_stmt)
                for insert_data_stmt in insert_data_stmts:
                    insert_data(connection, insert_data_stmt)
                connection.commit()
            except sqlite3.Error as e:
                print(f'Error inserting data: {e}')
                connection.rollback()


if __name__ == '__main__':
    main()
