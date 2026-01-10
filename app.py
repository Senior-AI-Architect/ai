import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="AI Swarm OS | Senior AI Project", 
    page_icon="🦾", 
    layout="wide"
)

# Key Management - Professional approach using Secrets
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    # Fallback for local testing
    os.environ["OPENAI_API_KEY"] = "sk-proj-YOUR_API_KEY"

# --- 2. ADVANCED UI STYLING (Senior UI/UX) ---
st.markdown("""
    <style>
    .report-container {
        background-color: #0d1117;
        padding: 30px;
        border-radius: 15px;
        border-left: 5px solid #00f2ff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #c9d1d9;
        line-height: 1.8;
    }
    .stTextInput>div>div>input {
        background-color: #161b22;
        color: #58a6ff;
        border: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MAIN INTERFACE ---
st.title("🦾 [PROJECT_BETA]: AGENT_SWARM_OS")
st.subheader("Autonomous Orchestration of Specialized AI Agents")
st.write("---")

# User Input for Objective
objective = st.text_input("🎯 DEFINE SYSTEM OBJECTIVE:", placeholder="e.g., Scalable Microservices Architecture 2026")

if st.button("🚀 INITIATE COLLABORATION"):
    if not os.environ.get("OPENAI_API_KEY") or "YOUR_API_KEY" in os.environ["OPENAI_API_KEY"]:
        st.error("❌ CRITICAL: OpenAI API Key is missing or invalid.")
    else:
        try:
            # Initialize LLM - GPT-4o-mini for speed and high logic
            llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3)

            # AGENT 1: The Domain Specialist (Focused Intelligence)
            analyst = Agent(
                role='Principal Strategy Analyst',
                goal=f'Synthesize high-level technical requirements for {objective}',
                backstory="Senior technical strategist with 20 years of experience in system forecasting.",
                llm=llm,
                verbose=True,
                allow_delegation=False # Performance optimization: prevents unnecessary loops
            )

            # AGENT 2: The Implementation Architect (Structure Expert)
            architect = Agent(
                role='Lead Solutions Architect',
                goal=f'Convert strategic findings into a technical execution blueprint for {objective}',
                backstory="Expert in converting abstract concepts into structured, scalable system architectures.",
                llm=llm,
                verbose=True,
                allow_delegation=False
            )

            # TASK 1: Analysis Phase
            analysis_task = Task(
                description=f"Perform a deep-dive analysis into {objective}. Identify 3 core architectural pillars.",
                agent=analyst,
                expected_output="A structured list of 3 strategic technical insights."
            )

            # TASK 2: Blueprinting Phase
            blueprint_task = Task(
                description=f"Design a 12-month technical roadmap and high-level architecture based on the analysis.",
                agent=architect,
                expected_output="A comprehensive Markdown technical roadmap with milestones."
            )

            # EXECUTION: Sequential Orchestration
            with st.status("🛠️ Swarm Active: Agents are reasoning...", expanded=True) as status:
                st.write("📡 Analyst is processing objective...")
                crew = Crew(
                    agents=[analyst, architect], 
                    tasks=[analysis_task, blueprint_task], 
                    process=Process.sequential # Ensures logical flow from research to design
                )
                final_intelligence = crew.kickoff()
                status.update(label="✅ Collaboration Successful!", state="complete")

            # --- 4. OUTPUT DISPLAY ---
            st.markdown("### 📡 SYSTEM INTELLIGENCE REPORT")
            st.markdown(f'<div class="report-container">{final_intelligence}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Orchestration Failed: {str(e)}")

else:
    st.info("System Idle. Enter an objective and initiate swarm to begin.")
