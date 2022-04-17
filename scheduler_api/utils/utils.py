import os

from sqlalchemy.engine import create_engine

def get_config_value(env_var: str) -> str:
    return os.getenv(env_var)

engine = create_engine(get_config_value('JOB_STORE_DB_CONN_STR'), pool_recycle=1800)

def get_engine():
    return engine
