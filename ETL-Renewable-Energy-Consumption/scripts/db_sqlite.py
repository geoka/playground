import getpass
import os
import sqlite3
import requests
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from langchain.chains import create_sql_query_chain

# print(os.environ["OPENAI_API_KEY"])
os.environ["OPENAI_API_KEY"] = getpass.getpass()

def get_engine_for_chinook_db():
    """Pull sql file, populate in-memory database, and create engine."""
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
    response = requests.get(url)
    sql_script = response.text

    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(sql_script)
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )


engine = get_engine_for_chinook_db()

db = SQLDatabase(engine)

# print(db.dialect)
# print(db.get_usable_table_names())
# db.run("SELECT * FROM Artist LIMIT 10;")

llm = ChatOpenAI(model="gpt-4o-mini")

chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "How many employees are there"})
response
