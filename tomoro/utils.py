import re
from langchain_core.language_models.base import BaseLanguageModel
from .config import get_env_var


def make_table_name(record_id: str) -> str:
    return re.sub('[-/.]', '_', record_id)

def get_llm(llm_type: str) -> BaseLanguageModel:
    if llm_type == 'openai':
        from langchain_openai import ChatOpenAI
        llm_model = get_env_var('LLM_MODEL')
        api_key = get_env_var('OPENAI_API_KEY')
        llm = ChatOpenAI(model_name=llm_model, temperature=0, api_key=api_key)
    else:
        raise ValueError(f"Unsupported LLM type: {llm_type}")
    return llm
