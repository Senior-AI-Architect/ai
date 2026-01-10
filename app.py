import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- 1. CONFIGURATION ---
# Aapne kaha ke key andar hi hai, isliye yahan direct define kar di hai
os.environ["OPENAI_API_KEY"] = "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Apni asli key yahan lazmi check karein

st.set_page_config(page_title="AI Swarm OS", page_icon="🤖", layout="wide")

# UI Styling
st.markdown("""
    <style>
    .main { background-color: #050b14; color: #00f2ff; }
    .stButton>button { width: 100%; background: linear-gradient(45deg, #0891b2, #06b6d4); color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 [PROJECT_BETA]: AGENT_SWARM_OS")
st.write("Autonomous Multi-Agent Collaboration Engine")

# --- 2. INPUT ---
topic = st.text_input("Enter Swarm Objective", value="Next-Gen AI Agentic Workflows 2026")

if st.button("🚀 Initialize Swarm"):
    try:
        # LLM Setup (GPT-4o-mini for extreme speed)
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

        # Agent 1: Neural Researcher
        researcher = Agent(
            role='Neural Research Analyst',
            goal=f'Analyze the most critical breakthroughs in {topic}',
            backstory="You are an elite AI analyst. You don't need the web; you have a massive internal database of technical knowledge.",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

        # Agent 2: System Architect
        architect = Agent(
            role='System Architect',
            goal=f'Design a professional technical roadmap for {topic}',
            backstory="You take complex analysis and turn it into actionable, world-class system designs.",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

        # --- 3. TASKS ---
        research_task = Task(
            description=f"Identify top 5 technical trends in {topic}. Focus on scalability.",
            expected_output="A list of 5 deeply technical insights.",
            agent=researcher
        )

        design_task = Task(
            description=f"Based on research, create a high-level architecture and a 6-month execution roadmap.",
            expected_output="A structured Markdown report with 'Architecture' and 'Roadmap' sections.",
            agent=architect
        )

        # --- 4. EXECUTION ---
        with st.status("🛠️ Swarm active: Agents are collaborating...", expanded=True) as status:
            st.write("📡 Neural Researcher is analyzing patterns...")
            crew = Crew(
                agents=[researcher, architect],
                tasks=[research_task, design_task],
                process=Process.sequential
            )
            result = crew.kickoff()
            status.update(label="✅ Swarm Intelligence Ready!", state="complete")

        # --- 5. OUTPUT ---
        st.divider()
        st.subheader("📊 Final Intelligence Output")
        st.markdown(result)
        
    except Exception as e:
        st.error(f"System Error: {str(e)}")
