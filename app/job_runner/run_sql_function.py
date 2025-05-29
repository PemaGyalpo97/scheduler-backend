# app/job_runner/sql_executor.py

from sqlalchemy import create_engine, text
from app.database.session import SQLALCHEMY_SYNC_DATABASE_URL

engine = create_engine(SQLALCHEMY_SYNC_DATABASE_URL)

def execute_sql_function(function_name: str):
    with engine.connect() as conn:
        conn.execute(text(f"SELECT {function_name}();"))
        conn.commit()

    print(f"Function {function_name} executed successfully.")