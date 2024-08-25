from langchain_core.prompts import PromptTemplate

def define_prompt():
    template = '''Given an input question, first create a syntactically correct SQLite query to run that returns the top {top_k} results.  
    
    Only use the following tables:

    {table_info}.

    Question: {input}'''

    prompt = PromptTemplate.from_template(template)

    return prompt
