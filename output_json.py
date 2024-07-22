##Agent
from dotenv import load_dotenv
import os
import json

from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool
from datetime import datetime
from pydantic import BaseModel
from tools.tools import *

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






llm = ChatGroq(
    model = "llama3-70b-8192",
    temperature = 0.0,
    api_key = GROQ_API_KEY
)



input_data = input("Enter the data : ")

input = {
    "input_data": input_data
}

"""
class Person(BaseModel):
    name: str
    age: int
"""
# Define the JSON Specialist agent
json_specialist = Agent(
    role='JSON Specialist',
    goal='To process {input_data} and provide output in JSON format.',
    backstory='You have extensive experience in handling various data formats and are proficient in converting data into structured JSON objects. Your expertise ensures accurate and efficient JSON outputs.',
    llm= llm,
    tool = [output_json],
    #response_template= my_response_template,
    #response_template = """<| start_header_id|>assistant<|end_header_id|>
    #{{ .Response }}<|eot_id|>
    #""",
    verbose=True
)

# Define the task for generating JSON output
generate_json_task = Task(
    description='Process the provided {input_data} and generate a structured JSON output. Ensure that the output contains all necessary information and is formatted correctly. The response should only contains JSON',
    expected_output="A JSON object containing the processed data",
    agent=json_specialist,
    #output_json = Person,
    #output = json
)

# Form the crew and kick off the process
crew = Crew(
    agents=[json_specialist],
    tasks=[generate_json_task],
    process=Process.sequential
)

# Kick off the crew
result = crew.kickoff(inputs=input)
print(result)
#print(json.dumps(generate_json_task.json_dict, indent=2))

