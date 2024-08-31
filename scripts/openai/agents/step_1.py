import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.pool import SingletonThreadPool
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from system_prompt import return_system_message

def get_engine_for_energy_data():
    """
    Creates an SQLAlchemy engine.

    :param db_path: The database connection string.
                    Default is for a SQLite database named 'energy.db'.
                    For in-memory database use 'sqlite:///:memory:'.
    :return: SQLAlchemy engine object.
    """

    db_file = 'data/energy_data.db'
    # Connect to the disk-based database
    disk_conn = sqlite3.connect(db_file) # works OK
    # cursor = disk_conn.cursor()
    # print("Database created and Successfully Connected to SQLite")

    # Create an in-memory database
    # memory_conn = sqlite3.connect(':memory:')
  
    # Attach the disk-based database to the in-memory database
    # disk_conn.backup(memory_conn)

    # Close the connection to the disk-based database
    # disk_conn.close()

    print("Loaded energy.db into memory.")

    engine = create_engine(
        "sqlite://",
        creator=lambda: disk_conn,
        poolclass=SingletonThreadPool,
        connect_args={"check_same_thread": False},
    )


    # Get a list of all tables in the database
    # inspector = inspect(engine)

    # tables = inspector.get_table_names()
    # print(tables)

    return engine

engine = get_engine_for_energy_data()

# Create LangChain DB
db = SQLDatabase(engine)
# responses differ per model e.g. 4o or 4o-mini respond with text + SQL
#  and the SQL query fails on the Database
llm = ChatOpenAI(model="gpt-4")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()

# print(tools)

system_message = return_system_message()
agent_executor = create_react_agent(llm, tools, messages_modifier=system_message)

for s in agent_executor.stream(
    {"messages": [HumanMessage(content="Which country's in which year has consumed most biofuels?")]}
):
    print(s)
    print("----")
