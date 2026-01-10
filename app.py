import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- CONFIGURATION ---
# Apni BILKUL SAHI key yahan single quotes ke andar paste karein
os.environ["OPENAI_API_KEY"] = "PASTE_YOUR_CORRECT_KEY_HERE"

st.set_page_config(page_title="AI Swarm OS", page_icon="🤖", layout="wide")

# Futuristic UI
st.markdown("""
    <style>
    .main { background-color: #050b14; color: #00f2ff; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input { background-color: #0a192f; color: #00f2ff; border: 1px solid #00f2ff; }
    .stButton>button { background: linear-gradient(45deg, #0891b2, #06b6d4); color: white; font-weight: bold; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 [PROJECT_BETA]: AGENT_SWARM_OS")
st.write("---")

# Input Objective
topic = st.text_input("ENTER SYSTEM OBJECTIVE:", value="Advanced Multi-Agent Collaboration 2026")

if st.button("EXECUTE SWARM"):
    try:
        # GPT-4o-mini extreme speed ke liye
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

        # AGENTS (Using internal knowledge for speed)
        researcher = Agent(
            role='Neural Analyst',
            goal=f'Analyze {topic} trends',
            backstory="Elite data intelligence entity.",
            llm=llm,
            verbose=True
        )

        architect = Agent(
            role='System Designer',
            goal=f'Create blueprint for {topic}',
            backstory="Master of technical architecture.",
            llm=llm,
            verbose=True
        )

        # TASKS
        t1 = Task(description=f"Identify 3 breakthroughs in {topic}.", agent=researcher, expected_output="3 bullet points.")
        t2 = Task(description="Create a technical roadmap.", agent=architect, expected_output="Markdown roadmap.")

        # EXECUTION
        with st.status("🚀 SWARM ACTIVE: COLLABORATING...", expanded=True) as status:
            crew = Crew(agents=[researcher, architect], tasks=[t1, t2], process=Process.sequential)
            result = crew.kickoff()
            status.update(label="✅ TASK COMPLETED!", state="complete")

        st.subheader("📡 FINAL INTELLIGENCE REPORT:")
        st.markdown(result)

    except Exception as e:
        st.error(f"❌ SYSTEM CRITICAL ERROR: {str(e)}")
