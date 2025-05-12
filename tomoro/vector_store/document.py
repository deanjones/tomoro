from langchain_core.documents import Document
from tomoro import Record
from tomoro.utils import make_table_name


def create_document(record: Record) -> Document:
    """
    Combine table row and column headers into a single string and stuff into a Document object.
    """
    table = record.table
    table_text = " ".join([entry for row in table for entry in row])
    return Document(id=record.id, page_content=table_text, metadata={'id': record.id, 'table_name': make_table_name(record.id)})
