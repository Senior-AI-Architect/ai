import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="AI Swarm OS", page_icon="🤖", layout="wide")

with st.sidebar:
    st.header("⚙️ System Config")
    user_key = st.text_input("OpenAI API Key", type="password")
    topic = st.text_input("Swarm Objective", value="AI Agents 2026")

if st.button("🚀 Initialize Swarm"):
    if not user_key:
        st.error("⚠️ Please enter your OpenAI API Key!")
    else:
        try:
            os.environ["OPENAI_API_KEY"] = user_key
            llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

            # --- 2. AGENTS (Without External Tools for Stability) ---
            researcher = Agent(
                role='Neural Researcher',
                goal=f'Analyze high-level trends for {topic}',
                backstory="Expert AI analyst with vast internal knowledge of technical breakthroughs.",
                llm=llm,
                verbose=True
            )

            architect = Agent(
                role='System Architect',
                goal=f'Design a technical blueprint for {topic}',
                backstory="Senior system designer focused on scalability and future-proofing.",
                llm=llm,
                verbose=True
            )

            # --- 3. TASKS ---
            t1 = Task(description=f"Identify 5 critical trends in {topic}.", agent=researcher, expected_output="List of 5 trends.")
            t2 = Task(description=f"Create a 6-month roadmap for {topic}.", agent=architect, expected_output="Technical Markdown Roadmap.")

            # --- 4. EXECUTION ---
            with st.status("🛠️ Swarm active: Collaborating...", expanded=True) as status:
                crew = Crew(agents=[researcher, architect], tasks=[t1, t2], process=Process.sequential)
                result = crew.kickoff()
                status.update(label="✅ Success!", state="complete")

            st.divider()
            st.subheader("📊 Final Intelligence Report")
            st.markdown(result)

        except Exception as e:
            st.error(f"Error: {str(e)}")
