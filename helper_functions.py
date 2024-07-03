from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import os
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.utils.function_calling import convert_to_openai_function


os.environ["GOOGLE_API_KEY"] = "AIzaSyAgkKi4TKH9xL3N78FWn7SS7yDIz0T4r_4"
genai.configure(api_key="AIzaSyAgkKi4TKH9xL3N78FWn7SS7yDIz0T4r_4")


class Reverse(BaseModel):
    """returns the reverse of a string"""
    string: str 

weather_function = convert_to_openai_function(Reverse)


model = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.3)
model  = model.bind( functions=[Reverse])
prompt = ChatPromptTemplate.from_template(""" {input} """)
output_parser = StrOutputParser()
chain = prompt | model | output_parser
print(chain.invoke({"input": "what is the reverse of Sbaiuodcbdvu"}))

# output_parser = StrOutputParser()
# prompt = """Hey Gemini. Act as OIC Bot and follow the instructions and answer the question accordingly. 
# Chat Instructions:
# 1. Explain the question in 1-2 lines with heading as Question Explaination.
# 2. Explain the potential solution with heading as Potential Solution to it and don't hallucinate.
# General Instructions:
# 1. Ensure that you answer clearly and briefly and only answer from the context strictly.
# 2. While answering the question follow these steps.
# 3. Make sure you explain every question step by step and don't exceed 15 lines.
# Here is the chat history and respond to the user query accordingly.
# chat_history: \n {chat_history}\n
#     Context:\n {context}\n
#     Question: \n{question}?\n

#     Answer:"""
# simple_chain = ChatPromptTemplate.from_template(prompt)
# chain = simple_chain | model | output_parser
# print(chain.invoke({'chat_history':'','context':'connections are ways to connect things','question':'what is connection'}))