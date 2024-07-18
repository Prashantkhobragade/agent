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
        raise ValueError("SERPER API KEYis not found")
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
#Agent
#it will research the topic
researcher_agent = Agent(
    role = "Research Analyst",
    goal = "Provide up-to-date market analysis of the topic {topic}.",
    backstory = "An expert analyst with a keen eye for market trends.",
    tool = [serper_tool],
    llm = llm,
    verbose = True
)

#It will write a article on the topic
writer_agent = Agent(
    role = "Content Writer",
    goal = "Craft engaging blog posts about the topic {topic}",
    backstory = "A skilled writer with a passion for technology.",
    tool = [serper_tool],
    llm = llm,
    verbose = True
)


# Define tasks
research_task = Task(
    description='Research the latest trends in the {topic} and provide a summary.',
    expected_output='A summary of the top 2 trending developments in the {topic} with a unique perspective on their significance.',
    agent=researcher_agent
)

write_task = Task(
    description='Write an engaging micro blog post about the {topic}, based on the research analyst’s summary.',
    expected_output='A 2-paragraph micro blog post formatted in text with engaging, informative, and accessible content, avoiding complex jargon.',
    agent=writer_agent,
    output_file=f'article-posts/{topic}_{timestamp}.txt'  # The final article post will be saved here
)


## Assemble a crew
crew = Crew(
    agents=[researcher_agent, writer_agent],
    tasks=[research_task, write_task],
    verbose=True
)

result = crew.kickoff(inputs={"topic": topic})
