# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 21:47:11 2024

@author: jhapr
"""

from langchain_ollama.llms import OllamaLLM
from gnewsclient import gnewsclient

class Agent:
    def __init__(self, role, goal, backstory):
        self.role = role
        self.goal = goal
        self.backstory = backstory

    def perform_task(self, task, context=""):
        prompt = f"""
        Role: {self.role}
        Goal: {self.goal}
        Backstory: {self.backstory}
        
        Task: {task}
        
        Previous Context: {context}
        
        Please complete the task based on your role, goal, and the previous context if provided.
        Show your work step by step.
        """
        model = OllamaLLM(model="llama3.1")
        response = model.invoke(prompt)
        return response

class Task:
    def __init__(self, description, agent):
        self.description = description
        self.agent = agent

class Crew:
    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks

    def kickoff(self):
        context = ""
        results = []
        for task in self.tasks:
            result = task.agent.perform_task(task.description, context)
            results.append(f"Agent {task.agent.role}'s output:\n{result}")
            context = f"\n{result}"
        # return "\n\n".join(results)
        return results[-1]
    
    

def get_new_data(topic="Stock Market",maximum=20):
    client = gnewsclient.NewsClient(language='english', location='India', topic=topic, max_results=maximum)
    data = ''
    news_list = client.get_news()
    for news in news_list: 
        data += f"\n{news['title']}"
        
    return data
        
    

# Initialize agents
summarizer = Agent(
    role='Data Summarizer',
    goal='Summarize the provided data accurately in less than 500 words',
    backstory="You have a keen eye for identifying key points and summarizing large datasets efficiently"
)

interpreter = Agent(
    role='Data Interpreter',
    goal='Interpret the data and provide insights for trading or investment in less than 500 words',
    backstory="You're skilled at analyzing data for trading and investment and extracting meaningful insights from it"
)

planner = Agent(
    role='Financial Advisor',
    goal='Create an actionable plan for trading strategy based on the data and interpreted data',
    backstory="You're experienced in strategic planning and turning insights into action steps"
)


