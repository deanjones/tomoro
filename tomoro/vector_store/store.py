from .document import Document
from abc import ABC, abstractmethod
import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


def get_store(store_type: str, **kwargs) -> 'DocumentStore':
    """
    Get the document store based on the specified type.
    """
    if store_type == "chroma":
        return ChromaDocumentStore(**kwargs)
    else:
        raise ValueError(f"Unknown store type: {store_type}")


class DocumentStore(ABC):
    """
        A DocumentStore associates table metadata with the names of SQL tables, and is used
        to identify the set of candidate tables that can be used to answer a user question.
    """

    @abstractmethod
    def store(self, documents: list[Document]) -> None:
        """
        Store the given documents.
        """
        raise NotImplementedError('Subclasses should implement this method.')

    @abstractmethod
    def retrieve(self, query: str, k: int) -> list[Document]:
        """
        Retrieve the top k documents which match the query.
        """
        raise NotImplementedError('Subclasses should implement this method.')


class ChromaDocumentStore(DocumentStore):
    """
        A DocumentStore based on ChromaDB.
    """
    def __init__(self, db_path: str, collection_name: str):
        db_path = db_path
        collection_name = collection_name
        db_client = chromadb.PersistentClient(path=db_path)
        embeddings = OpenAIEmbeddings(model='text-embedding-3-large')  # this could be made configurable
        self.vector_store = Chroma(client=db_client, collection_name=collection_name, persist_directory=db_path, embedding_function=embeddings)

    def store(self, documents: list[Document]) -> None:
        """
            Persist the given documents into the vector store.
        """
        ids = [doc.id for doc in documents]
        self.vector_store.add_documents(documents=documents, ids=ids)

    def retrieve(self, query: str, k=2) -> list[Document]:
        """
            Retrieve the top k documents which match the query.
        """
        results = self.vector_store.similarity_search(query, k=k)
        return results
    