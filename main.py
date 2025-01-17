from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_experimental.agents.agent_toolkits import create_csv_agent


# from dotenv import load_dotenv

# load_dotenv()
# os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

os.environ["GOOGLE_API_KEY"] = "AIzaSyCsYPr4TiZEjCTcrOP_Itw3CiIYk7sKykc"
genai.configure(api_key="AIzaSyCsYPr4TiZEjCTcrOP_Itw3CiIYk7sKykc")


def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text



def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """
    Hey Gemini. You are an OIC Bot now and follow the instructions strictly and answer the question accordingly. 
Chat Instructions:
1. The reponse must contain Question Explaination Heading.
2. The reponse must contain Potential Solution Heading.
3. Ensure that you answer clearly and briefly and only answer from the context strictly.
4. While answering the question follow these steps.
5. Make sure you explain every question step by step and don't exceed 15 lines.
6. The reponse must give a brief summary of what you have explained.
7. Reponse must have possible error scenarios or have few Edge cases to consider.
chat_history: \n {chat_history}\n
    Context:\n {context}\n
    Question: \n{question}?\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context","question","chat_history"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain



def user_input(user_question,chat_history):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")

    new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization  = True)
    docs = new_db.similarity_search(user_question)
    retriver = new_db.as_retriever()
    output_docs=  retriver.get_relevant_documents(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents":docs, "question": user_question,"chat_history":chat_history}
        , return_only_outputs=True)

    # print(response)
    return response,output_docs

def response_generator(prompt,chat_history):
    response,output_docs = user_input(prompt,chat_history)
    return response['output_text'],output_docs

############################  DB QUERY CSV ########################
def query_csv_db(csv_files,query):
    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0)
    agent = create_csv_agent(llm=model,path=csv_files,verbose = True,allow_dangerous_code=True)
    result = agent.invoke(query)
    return result

if __name__ == "__main__":
    files = os.listdir(r"C:\Users\Sujith\Downloads\Innovation\OIC_Docs")
    os.chdir(r"C:\Users\Sujith\Downloads\Innovation\OIC_Docs")
    get_vector_store(get_text_chunks(get_pdf_text(files)))
    # chat_history  = ''
    # prompt = "how to add the Google Calendar Adapter Connection to an Integration"
    # response =response_generator(prompt,chat_history)
    # chat_history += f"""User: {prompt}\nBot: {response}\n"""
    # print('\033[95m'+chat_history+'\033[0m')