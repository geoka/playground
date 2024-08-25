import getpass
import os
import sqlite3
from dotenv import load_dotenv
import requests
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_google_vertexai import ChatVertexAI
from langchain.chains import create_sql_query_chain
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from prompt_prep import define_prompt


# load_dotenv()
# google_api_key = os.environ['GOOGLE_API_KEY']
# print(os.environ["OPENAI_API_KEY"])
# os.environ["OPENAI_API_KEY"] = getpass.getpass()

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

llm = ChatVertexAI(model="gemini-1.5-flash")

execute_query = QuerySQLDataBaseTool(db=db)

# prompt
QUESTION = 'How many employees are there'
TABLE_INFO = 'Employee'
DIALECT = 'SQLlite'
TOP_K = "10"
prompt_template = define_prompt()
# print(prompt)

write_query = create_sql_query_chain(llm, db, prompt_template)

# chain = write_query
chain = write_query | execute_query
chain.get_prompts()[0].pretty_print()

response = chain.invoke({"question": QUESTION, "top_k": TOP_K})

print("response:",response)

# Then answer the question
# https://python.langchain.com/v0.2/docs/tutorials/sql_qa/#answer-the-question

# chain = create_sql_query_chain(llm, db)
# chain.get_prompts()[0].pretty_print()
# response = chain.invoke({"question": "How many employees are there"})
# print(response)
# db.run(response)
