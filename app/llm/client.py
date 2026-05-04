# app/llm/client.py
from langchain_mistralai import ChatMistralAI
from .pathloader import  load_prompt
from .schemas import StructuredOutput
from fastapi import HTTPException
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
load_dotenv()


def get_llm_chain(provider: str):
    raw_prompt = load_prompt('analyze_v1')
    prompt = ChatPromptTemplate.from_template(raw_prompt)
    if provider.lower() == "mistral":
        llm = ChatMistralAI(model="mistral-small-latest")
    elif provider.lower() == 'groq':
        llm = ChatGroq(model="llama-3.1-8b-instant")
       
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider}")
    return prompt | llm.with_structured_output(StructuredOutput)