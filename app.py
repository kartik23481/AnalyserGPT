import streamlit as st
import asyncio
import os
from config.docker_utils import start_docker_executor, stop_docker_executor
from config.model_client import get_model_client
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage
from config.constant import DOCKER_WORK_DIR
from team.analysergpt_team import get_analyser_team
from config.docker_container import get_docker_executor

import warnings
warnings.filterwarnings("ignore")

# --- 1. Page Configuration (Enterprise Look) ---
st.set_page_config(
    page_title="Insight AI | Autonomous EDA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Production Aesthetics ---
st.markdown("""
    <style>
    /* Clean up top padding */
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }
    
    /* Elegant typography and spacing for headers */
    h1 { color: #0F172A; font-weight: 800; letter-spacing: -0.025em; }
    h2, h3 { color: #1E293B; font-weight: 700; }
    
    /* Style the status box to look like a terminal/workspace */
    [data-testid="stStatusWidget"] { 
        background-color: #F8FAFC; 
        border: 1px solid #E2E8F0; 
        border-radius: 8px; 
    }
    
    /* Subtle hover effects on containers */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        transition: box-shadow 0.3s ease;
    }
    div[data-testid="stVerticalBlock"] > div[style*="border"]:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. Title and Hero Section ---
st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-size: 2.8rem; margin-bottom: 0.5rem;">🧠 Insight AI</h1>
        <p style="font-size: 1.2rem; color: #64748B; margin-top: 0;">
            Autonomous Multi-Agent Data Analysis & Code Execution Engine
        </p>
    </div>
""", unsafe_allow_html=True)

# --- 3. Sidebar (Professional Control Panel) ---
with st.sidebar:
    st.markdown("### ⚙️ Workspace Configuration")
    file = st.file_uploader("Ingest Dataset (CSV)", type=["csv"], help="Upload a clean CSV file for analysis.")
    
    st.divider()
    
    st.markdown("### 🔒 Security & Privacy")
    st.info(
        "**Ephemeral Sandbox:** Your data and code are processed in an isolated, secure Docker container (E2B) and are permanently purged after your session ends.",
        icon="🛡️"
    )

# --- 4. Session State Setup ---
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'autogen_team_state' not in st.session_state:
    st.session_state.autogen_team_state = None
if 'final_insight' not in st.session_state:
    st.session_state.final_insight = None

# --- 5. Welcome Message (Dashboard Aesthetic) ---
if not st.session_state.messages and not st.session_state.final_insight:
    st.markdown("### Welcome to your AI Data Workspace.")
    st.markdown("Upload a dataset from the sidebar to activate the multi-agent system. You can request complex operations in plain English:")
    
    # Use columns to make the examples look like professional feature cards
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("🧹 **Data Cleaning**")
            st.caption('"Find and impute all missing values in the Age column using the median."')
        with st.container(border=True):
            st.markdown("📊 **Statistical Analysis**")
            st.caption('"Generate a statistical summary and correlation matrix for all numeric columns."')
    with col2:
        with st.container(border=True):
            st.markdown("⚙️ **Feature Engineering**")
            st.caption('"Create a new feature called Profit_Margin by dividing Profit by Revenue."')
        with st.container(border=True):
            st.markdown("📈 **Visualizations**")
            st.caption('"Plot an interactive scatter plot of Price vs. Rating grouped by Category."')

# --- 6. Chat Input ---
task = st.chat_input("Enter your analytical objective... (e.g., 'Identify the key drivers of churn')")

# --- 7. Agent Team Function (Core Logic Intact) ---
async def run_agent_team(docker, model_client, task, file_bytes=None, filename=None):

    with st.status("🚀 Initializing Insight AI Multi-Agent Loop...", state="running") as status_box:
        try:
            await start_docker_executor(docker)

            if file_bytes is not None and filename is not None:
                await docker.upload_file(filename, file_bytes)

            data_analyzer_team = await get_analyser_team(docker, model_client)

            if st.session_state.autogen_team_state is not None:
                await data_analyzer_team.load_state(st.session_state.autogen_team_state)

            async for message in data_analyzer_team.run_stream(task=task):
                if isinstance(message, TextMessage):
                    
                    # Enhanced formatting for agent logs
                    if message.source == "CODE_EXECUTOR_AGENT":
                        status_box.update(label="⚡ E2B Sandbox: Executing generated code...")
                        msg_content = f"**💻 CODE EXECUTOR:**\n```python\n{message.content}\n```"
                    
                    elif message.source == "DATA_ANALYSER_AGENT":
                        status_box.update(label="🧠 AutoGen Orchestrator: Analyzing outputs...")
                        msg_content = f"**🤖 DATA ANALYZER:** {message.content}"
                        st.session_state.final_insight = message.content
                    
                    else:
                        msg_content = f"**⚙️ {message.source}:** {message.content}"

                    status_box.markdown(msg_content) 
                    st.session_state.messages.append(msg_content) 

                elif isinstance(message, TaskResult):
                    msg_content = f'**✅ Task Result:** {message.stop_reason}'
                    status_box.markdown(msg_content)
                    st.session_state.messages.append(msg_content)
                    
                    if message.stop_reason != "in_progress":
                        status_box.update(label="Analysis Sequence Complete", state="complete")
                        break 
            
            st.session_state.autogen_team_state = await data_analyzer_team.save_state()

            # --- File handling remains untouched ---
            if not os.path.exists(DOCKER_WORK_DIR):
                os.makedirs(DOCKER_WORK_DIR)
            await docker.download_file("output.png",     f"{DOCKER_WORK_DIR}/output.png")
            await docker.download_file("outputplot.png", f"{DOCKER_WORK_DIR}/outputplot.png")
            await docker.download_file("output.html",    f"{DOCKER_WORK_DIR}/output.html")

        except Exception as e:
            st.error(e)
            status_box.update(label="System Error Encountered", state="error")
        finally:
            await stop_docker_executor(docker)

# --- 8. Main Execution Logic (Core Logic Intact) ---
if task:
    try:
        if file is not None and task:
            st.session_state.messages = []
            st.session_state.final_insight = None 
            
            if not os.path.exists(DOCKER_WORK_DIR):
                os.makedirs(DOCKER_WORK_DIR)
            
            # --- FILE CLEANUP ---
            if os.path.exists(f'{DOCKER_WORK_DIR}/outputplot.png'):
                os.remove(f'{DOCKER_WORK_DIR}/outputplot.png')
            if os.path.exists(f'{DOCKER_WORK_DIR}/output.html'):
                os.remove(f'{DOCKER_WORK_DIR}/output.html')
            if os.path.exists(f'{DOCKER_WORK_DIR}/output.png'):
                os.remove(f'{DOCKER_WORK_DIR}/output.png')

            with open(f"{DOCKER_WORK_DIR}/data.csv", "wb") as f:
                f.write(file.getbuffer())
            
            # Use chat_message for the user input to distinguish it beautifully
            with st.chat_message("user", avatar="👤"):
                st.write(task)
            st.session_state.messages.append(f"**You:** {task}")

            openai_model_client = get_model_client()
            docker = get_docker_executor() 

            file_bytes = file.getbuffer().tobytes()
            filename = file.name

            # Run the agent team
            asyncio.run(run_agent_team(docker, openai_model_client, task, file_bytes=file_bytes, filename=filename))

            # --- 9. Final Insight Display (Executive Dashboard Look) ---
            if st.session_state.final_insight:
                st.markdown("### 📋 Executive Summary")
                with st.container(border=True):
                    st.success("Target analysis generated successfully.", icon="✅")
                    st.markdown(st.session_state.final_insight)

            # --- 10. Plot/HTML Display (Polished Rendering) ---
            has_visuals = any(os.path.exists(f'{DOCKER_WORK_DIR}/{f}') for f in ['output.png', 'outputplot.png', 'output.html'])
            
            if has_visuals:
                st.markdown("### 📈 Visualizations")
                with st.container(border=True):
                    if os.path.exists(f'{DOCKER_WORK_DIR}/output.png'):
                        st.image(f'{DOCKER_WORK_DIR}/output.png', use_container_width=True)
                        with open(f'{DOCKER_WORK_DIR}/output.png', "rb") as file:
                            st.download_button(label="⬇️ Download Plot", data=file, file_name="insight_plot.png", mime="image/png")
                    elif os.path.exists(f'{DOCKER_WORK_DIR}/outputplot.png'):
                        st.image(f'{DOCKER_WORK_DIR}/outputplot.png', use_container_width=True)
                        with open(f'{DOCKER_WORK_DIR}/outputplot.png', "rb") as file:
                            st.download_button(label="⬇️ Download Plot", data=file, file_name="insight_plot.png", mime="image/png")
                        
                    if os.path.exists(f'{DOCKER_WORK_DIR}/output.html'):
                        with open(f'{DOCKER_WORK_DIR}/output.html', 'r', encoding='utf-8') as f:
                            html_string = f.read()
                        st.components.v1.html(html_string, height=600, scrolling=True)
                        with open(f'{DOCKER_WORK_DIR}/output.html', "rb") as file:
                            st.download_button(label="⬇️ Download Interactive Chart", data=file, file_name="insight_chart.html", mime="text/html")

        elif file is None:
            st.warning("⚠️ Action Required: Please ingest a dataset via the sidebar to proceed.")
        
    except Exception as e:
        st.error(f"Critical Failure: {e}")