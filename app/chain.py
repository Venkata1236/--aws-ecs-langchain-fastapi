from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from app.config import OPENAI_API_KEY

def get_chain():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=OPENAI_API_KEY,
        temperature=0.7
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Answer clearly and concisely."),
        ("human", "{question}")
    ])

    chain = prompt | llm | StrOutputParser()
    return chain