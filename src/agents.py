from crewai import Crew, Agent, Task, Process
from langchain_community.tools import DuckDuckGoSearchRun
from crewai_tools import tool

class APICrew():

    def __init__(self, api_spec, industry, rules, violations):
        self.api_spec = api_spec
        self.industry = industry
        self.rules = rules
        self.violations = violations

        @tool('DuckDuckGoSearch')
        def search(search_query: str):
            """Search the web for information on a given topic"""
            return DuckDuckGoSearchRun().run(search_query)

        
        self.ingestion_agent = Agent(
        role="Data Science Wizard",
        goal="Take all ingested context data regarding an API and its respective rules and violations and turn it into a highly readable format for a solutions architect to use",
        backstory="You are a highly skilled data cleaning and representation scientist"
        )

        self.solutions_agent = Agent(
        role="Senior Solutions Architect",
        goal="Utilize data regarding an API and its indentified flaws and turn it into possible fixes for the API Spec, with consideration for the industry that the API is deployed in",
        backstory="You are an expert solutions architect that always delivers solution with excellent, thorough context, with possible benefits and trade-offs.",
        tools=[search]
        )

        self.suggestions_agent = Agent(
        role="Principal Suggestions Engineer",
        goal="Turn solutions into procederal, straight forward actionable suggestions that would are well explained and easy followed",
        backstory="You are a distinguished engineer skilled in assisting customers in implementing actionable solutions to their needs"
        )

        self.ingestion_task = Task(
        description=f"""Turn all of the following data about an API into a highly readable format:
        API SPECIFICATION:{api_spec},
        RULES FOR API SPECIFICATION:{rules},
        INDUSTRY IMPLEMENTING THIS API: {industry},
        VIOLATIONS OF THE RULES FOR IMPLEMENTATION: {violations},
        
        MAKE SURE THAT YOU ARE ACTUALLY USING THE DATA AS IT VERY IMPORTANT TO THE END USER!""",
        agent= self.ingestion_agent,
        expected_output='A highly readable report cotaining all of the data related to this API and its status',
        )

        self.solutions_task = Task(
        description=f"Analyze the provided API specification and identified flaws. Develop potential fixes or improvements for the API, taking into account the specific requirements and constraints of the {self.industry} industry. Consider the existing rules and any violations observed, and provide a detailed analysis of the benefits and trade-offs for each proposed solution.",
        agent=self.solutions_agent,
        expected_output="A detailed report outlining the proposed fixes for the API, including a list of potential benefits, trade-offs, and implementation considerations."
        )

        self.suggestions_task = Task(
        description=f"Review the solutions developed by the Senior Solutions Architect for the API flaws. Transform these solutions into clear, procedural, and actionable steps that are easy to understand and implement. Ensure that each step is well explained and provides sufficient context for successful implementation.",
        agent=self.suggestions_agent,
        expected_output="A step-by-step guide with actionable suggestions that detail how to implement the proposed API fixes. Each step should be clear, concise, and include any necessary explanations to ensure ease of execution.")

        self.api_crew = Crew(
            agents=[self.ingestion_agent, self.solutions_agent, self.suggestions_agent],  # Updated to include the correct agents
            tasks=[self.ingestion_task, self.solutions_task, self.suggestions_task],  # Updated to include the correct tasks
            process=Process.sequential,  # Assuming you want the tasks to run sequentially
            full_output=True,
            verbose=True,
        )

    def crew_kickoff(self):
        self.api_crew.kickoff()
        





    
