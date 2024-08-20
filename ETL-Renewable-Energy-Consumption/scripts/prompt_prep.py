from langchain_core.prompts import PromptTemplate

def define_prompt():
    template = '''Given an input question, first create a syntactically correct {dialect} query to run, then look at the first {top_k} results of the query. 
    Return the SQL query to run in the database without the {dialect} prefix

    Only use the following tables:

    {table_info}.

    Question: {input}'''

    prompt = PromptTemplate.from_template(template)

    return prompt
