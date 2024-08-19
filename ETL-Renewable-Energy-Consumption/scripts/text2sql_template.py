import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

# Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = "Your OpenAI API Key"

# Database connection details
host = "localhost"
user = "root"
password = "Your MySQL Password"
database = "SalesOrderSchema"

# Setup database connection
db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
db = SQLDatabase.from_uri(db_uri)
llm = ChatOpenAI(model="gpt-4", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

# Streamlit app layout
st.title('SQL Chatbot')

# User input
user_query = st.text_area("Enter your SQL-related query:", "List Top 10 Employees by Salary?")

if st.button('Submit'):
    #try:
        # Processing user input
        #response = agent_executor.invoke(user_query)
        #response = agent_executor.invoke({"query": user_query})
        #if st.button('Submit'):
    try:
        # Processing user input
        response = agent_executor.invoke({
            "agent_scratchpad": "",  # Assuming this needs to be an empty string if not used
            "input": user_query  # Changed from "query" to "input"
        })
        st.write("Response:")
        st.json(response)  # Use st.json to pretty print the response if it's a JSON
    except Exception as e:
        st.error(f"An error occurred: {e}")

        #st.write("Response:")
        #st.write(response)
    #except Exception as e:
        #st.error(f"An error occurred: {e}")
