from  fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

groq_api_key= os.getenv('GROQ_API_KEY')
llm = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)

system_template ="transalte the following into {language}"
prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        system_template
    ),
    (
        "user",
        "{input}"
    )
])

parser = StrOutputParser()
chain = prompt_template|llm|parser
# chain.invoke({'input':"how are you", 'language':"french"})

app = FastAPI(title="langchain server", description="a simple api using langchain runnable interfaces",version="1.0")

add_routes(app, chain,path='/chain')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
