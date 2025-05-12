from tomoro.record import read_records
from tomoro.config import get_env_var
from tomoro.vector_store import get_store, create_document


def main() -> None:
    """
        Reads in the data from train.json, and generates a vector store, one document per record.
        The vector store is used to associate searchable table schema information with table names.
    """
    data_path = get_env_var('DATA_PATH')
    records = read_records(data_path)
    print(f"Loaded {len(records)} records from {data_path}")
    store_type = get_env_var('VECTOR_STORE')
    vec_store = get_store(store_type, db_path=get_env_var('VECTOR_DB_PATH'), collection_name=get_env_var('VECTOR_DB_COLLECTION_NAME'))
    documents = [create_document(record) for record in records]
    vec_store.store(documents)

if __name__ == "__main__":
    main()