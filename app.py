import streamlit as st
import os
import re
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- 1. SENIOR LEVEL ARCHITECTURE ---
st.set_page_config(
    page_title="Agent Swarm OS | Final Masterpiece",
    page_icon="🤖",
    layout="wide"
)

# API Key Security Logic
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# --- 2. FORENSIC UI STYLING (ZERO-GAP) ---
st.markdown("""
    <style>
    /* Remove default Streamlit padding */
    .block-container { padding: 1.5rem 5rem !important; }
    
    /* Professional Report Typography */
    .report-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 30px 45px;
        color: #1e293b;
        line-height: 1.45 !important;
        font-size: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    /* Global Spacing Fixes */
    h1, h2, h3 { margin-top: 12px !important; margin-bottom: 8px !important; color: #0f172a; }
    p, li { margin-bottom: 5px !important; margin-top: 0px !important; }
    ul, ol { margin-top: 5px !important; margin-bottom: 10px !important; }
    
    /* Button & Input Polish */
    .stButton>button { border-radius: 8px; font-weight: 600; background: #0f172a; color: white; border: none; }
    .stTextInput>div>div>input { border-radius: 8px; border: 1px solid #cbd5e1; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BACKEND DATA SANITIZER ---
def sanitize_ai_output(raw_text):
    """
    Forensic cleaning: Removes markdown artifacts, fixes line breaks, 
    and ensures the UI doesn't break.
    """
    text = str(raw_text)
    # 1. Remove raw markdown identifiers found in screenshots
    text = re.sub(r'```markdown', '', text)
    text = re.sub(r'```', '', text)
    # 2. Fix excessive newlines for compact look
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# --- 4. MAIN INTERFACE ---
st.markdown("<h1 style='text-align: center;'>🤖 Agent Swarm OS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; margin-top: -15px;'>Autonomous Multi-Agent Collaboration Engine</p>", unsafe_allow_html=True)
st.divider()

# Input Dashboard
objective = st.text_input("🎯 Define System Objective", placeholder="e.g., Tesla Market Expansion Strategy 2026")

if st.button("🚀 EXECUTE NEURAL SWARM"):
    try:
        # High-Resolution LLM
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)

        # Agent Definition
        analyst = Agent(
            role='Strategic Director',
            goal=f'Deep technical and market analysis for {objective}',
            backstory="Elite strategist with 15+ years experience in identifying market pivot points.",
            llm=llm,
            verbose=True,
            allow_delegation=False # Performance lock
        )

        architect = Agent(
            role='Technical Architect',
            goal=f'Create a high-fidelity execution roadmap for {objective}',
            backstory="Expert in converting complex data into scalable operational blueprints.",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

        # Task Logic
        t1 = Task(description=f"Analyze {objective}. Define 3 core pillars.", agent=analyst, expected_output="3 high-fidelity insights.")
        t2 = Task(description="12-month tactical roadmap.", agent=architect, expected_output="Structured Markdown roadmap.")

        # Swarm Orchestration
        with st.status("🛠️ Deep Scanning & Reasoning...", expanded=True) as status:
            crew = Crew(
                agents=[analyst, architect],
                tasks=[t1, t2],
                process=Process.sequential # Logical Handover
            )
            raw_result = crew.kickoff()
            
            # Backend Sanitization
            final_report = sanitize_ai_output(raw_result)
            status.update(label="✅ Swarm Intelligence Ready", state="complete")

        # --- 5. RENDERED OUTPUT ---
        st.subheader("📡 Intelligence Report")
        with st.container():
            # Perfect spacing wrapper
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.markdown(final_report) 
            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"System Critical Error: {str(e)}")

else:
    st.info("System Ready. Define an objective to initiate autonomous reasoning.")
