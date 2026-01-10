import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- 1. PAGE CONFIGURATION (FULL WIDTH) ---
st.set_page_config(
    page_title="AI Swarm OS", 
    page_icon="🤖", 
    layout="wide", # Isse text ko poori jagah milegi
    initial_sidebar_state="collapsed"
)

# Key Management (Streamlit Cloud Secrets use karein ya yahan paste karein)
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    # Testing ke liye agar key code mein dalni ho:
    os.environ["OPENAI_API_KEY"] = "sk-proj-YOUR_ACTUAL_KEY_HERE"

# --- 2. SUPER-FAST UI STYLING ---
st.markdown("""
    <style>
    /* Full Width Fix */
    .block-container {
        max-width: 98% !important;
        padding-top: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    /* Text Wrap Fix taake adha nazar na aaye */
    .report-box {
        background-color: #050b14;
        color: #e6f1ff;
        padding: 25px;
        border-radius: 12px;
        border: 1px dashed #00f2ff;
        line-height: 1.6;
        word-wrap: break-word;
        white-space: pre-wrap;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #0891b2, #06b6d4);
        color: white;
        border: none;
        padding: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 [PROJECT_BETA]: AGENT_SWARM_OS")
st.write("---")

# --- 3. INPUT ---
topic = st.text_input("SYSTEM OBJECTIVE:", value="AI Agents Efficiency 2026")

if st.button("🚀 EXECUTE SWARM"):
    try:
        # GPT-4o-mini extreme speed ke liye best hai
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

        # Agent 1: Fast Analyst
        analyst = Agent(
            role='Neural Analyst',
            goal=f'Summarize core breakthroughs for {topic}',
            backstory="High-speed data synthesis engine.",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

        # Agent 2: Precision Architect
        architect = Agent(
            role='System Architect',
            goal=f'Create a technical roadmap for {topic}',
            backstory="Master of system logical structures.",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

        # Tasks
        t1 = Task(description=f"Quick 3 insights for {topic}.", agent=analyst, expected_output="3 bullet points.")
        t2 = Task(description="Brief 6-month roadmap.", agent=architect, expected_output="Markdown roadmap.")

        # Swarm Execution
        with st.status("⚡ COLLABORATING (STAY TUNED)...", expanded=True) as status:
            swarm = Crew(
                agents=[analyst, architect], 
                tasks=[t1, t2], 
                process=Process.sequential
            )
            result = swarm.kickoff()
            status.update(label="✅ TASK COMPLETED!", state="complete")

        # --- 4. OUTPUT (WRAPPER TO PREVENT TEXT CUTTING) ---
        st.subheader("📡 AGENT OUTPUT REPORT:")
        st.markdown(f'<div class="report-box">{result}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ SYSTEM ERROR: {str(e)}")
