# In imports (Line 5 approx)
from langchain_community.tools import DuckDuckGoSearchRun
# Jab tool initialize karein:
search_tool = DuckDuckGoSearchRun()
import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

# Page Config
st.set_page_config(page_title="AI Swarm OS", page_icon="🤖", layout="wide")

st.title("🤖 [PROJECT_BETA]: AGENT_SWARM_OS")
st.write("Autonomous Multi-Agent Collaboration Engine")

# Sidebar for API Key
with st.sidebar:
    st.header("Configuration")
    # Yahan user apni key daal sakega
    user_key = st.text_input("Enter OpenAI API Key", type="password")
    topic = st.text_input("Research Topic", value="AI Agents in 2026")

if st.button("Initialize Swarm"):
    if not user_key:
        st.error("Please enter your OpenAI API Key!")
    else:
        # Key set karna
        os.environ["OPENAI_API_KEY"] = user_key
        
        # Tools & LLM Initialize
        search_tool = DuckDuckGoSearchRun()
        llm = ChatOpenAI(model_name="gpt-4o", temperature=0.5)

        # Agent 1: Researcher
        researcher = Agent(
            role='Neural Researcher',
            goal=f'Uncover deep technical insights about {topic}',
            backstory="Advanced AI entity designed for high-speed information synthesis.",
            tools=[search_tool], 
            llm=llm, 
            verbose=True
        )

        # Agent 2: Architect
        architect = Agent(
            role='System Architect',
            goal=f'Synthesize research into a technical blueprint for {topic}',
            backstory="Senior logic engine that converts raw data into structured systems.",
            llm=llm, 
            verbose=True
        )

        # Tasks
        t1 = Task(description=f"Research latest trends in {topic}.", agent=researcher, expected_output="List of 5 technical insights.")
        t2 = Task(description=f"Create a technical roadmap based on research.", agent=architect, expected_output="A structured Markdown roadmap.")

        # Execution
        with st.status("🚀 Swarm in progress...", expanded=True) as status:
            st.write("Agents are collaborating...")
            crew = Crew(agents=[researcher, architect], tasks=[t1, t2], process=Process.sequential)
            result = crew.kickoff()
            status.update(label="✅ Swarm Tasks Completed!", state="complete")

        # Result Display
        st.subheader("Final Output")
        st.markdown(result)

