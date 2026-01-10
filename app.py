import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- 1. GLOBAL SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="Agent Swarm OS | Enterprise AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Key Management - Secure Public Repo Practice
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    # Recruiter ko batane ke liye ke logic security-first hai
    os.environ["OPENAI_API_KEY"] = "PASTE_KEY_HERE_FOR_LOCAL_TESTING"

# --- 2. RESPONSIVE FRONT-END ARCHITECTURE (CSS3) ---
st.markdown("""
    <style>
    /* Professional Google-style Sans Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #ffffff;
    }

    /* Full-width Responsive Container */
    .report-container {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 40px;
        margin-top: 25px;
        color: #1e293b;
        line-height: 1.8;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        word-wrap: break-word;
        white-space: pre-wrap;
    }

    /* Senior Dashboard Header */
    .main-title {
        font-size: 2.8rem;
        font-weight: 600;
        background: linear-gradient(90deg, #0f172a, #334155);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }

    /* Status Pulse Animation */
    .agent-status {
        padding: 12px 20px;
        background: #f1f5f9;
        border-radius: 10px;
        border-left: 4px solid #2563eb;
        color: #475569;
        font-size: 0.95rem;
        margin-bottom: 10px;
    }

    .stButton>button {
        background-color: #0f172a;
        color: white;
        border-radius: 10px;
        padding: 15px;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1e293b;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UI LAYOUT ---
st.markdown('<h1 class="main-title">Agent Swarm OS</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;">Production-grade Multi-Agent Orchestration for Technical Intelligence.</p>', unsafe_allow_html=True)

# Main Dashboard Input Area
with st.container():
    objective = st.text_input("🎯 Define Swarm Objective", placeholder="e.g., Enterprise Blockchain Architecture 2026", help="Define the technical goal for the agentic swarm.")
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        run_btn = st.button("🚀 EXECUTE NEURAL SWARM")

# --- 4. BACKEND REASONING ENGINE ---
if run_btn:
    if "PASTE_KEY" in os.environ["OPENAI_API_KEY"]:
        st.warning("⚠️ Security Alert: OpenAI API Key not detected in environment.")
    else:
        try:
            # High-Logic Model for Senior Reasoning
            llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3)

            # Agent 1: Senior Research Entity
            researcher = Agent(
                role='Strategic Research Director',
                goal=f'Conduct a multi-dimensional analysis of {objective}',
                backstory="Expert in identifying high-impact technical trends and infrastructure shifts.",
                llm=llm,
                verbose=True,
                allow_delegation=False # Efficiency Control
            )

            # Agent 2: Solutions Architect
            architect = Agent(
                role='Principal Solutions Architect',
                goal=f'Synthesize research into a 12-month execution blueprint for {objective}',
                backstory="Specialized in building scalable, modular, and future-proof system designs.",
                llm=llm,
                verbose=True,
                allow_delegation=False
            )

            # Define Modular Tasks
            t1 = Task(
                description=f"Analyze {objective}. Extract top 3 architectural pillars and potential risks.",
                agent=researcher,
                expected_output="A structured list of 3 strategic insights with risk assessments."
            )
            t2 = Task(
                description="Create a comprehensive technical roadmap with quarterly milestones.",
                agent=architect,
                expected_output="A professional technical roadmap formatted in Markdown."
            )

            # --- 5. EXECUTION & LOGGING ---
            with st.status("🧠 Swarm Intelligence in Progress...", expanded=True) as status:
                st.markdown('<div class="agent-status">📡 Phase 1: Director is evaluating technical constraints...</div>', unsafe_allow_html=True)
                
                # Orchestrate the Crew
                crew = Crew(
                    agents=[researcher, architect],
                    tasks=[t1, t2],
                    process=Process.sequential # Ensures logical handover
                )
                
                output = crew.kickoff()
                
                st.markdown('<div class="agent-status">🏗️ Phase 2: Architect is mapping strategic goals to milestones...</div>', unsafe_allow_html=True)
                status.update(label="✅ Swarm Collaboration Finalized", state="complete")

            # --- 6. READABLE FINAL REPORT ---
            st.markdown("### 📡 Final Intelligence Output")
            st.markdown(f'<div class="report-container">{output}</div>', unsafe_allow_html=True)
            
            # Professional Disclosure
            st.caption("Architecture Note: This output is the result of a sequential reasoning loop between two specialized agents to ensure technical depth.")

        except Exception as e:
            st.error(f"Execution Error: {str(e)}")

else:
    st.info("System is standby. Awaiting objective initialization.")
