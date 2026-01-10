import streamlit as st
import os
import re
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Agent Swarm OS", layout="wide")

if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# --- 2. THE "ZERO-SPACE" CSS ---
st.markdown("""
    <style>
    .block-container { padding: 1rem 3rem !important; }
    .report-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 20px 30px;
        color: #1e293b;
        line-height: 1.5 !important; /* Tight spacing for senior look */
        font-size: 15px;
    }
    /* Eliminating unnecessary margins from markdown elements */
    h1, h2, h3 { margin-bottom: 10px !important; margin-top: 15px !important; }
    p, ul, li { margin-bottom: 6px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BACKEND CLEANING LOGIC ---
def format_output(text):
    """Fazol 'markdown' tags aur spacing ko backend se saaf karne ke liye"""
    clean_text = re.sub(r'```markdown', '', text)
    clean_text = re.sub(r'```', '', clean_text)
    return clean_text.strip()

st.title("🦾 Agent Swarm OS")

# Input
objective = st.text_input("🎯 Define Objective", value="iPhone 16 Pricing Strategy")

if st.button("🚀 EXECUTE NEURAL SWARM"):
    try:
        # High-Logic Backend
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)

        # Agent Setup
        analyst = Agent(role='Researcher', goal=f'Analyze {objective}', backstory="Senior Strategist.", llm=llm)
        architect = Agent(role='Architect', goal=f'Design {objective}', backstory="Systems Expert.", llm=llm)

        # Task Handover
        t1 = Task(description=f"Analyze {objective}.", agent=analyst, expected_output="Key points.")
        t2 = Task(description="Create roadmap.", agent=architect, expected_output="Technical Markdown.")

        # Sequential Execution
        with st.status("🧠 Agents are reasoning...", expanded=False):
            crew = Crew(agents=[analyst, architect], tasks=[t1, t2], process=Process.sequential)
            raw_result = crew.kickoff()
            
            # Backend Cleaning Step
            processed_result = format_output(str(raw_result))

        # --- 4. FINAL OUTPUT ---
        st.subheader("📡 Intelligence Output")
        st.markdown(f'<div class="report-card">{processed_result}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"System Error: {str(e)}")
