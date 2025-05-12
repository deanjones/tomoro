from pydantic import BaseModel, ValidationError
from typing import Union
from pathlib import Path
import json


class Annotation(BaseModel):
    amt_table: str
    amt_pre_text: str
    amt_post_text: str

class QA(BaseModel):
    question: str
    answer: str

class Record(BaseModel):
    table: list[list[str]]
    annotation: Annotation
    id: str
    qa: list[QA]


def read_records(data_path: Union[str, Path]) -> list[Record]:
    """
        Read the data from the train.json file and generate a list of Record objects.
    """
    # Read the JSON file
    with open(data_path) as f:
        data = json.load(f)
    # data has fields like 'qa', 'qa_1', 'qa_2' etc which we roll up into a list of QA objects
    for d in data:
        new_qa = []       
        keys = list(d.keys())
        for k in keys:
            if k.startswith('qa'):
                new_qa.append(d[k])
                del d[k]
        d['qa'] = new_qa

    records = []
    for d in data:
        try:
            records.append(Record(**d))
        except ValidationError as e:
            print(f"Validation error for data {d}: {e}")
            continue
    return records

