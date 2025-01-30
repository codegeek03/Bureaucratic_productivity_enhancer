from crewai_tools import WebsiteSearchTool

from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import TavilySearchResults
from langchain_core.tools import BaseTool
from pydantic import Field


load_dotenv()
llm = ChatGroq(
    model="groq/llama3-70b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=True
)

class SearchTool(BaseTool):
    name: str = "Search"
    description: str = "Useful for search-based queries. Use this to find current information about policies, regulatory frameworks, and institutional developments."
    search: TavilySearchResults = Field(
        default_factory=lambda: TavilySearchResults(
            max_results=5,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True,
            include_images=True,
        )
    )

    def _run(self, query: str) -> str:
        """Execute the search query using Tavily and return results."""
        try:
            return self.search.run(query)
        except Exception as e:
            return f"Error performing search: {str(e)}"


planner = Agent(
    role="Policy Speech Planner",
    goal="Develop a structured and informative speech on {topic} for a formal meeting or conference.",
    backstory="You are responsible for structuring a speech on {topic} that aligns with institutional objectives and policy frameworks."
              "Your role is to ensure that the speech effectively conveys key messages to stakeholders,"
              "includes relevant data, and maintains an authoritative and diplomatic tone.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    role="Speech Writer",
    goal="Compose a well-structured and impactful speech on {topic}, ensuring clarity, authority, and alignment with institutional messaging.",
    backstory="Your task is to craft a speech on {topic} that reflects official positions, policy direction, and key strategic considerations."
              "The speech should be articulate, fact-based, and designed to engage the audience while maintaining formal rigor.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

editor = Agent(
    role="Speech Editor",
    goal="Refine the speech to enhance clarity, coherence, and alignment with bureaucratic and institutional standards.",
    backstory="You are responsible for reviewing the speech to ensure it adheres to formal conventions, maintains neutrality,"
              "and appropriately balances rhetorical strength with factual accuracy. The speech should reflect professionalism"
              "and diplomatic finesse while conveying strategic intent effectively.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

plan = Task(
    description=(
        "1. Identify key themes, objectives, and messages relevant to {topic} in a formal setting.\n"
        "2. Outline key policy considerations, historical context, and institutional perspectives.\n"
        "3. Develop a structured speech framework, including an introduction, main body, and closing remarks.\n"
        "4. Ensure the outline includes references to regulatory frameworks, international best practices, or relevant precedents."
    ),
    expected_output="A structured speech plan document including key themes, objectives, and references to institutional or policy considerations.",
    agent=planner,
)

write = Task(
    description=(
        "1. Draft a comprehensive and persuasive speech on {topic} based on the provided speech plan.\n"
        "2. Use formal and diplomatic language, ensuring clarity, coherence, and authority.\n"
        "3. Incorporate relevant data, statistics, and policy references where applicable.\n"
        "4. Structure the speech with a strong opening, logical flow, and compelling conclusion.\n"
        "5. Ensure alignment with institutional messaging, avoiding unnecessary controversy."
    ),
    expected_output="A fully written speech document in formal bureaucratic style, ready for delivery at a meeting or conference.",
    agent=writer
)

edit = Task(
    description=("Refine the speech to ensure grammatical precision, clarity, and alignment with official discourse norms.\n"
                 "Review for consistency in tone, accuracy in policy references, and overall impact."),
    expected_output="A polished speech document, refined for clarity, coherence, and professional delivery.",
    agent=editor
)



def inference(query):
    crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit]
)
    
    web_research_results = tool.invoke(query)
    
    prompt = query + "\n"
    
    prompt += web_research_results[0]['content']
    prompt += "\n"
    prompt += web_research_results[1]['content']
    result = crew.kickoff(inputs={"topic": prompt})

    return result


if __name__ == "__main__":
    query = "Shamik Bhattacharya IIT KGP"
    response = inference(query)
    
    print(response)