from crewai_tools import WebsiteSearchTool 

from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

speech_planner = Agent(
    llm=llm,
    role="Speech Planner",
    goal="Plan well-structured and impactful speeches for bureaucratic meetings on {topic}",
    backstory="You're responsible for structuring speeches that bureaucrats will deliver in both public and private meetings. "
              "You ensure that the speech covers all key points, is aligned with governmental policies, and is tailored to the audience."
              "You research the latest trends, policies, and important information related to {topic}.",
    allow_delegation=False,
    verbose=True
)

speech_writer = Agent(
    llm=llm,
    role="Speech Writer",
    goal="Write compelling and authoritative speeches for bureaucratic meetings on {topic}",
    backstory="You're responsible for crafting speeches that bureaucrats will deliver in different settings. "
              "Your work is based on the structure and research provided by the Speech Planner."
              "You ensure the speech is engaging, persuasive, and clearly communicates key messages."
              "You maintain a formal tone and incorporate relevant data, statistics, and references where needed.",
    allow_delegation=False,
    verbose=True
)

speech_editor = Agent(
    llm=llm,
    role="Speech Editor",
    tools=[web_rag_tool],
    goal="Edit speeches for clarity, effectiveness, and alignment with official communication standards.",
    backstory="You review the speech drafted by the Speech Writer to refine its structure, tone, and impact. "
              "Your job is to ensure the speech maintains professionalism, coherence, and clarity while avoiding controversial statements. "
              "You verify that the speech aligns with government communication policies and diplomatic sensitivities.",
    allow_delegation=False,
    verbose=True
)

plan_speech = Task(
    description=(
        "1. Identify key messages, policy points, and strategic goals relevant to {topic}.",
        "2. Analyze the target audience (public or private meeting) to tailor the speech tone and content accordingly.",
        "3. Develop a clear structure including an introduction, main arguments, supporting evidence, and a strong conclusion.",
        "4. Include references to official reports, statistics, or legal frameworks where applicable."
    ),
    expected_output="A detailed speech plan document including structure, key messages, and supporting references.",
    agent=speech_planner,
)

write_speech = Task(
    description=(
        "1. Craft a compelling speech based on the provided plan, ensuring a formal and engaging tone.",
        "2. Adapt the speech for the specific audience (public or private meeting).",
        "3. Incorporate necessary policy details, statistics, and real-world examples to strengthen key points.",
        "4. Ensure smooth transitions between sections and a strong, memorable closing statement."
    ),
    expected_output="A fully developed speech in markdown format, ready for delivery.",
    agent=speech_writer,
    output_file="speech_output.md"
)

edit_speech = Task(
    description=("Proofread and refine the speech for coherence, impact, and adherence to bureaucratic communication standards."),
    expected_output="A final polished speech in markdown format, ensuring clarity, professionalism, and accuracy.",
    agent=speech_editor
)

crew = Crew(
    agents=[speech_planner, speech_writer, speech_editor],
    tasks=[plan_speech, write_speech, edit_speech],
    verbose=2
)
