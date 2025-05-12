import os
from dotenv import load_dotenv


load_dotenv()


def get_env_var(var_name: str):
    val = os.getenv(var_name)
    if val is None:
        raise ValueError(f"Environment variable {var_name} not set.")
    else:
        return val
