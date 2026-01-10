import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

# --- 1. KEY CONFIGURATION (Live Server Safe) ---
# Streamlit Secrets se key uthayega
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.error("Please add OPENAI_API_KEY to Streamlit Secrets!")
    st.stop()

# --- 2. REST OF THE CODE ---
st.set_page_config(page_title="AI Swarm OS", page_icon="🤖", layout="wide")
st.title("🤖 [PROJECT_BETA]: AGENT_SWARM_OS")

# Tools & LLM
search_tool = DuckDuckGoSearchRun()
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

# Agents Definition
researcher = Agent(
    role='Neural Researcher',
    goal='Uncover deep technical insights',
    backstory="Advanced AI entity for high-speed synthesis.",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

architect = Agent(
    role='System Architect',
    goal='Create technical blueprints',
    backstory="Senior logic engine.",
    llm=llm,
    verbose=True
)

topic = st.text_input("Swarm Objective", value="AI Agents 2026")

if st.button("🚀 Initialize Swarm"):
    with st.status("🛠️ Swarm active: Agents are collaborating...", expanded=True):
        crew = Crew(
            agents=[researcher, architect], 
            tasks=[
                Task(description=f"Research {topic}", agent=researcher, expected_output="5 findings"),
                Task(description=f"Design roadmap for {topic}", agent=architect, expected_output="Markdown roadmap")
            ], 
            process=Process.sequential
        )
        result = crew.kickoff()
    st.markdown(result)
