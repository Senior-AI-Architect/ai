import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="AI Swarm OS", page_icon="🤖", layout="wide")

# UI Design
st.markdown("""
    <style>
    .main { background-color: #050b14; color: #00f2ff; font-family: 'monospace'; }
    .stButton>button { width: 100%; background: #0891b2; color: white; border-radius: 5px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# Key Management (Streamlit Cloud Secrets)
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.error("❌ API Key Missing: Please add 'OPENAI_API_KEY' in Streamlit Cloud Secrets.")
    st.stop()

st.title("🤖 [PROJECT_BETA]: AGENT_SWARM_OS")
st.write("---")

# Input
topic = st.text_input("SYSTEM OBJECTIVE:", value="AI Agents Efficiency 2026")

if st.button("EXECUTE SWARM"):
    try:
        # LLM Initialization (Fastest Model)
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

        # Specialized Agents
        analyst = Agent(
            role='Neural Analyst',
            goal=f'Define core breakthroughs for {topic}',
            backstory="Deep-level AI research entity.",
            llm=llm, verbose=True
        )

        architect = Agent(
            role='System Architect',
            goal=f'Design a roadmap for {topic}',
            backstory="Senior technical logic engine.",
            llm=llm, verbose=True
        )

        # Tasks
        t1 = Task(description=f"Identify 3 key trends in {topic}.", agent=analyst, expected_output="List of 3 insights.")
        t2 = Task(description="Build a high-level technical roadmap.", agent=architect, expected_output="Markdown Roadmap.")

        # Swarm Execution
        with st.status("🚀 COLLABORATING...", expanded=True) as status:
            swarm = Crew(agents=[analyst, architect], tasks=[t1, t2], process=Process.sequential)
            result = swarm.kickoff()
            status.update(label="✅ EXECUTION COMPLETE", state="complete")

        st.subheader("📡 AGENT OUTPUT REPORT:")
        st.markdown(result)

    except Exception as e:
        st.error(f"❌ SYSTEM ERROR: {str(e)}")
