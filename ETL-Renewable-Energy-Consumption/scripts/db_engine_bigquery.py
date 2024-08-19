from sqlalchemy import *
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit,create_sql_agent
from langchain_community.utilities import SQLDatabase


# Connect to your Google BigQuery database
# db = SQLDatabase.from_uri("bigquery://")
BIGQUERY_PROJECT = "ni-sadc-live"
BIGQUERY_DATASET = "ni_gk_eu"
SERVICE_ACCOUNT_KEY_PATH = 'C:/Users/Georgios Kallos/AppData/Roaming/gcloud/application_default_credentials.json'
SQL_ALCHEMY_URL = f'bigquery://{BIGQUERY_PROJECT}/{BIGQUERY_DATASET}' #?credentials_path={SERVICE_ACCOUNT_KEY_PATH}'
db = SQLDatabase.from_uri(SQL_ALCHEMY_URL)

# engine = create_engine('bigquery://', credentials_path='C:/Users/Georgios Kallos/AppData/Roaming/gcloud/application_default_credentials.json')

# Create a language model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Create the SQL agent
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)