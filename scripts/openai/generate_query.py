import getpass
import os
import sys
from dotenv import load_dotenv

from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from sqlalchemy.pool import StaticPool
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from prompt_question import define_prompt
# Add the directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
from get_engine import get_engine_for_chinook_db,get_engine_for_energy_data


load_dotenv()
openai_api_key = os.environ['OPENAI_API_KEY']
# print(os.environ["OPENAI_API_KEY"])
# os.environ["OPENAI_API_KEY"] = getpass.getpass()

# engine = get_engine_for_chinook_db()
engine = get_engine_for_energy_data()

# Create LangChain DB
db = SQLDatabase(engine)

# print(db.dialect)
# print(db.get_usable_table_names())
# db.run("SELECT * FROM Artist LIMIT 10;")

llm = ChatOpenAI(model="gpt-4") # responses differ per model e.g. 4o or 4o-mini respond with text + SQL and the SQL query fails on the Database


# Design prompt
prompt_template = define_prompt()
# print(prompt)

# Generate query:
chain = create_sql_query_chain(llm, db, define_prompt())
print("Prompt:")
chain.get_prompts()[0].pretty_print()
sql_query = chain.invoke({"question": "How many entities are there"})

print("sql_query:",sql_query)

#Execute Query:
execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db, define_prompt())
chain = write_query | execute_query
results = chain.invoke({"question": "How many entities are there"})
print("query results:", results)


# Then answer the question
# https://python.langchain.com/v0.2/docs/tutorials/sql_qa/#answer-the-question
