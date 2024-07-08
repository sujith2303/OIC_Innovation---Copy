from langchain_experimental.agents.agent_toolkits import create_csv_agent
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import os


os.environ["GOOGLE_API_KEY"] = "AIzaSyCsYPr4TiZEjCTcrOP_Itw3CiIYk7sKykc"
genai.configure(api_key="AIzaSyCsYPr4TiZEjCTcrOP_Itw3CiIYk7sKykc")

model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0)
agent = create_csv_agent(llm=model,path='Training.csv',verbose = True,allow_dangerous_code=True,)
result = agent.invoke('Return the training No and Trainer name where the start date is May')
print(result['output'])
# print(agent.invoke('I need to get the training number and training start and end date for the records which are present or null and the trainer is prefixed with ank and the startday is a weekday and training_no is divisble by 10'))