import streamlit as st
import os
import re
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- 1. CORE CONFIGURATION ---
st.set_page_config(
    page_title="Agent Swarm OS | Enterprise Edition",
    page_icon="💠",
    layout="wide"
)

def apply_custom_styling():
    st.markdown("""
        <style>
        .block-container { padding: 2rem 5rem !important; }
        .report-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 40px;
            color: #1e293b;
            line-height: 1.6;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        }
        .stButton>button {
            background: linear-gradient(90deg, #0f172a 0%, #334155 100%);
            color: white;
            border: none;
            padding: 15px;
            font-weight: 700;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        h1 { font-weight: 800 !important; color: #0f172a !important; }
        </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC & UTILITIES ---
def scan_and_clean(raw_input):
    """Sanitizes AI output for professional presentation."""
    text = str(raw_input)
    text = re.sub(r'```markdown|```', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# --- 3. UI LAYOUT ---
apply_custom_styling()

st.title("💠 Agent Swarm OS")
st.markdown("<p style='color: #64748b; font-size: 1.2rem; margin-top:-15px;'>Autonomous Intelligence Orchestration for Enterprise Objectives</p>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ System Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    model_choice = st.selectbox("Intelligence Core", ["gpt-4o-mini", "gpt-4o"])
    temp = st.slider("Creativity Level", 0.0, 1.0, 0.2)
    
    st.divider()
    st.info("Role: Senior Intelligence Architect\nStatus: Online")

objective = st.text_input("🎯 Define Strategic Objective", placeholder="e.g., Expansion strategy for a FinTech startup in Southeast Asia")

# --- 4. EXECUTION ENGINE ---
if st.button("EXECUTE SYSTEM ARCHITECTURE"):
    if not api_key and "OPENAI_API_KEY" not in os.environ:
        st.error("⚠️ API Key missing. Please provide it in the sidebar.")
    elif not objective:
        st.warning("⚠️ Please define an objective first.")
    else:
        try:
            os.environ["OPENAI_API_KEY"] = api_key if api_key else os.environ.get("OPENAI_API_KEY")
            llm = ChatOpenAI(model_name=model_choice, temperature=temp)

            # Define Agents with distinct personas
            analyst = Agent(
                role='Market Intelligence Lead',
                goal=f'Synthesize 3 high-impact strategic insights for {objective}',
                backstory="Ex-McKinsey Principal specializing in pattern recognition and market disruption.",
                llm=llm,
                verbose=True
            )
            
            architect = Agent(
                role='Operations Strategy Director',
                goal=f'Develop a 12-month tactical roadmap for {objective}',
                backstory="Expert in operational excellence and scaling high-growth ventures.",
                llm=llm,
                verbose=True
            )

            # Tasks with clear expectations
            t1 = Task(
                description=f"Conduct a deep-dive analysis on {objective}. Focus on risks, opportunities, and market positioning.",
                agent=analyst,
                expected_output="3 deep-reasoning insights formatted in Markdown."
            )
            
            t2 = Task(
                description=f"Based on the analyst's findings, create a month-by-month execution roadmap.",
                agent=architect,
                expected_output="A structured 12-month roadmap with KPIs."
            )

            with st.status("🧠 Orchestrating Swarm Intelligence...", expanded=True) as status:
                swarm = Crew(
                    agents=[analyst, architect],
                    tasks=[t1, t2],
                    process=Process.sequential
                )
                raw_result = swarm.kickoff()
                
                # Cleanup
                clean_output = scan_and_clean(raw_result)
                st.session_state['final_report'] = clean_output
                status.update(label="✅ Intelligence Synthesis Complete", state="complete")

        except Exception as e:
            st.error(f"System Error: {str(e)}")

# --- 5. OUTPUT DISPLAY ---
if 'final_report' in st.session_state:
    st.divider()
    cols = st.columns([0.8, 0.2])
    with cols[0]:
        st.subheader("📡 Final Intelligence Report")
    with cols[1]:
        st.download_button("Download Report", st.session_state['final_report'], file_name="intelligence_report.md")

    st.markdown(f'<div class="report-card">{st.session_state["final_report"]}</div>', unsafe_allow_html=True)
