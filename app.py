import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- 1. SYSTEM CORE CONFIGURATION ---
st.set_page_config(
    page_title="Agent Swarm OS | Professional Edition",
    page_icon="🤖",
    layout="wide"
)

# API Key Management (Security-First)
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    # Testing fallback
    os.environ["OPENAI_API_KEY"] = "sk-proj-PASTE_YOUR_KEY_HERE"

# --- 2. ELITE COMPACT UI (CSS3) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #ffffff; }

    /* Compact Report Container */
    .report-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px 32px;
        margin-top: 10px;
        color: #1e293b;
        line-height: 1.5 !important; /* Compact spacing for professional look */
        word-wrap: break-word;
        white-space: pre-wrap;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    /* Headings Spacing Fix */
    h1, h2, h3 { margin-bottom: 8px !important; margin-top: 15px !important; }
    
    /* Action Button */
    .stButton>button {
        background-color: #0f172a;
        color: white;
        border-radius: 8px;
        padding: 12px;
        font-weight: 600;
        width: 100%;
        transition: 0.2s;
    }
    .stButton>button:hover { background-color: #1e293b; border: none; }

    /* Custom Scrollbar for better UX */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DASHBOARD INTERFACE ---
st.markdown('<h1 style="font-size: 2.2rem; color: #0f172a;">Agent Swarm OS</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; margin-top: -10px;">Production-ready Multi-Agent Orchestration for Technical Intelligence.</p>', unsafe_allow_html=True)

# Input Layout
objective = st.text_input("🎯 Define Swarm Objective", placeholder="e.g., Scalable E-commerce Architecture 2026")

if st.button("🚀 INITIATE NEURAL SWARM"):
    if not os.environ.get("OPENAI_API_KEY") or "PASTE_YOUR_KEY" in os.environ["OPENAI_API_KEY"]:
        st.error("Invalid API Configuration. Please verify environment secrets.")
    else:
        try:
            # High-Reasoning LLM
            llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)

            # Agent 1: The Researcher (Logic First)
            researcher = Agent(
                role='Strategic Technology Analyst',
                goal=f'Perform a deep-dive analysis into {objective}',
                backstory="Ex-Meta Infrastructure Analyst specialized in identifying system bottlenecks and trends.",
                llm=llm,
                verbose=True,
                allow_delegation=False # Performance optimization
            )

            # Agent 2: The Architect (Structural Expert)
            architect = Agent(
                role='Principal Solutions Architect',
                goal=f'Convert analytical insights into a professional 12-month blueprint for {objective}',
                backstory="Senior Architect focused on modular design and high-availability system mapping.",
                llm=llm,
                verbose=True,
                allow_delegation=False
            )

            # Define Sequential Tasks
            t1 = Task(
                description=f"Analyze {objective}. Identify 3 critical architectural pillars and potential risks.",
                agent=researcher,
                expected_output="A structured list of 3 strategic insights."
            )
            t2 = Task(
                description="Draft a 12-month technical roadmap with quarterly milestones.",
                agent=architect,
                expected_output="A comprehensive Markdown roadmap."
            )

            # --- 4. BACKEND ORCHESTRATION ---
            with st.status("🧠 Swarm reasoning in progress...", expanded=True) as status:
                st.write("📡 Phase 1: Strategic Lead is analyzing core objective...")
                
                crew = Crew(
                    agents=[researcher, architect],
                    tasks=[t1, t2],
                    process=Process.sequential # Logical Handover
                )
                
                final_report = crew.kickoff()
                status.update(label="✅ Swarm Intelligence Generated", state="complete")

            # --- 5. OUTPUT DISPLAY ---
            st.markdown("### 📡 Intelligence Report")
            # Text wrapping wrapper
            st.markdown(f'<div class="report-card">{final_report}</div>', unsafe_allow_html=True)
            
            st.caption("Note: This autonomous intelligence was generated using a sequential multi-agent reasoning loop.")

        except Exception as e:
            st.error(f"System Critical Error: {str(e)}")
