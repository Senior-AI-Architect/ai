import streamlit as st
import os
import time
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- 1. SYSTEM SETTINGS ---
st.set_page_config(
    page_title="Agent Swarm OS | Enterprise Edition",
    page_icon="🧠",
    layout="wide"
)

# Professional Key Management
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    # Manual key input for testing (Only if secrets not set)
    os.environ["OPENAI_API_KEY"] = "sk-proj-YOUR_KEY_HERE"

# --- 2. ELITE MINIMALIST UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #ffffff; }
    
    .main-header { font-size: 2.5rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.1rem; color: #64748b; margin-bottom: 2rem; }
    
    /* Elegant Report Container */
    .report-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 35px;
        margin-top: 20px;
        color: #1e293b;
        line-height: 1.8;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Status Box */
    .status-box {
        background-color: #f1f5f9;
        border-left: 4px solid #3b82f6;
        padding: 15px;
        margin: 10px 0;
        font-size: 0.9rem;
        color: #475569;
    }
    
    .stButton>button {
        background-color: #0f172a;
        color: white;
        border-radius: 6px;
        padding: 0.6rem 2rem;
        font-weight: 500;
        border: none;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown('<p class="main-header">🦾 Agent Swarm OS</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Multi-Agent Orchestration for Enterprise-Grade Technical Roadmaps</p>', unsafe_allow_html=True)

# --- 4. INPUT SECTION ---
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        objective = st.text_input("System Objective", value="Next-Gen Fintech Security Architecture 2026")
    with col2:
        st.write("##") # Spacer
        run_button = st.button("Initialize Swarm")

# --- 5. EXECUTION ---
if run_button:
    if not os.environ.get("OPENAI_API_KEY"):
        st.error("Missing API Credentials")
    else:
        try:
            # High-Speed Reasoning Model
            llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)

            # Define Agents with High-Level Personas
            analyst = Agent(
                role='Strategic Research Lead',
                goal=f'Extract 3 disruptive technical shifts for {objective}',
                backstory="Ex-Gartner analyst specialized in emerging tech infrastructure.",
                llm=llm,
                verbose=True,
                allow_delegation=False
            )

            architect = Agent(
                role='Senior Systems Architect',
                goal=f'Design a scalable blueprint based on research for {objective}',
                backstory="Specialist in modular cloud-native architectures and long-term roadmaps.",
                llm=llm,
                verbose=True,
                allow_delegation=False
            )

            # Tasks with Explicit Expectations
            t1 = Task(
                description=f"Analyze {objective} and identify 3 critical trends.",
                agent=analyst,
                expected_output="Detailed list of 3 technical insights."
            )
            t2 = Task(
                description="Create a structured 12-month roadmap with architecture milestones.",
                agent=architect,
                expected_output="Professional Markdown technical roadmap."
            )

            # Execution with "Thought Logs"
            with st.status("🛠️ System Reasoning in Progress...", expanded=True) as status:
                st.markdown('<div class="status-box">📡 Phase 1: Strategic Lead is analyzing core objective...</div>', unsafe_allow_html=True)
                
                # Crew Setup
                swarm = Crew(
                    agents=[analyst, architect],
                    tasks=[t1, t2],
                    process=Process.sequential # Ensures logical reasoning flow
                )
                
                result = swarm.kickoff()
                
                st.markdown('<div class="status-box">🏗️ Phase 2: Architect is aligning findings with system design...</div>', unsafe_allow_html=True)
                status.update(label="✅ Swarm Intelligence Generated", state="complete")

            # --- 6. READABLE FINAL OUTPUT ---
            st.divider()
            st.markdown("### 📡 Final Intelligence Report")
            st.markdown(f'<div class="report-card">{result}</div>', unsafe_allow_html=True)
            
            # Recruiter Tip: Mentioning why it took time
            st.caption("Note: This autonomous report was generated through a sequential reasoning loop between two specialized AI agents.")

        except Exception as e:
            st.error(f"System Orchestration Error: {str(e)}")

else:
    st.info("The system is currently idle. Define an objective to begin autonomous collaboration.")
