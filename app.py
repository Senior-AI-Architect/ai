import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Agent Swarm OS",
    page_icon="🦾",
    layout="wide" # Readable width ke liye
)

# API Key Management (Secrets se connect karein ya yahan paste karein)
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    os.environ["OPENAI_API_KEY"] = "sk-proj-YOUR_ACTUAL_KEY_HERE"

# --- 2. CLEAN & READABLE UI STYLING ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #f8fafc; color: #1e293b; }
    
    /* Readable Content Container */
    .report-box {
        background-color: white;
        padding: 40px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        line-height: 1.8;
        font-size: 16px;
        color: #334155;
        word-wrap: break-word;
        white-space: pre-wrap;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: #0f172a;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #334155; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦾 [PROJECT_BETA]: AGENT_SWARM_OS")
st.caption("Autonomous Collaboration of Strategy and Architecture Agents")
st.write("---")

# --- 3. INPUT SECTION ---
topic = st.text_input("Define Objective:", value="AI Agents Efficiency 2026")

if st.button("🚀 Run Swarm Collaboration"):
    try:
        # LLM Initialization (Fast & High Logic)
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3)

        # Agent 1: The Analyst (Specialized Research)
        analyst = Agent(
            role='Principal Technical Analyst',
            goal=f'Define core technical breakthroughs for {topic}',
            backstory="Expert in identifying high-impact patterns and system bottlenecks.",
            llm=llm,
            verbose=True,
            allow_delegation=False # Performance boost
        )

        # Agent 2: The Architect (System Design)
        architect = Agent(
            role='Lead Systems Architect',
            goal=f'Design a 6-month technical roadmap for {topic}',
            backstory="Senior architect focused on scalability and modular design principles.",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

        # Tasks
        t1 = Task(description=f"Identify 3 key innovations in {topic}.", agent=analyst, expected_output="3 detailed technical insights.")
        t2 = Task(description="Create a technical roadmap with milestones.", agent=architect, expected_output="Markdown formatted roadmap.")

        # Swarm Orchestration
        with st.status("🛠️ Swarm Active: Reasoning...", expanded=True) as status:
            crew = Crew(
                agents=[analyst, architect], 
                tasks=[t1, t2], 
                process=Process.sequential # Logical handoff
            )
            result = crew.kickoff()
            status.update(label="✅ Analysis Complete", state="complete")

        # --- 4. READABLE OUTPUT ---
        st.subheader("📡 Final System Intelligence Report")
        # Wrapper box for perfect readability
        st.markdown(f'<div class="report-box">{result}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error during orchestration: {str(e)}")

else:
    st.info("System Ready. Enter an objective above to trigger the autonomous agents.")
