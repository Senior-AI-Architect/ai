import streamlit as st
import os
import re
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- 1. CORE ARCHITECTURE ---
st.set_page_config(
    page_title="Agent Swarm OS | Atomic Edition",
    page_icon="🤖",
    layout="wide"
)

# Secure API Management
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# --- 2. FORENSIC UI STYLING (THE PERFECT LOOK) ---
st.markdown("""
    <style>
    /* Spacing & Width Optimization */
    .block-container { padding: 1rem 5rem !important; }
    
    /* Elegant Report Card */
    .report-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 30px 45px;
        color: #1e293b;
        line-height: 1.5 !important;
        font-size: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
    }
    
    /* Deep Spacing Fixes */
    h1, h2, h3 { margin-bottom: 8px !important; margin-top: 15px !important; color: #0f172a; }
    p, li { margin-bottom: 4px !important; }
    
    /* Button Style */
    .stButton>button {
        background: #0f172a;
        color: white;
        border-radius: 8px;
        padding: 12px;
        width: 100%;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BACKEND DATA CLEANER ---
def scan_and_clean(raw_input):
    """Deep cleaning of AI artifacts and excessive spacing"""
    text = str(raw_input)
    # Remove markdown block headers
    text = re.sub(r'```markdown', '', text)
    text = re.sub(r'```', '', text)
    # Fix spacing issues
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# --- 4. INTERFACE ---
st.title("🤖 Agent Swarm OS")
st.markdown("<p style='color: #64748b; margin-top:-15px;'> Autonomous Orchestration</p>", unsafe_allow_html=True)

objective = st.text_input("🎯 Define Objective", placeholder="Swarm search ")

if st.button("EXECUTE SYSTEM"):
    try:
        # Senior Level LLM Config
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)

        # Agent Personas
        analyst = Agent(
            role='Market Intelligence Lead',
            goal=f'Analyze {objective} for 3 critical insights',
            backstory="Senior Analyst at top consulting firm, specialized in data synthesis.",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
        
        architect = Agent(
            role='Operational Architect',
            goal=f'Draft a 12-month execution plan for {objective}',
            backstory="Execution expert who turns data into structured roadmaps.",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

        # Scanned Tasks
        t1 = Task(description=f"Analyze {objective}.", agent=analyst, expected_output="3 high-fidelity insights.")
        t2 = Task(description="Build execution roadmap.", agent=architect, expected_output="Markdown formatted roadmap.")

        # Atomic Execution
        with st.status("🧠 Deep Reasoning...", expanded=True) as status:
            swarm = Crew(
                agents=[analyst, architect],
                tasks=[t1, t2],
                process=Process.sequential # Data flow integrity
            )
            raw_result = swarm.kickoff()
            
            # Sanitization
            clean_output = scan_and_clean(raw_result)
            status.update(label="✅ Scanned Intelligence Ready", state="complete")

        # --- 5. OUTPUT ---
        st.subheader("📡 Intelligence Report")
        with st.container():
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.markdown(clean_output)
            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Scan Error: {str(e)}")

