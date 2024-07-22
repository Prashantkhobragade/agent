##Agent
from dotenv import load_dotenv
import os

from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool
from datetime import datetime

# Get the current timestamp
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')


load_dotenv()

#Groq API key
try:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("Groq api key is not found")
except:
    print("Error: Groq API key is not found")


#Serper API Key
try:
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    if not SERPER_API_KEY:
        raise ValueError("SERPER API KEY is not found")
except:
    print("Error: Serper API key is not found")



llm = ChatGroq(
    model = "llama3-70b-8192",
    temperature = 0.0,
    api_key = GROQ_API_KEY
)


#Tools
serper_tool = SerperDevTool()

topic:str = input("Enter the topic: ")
