import os
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase


# Connect to your Google BigQuery database
# db = SQLDatabase.from_uri("bigquery://")
BIGQUERY_PROJECT = "ni-sadc-live"
BIGQUERY_DATASET = "ni_gk_eu"

SERVICE_ACCOUNT_KEY_PATH = os.environ["SERVICE_ACCOUNT_KEY_PATH"]
SQL = f'bigquery://{BIGQUERY_PROJECT}/{BIGQUERY_DATASET}' #?credentials_path={SERVICE_ACCOUNT_KEY_PATH}'
db = SQLDatabase.from_uri(SQL)

# Create a language model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Create the SQL agent
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
