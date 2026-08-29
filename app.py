# import streamlit as st
# import asyncio
# import os
# from config.docker_utils import start_docker_executor,stop_docker_executor
# from config.model_client import get_model_client
# from autogen_agentchat.base import TaskResult
# from autogen_agentchat.messages import TextMessage
# from config.constant import DOCKER_WORK_DIR
# from team.analysergpt_team import get_analyser_team
# from config.docker_container import get_docker_executor

# import warnings
# warnings.filterwarnings("ignore")


# # st.title('Analyzer GPT - Data analyzer')

# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []
# if 'autogen_team_state' not in st.session_state:
#     st.session_state.autogen_team_state =  None #save_to_db(username,session_id,None)


# file = st.file_uploader("Upload a CSV file", type=["csv"])

# task = st.chat_input("Enter your task")

# async def run_agent_team(docker,model_client,task):

#     try:
#         await start_docker_executor(docker)
#         data_analyzer_team , docker = await get_analyser_team()

#         if st.session_state.autogen_team_state is not None:
#             await data_analyzer_team.load_state(st.session_state.autogen_team_state)

#         async for message in data_analyzer_team.run_stream(task=task):

#             if isinstance(message, TextMessage):
#                 st.markdown(msg:= f" {message.source}: {message.content}")
#                 # st.markdown(msg)
#                 st.session_state.messages.append(msg)

#             elif isinstance(message, TaskResult):
#                 st.markdown(msg:=f'Task Result: {message.stop_reason}')
#                 st.session_state.messages.append(msg)
            
                

        
#         st.session_state.autogen_team_state = await data_analyzer_team.save_state()


#     except Exception as e:
#         st.error(e)
#     finally:
#         await stop_docker_executor(docker)


# if st.session_state.messages:
#     for msg in st.session_state.messages:
#         st.markdown(msg)

# if task:
#     try:
#         if file is not None and task:
#             if not os.path.exists(DOCKER_WORK_DIR):
#                 os.makedirs(DOCKER_WORK_DIR)

#             with open(f"{DOCKER_WORK_DIR}/data.csv", "wb") as f:
#                 f.write(file.getbuffer())

#         openai_model_client=get_model_client()
#         docker = get_docker_executor()

#         asyncio.run(run_agent_team(docker,openai_model_client,task))

#         if os.path.exists(f'{DOCKER_WORK_DIR}/outputplot.png'):
#             st.image(f'{DOCKER_WORK_DIR}/outputplot.png',caption='Generated Image')
            


#     except  Exception as e:
#         st.error("Please upload a file and enter a task")   



# import streamlit as st
# import asyncio
# import os
# from config.docker_utils import start_docker_executor,stop_docker_executor
# from config.model_client import get_model_client
# from autogen_agentchat.base import TaskResult
# from autogen_agentchat.messages import TextMessage
# from config.constant import DOCKER_WORK_DIR
# from team.analysergpt_team import get_analyser_team
# from config.docker_container import get_docker_executor

# import warnings
# warnings.filterwarnings("ignore")


# st.title('InsightAI - Automated Data Analysis')

# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []
# if 'autogen_team_state' not in st.session_state:
#     st.session_state.autogen_team_state =  None #save_to_db(username,session_id,None)


# file = st.file_uploader("Upload a CSV file", type=["csv"])

# task = st.chat_input("Enter your task")

# async def run_agent_team(docker, model_client, task): # <-- Signature is fine

#     try:
#         await start_docker_executor(docker)
        
#         # vvv THIS IS THE CORRECTED LINE vvv
#         data_analyzer_team = await get_analyser_team(docker, model_client)
#         # ^^^ The 'docker' variable is no longer overwritten ^^^

#         if st.session_state.autogen_team_state is not None:
#             await data_analyzer_team.load_state(st.session_state.autogen_team_state)

#         async for message in data_analyzer_team.run_stream(task=task):

#             if isinstance(message, TextMessage):
                
#                 # --- THIS IS THE FIX ---
#                 if message.source == "CODE_EXECUTOR_AGENT":
#                     # For the code executor, wrap content in a text block
#                     msg_content = f"**{message.source}:**\n```text\n{message.content}\n```"
#                 else:
#                     # For other agents, display as normal markdown
#                     msg_content = f"**{message.source}:** {message.content}"
                
#                 st.markdown(msg_content)
#                 st.session_state.messages.append(msg_content)

#             elif isinstance(message, TaskResult):
#                 st.markdown(msg:=f'Task Result: {message.stop_reason}')
#                 st.session_state.messages.append(msg)
                
                

        
#         st.session_state.autogen_team_state = await data_analyzer_team.save_state()


#     except Exception as e:
#         st.error(e)
#     finally:
#         await stop_docker_executor(docker) # <-- This now correctly stops the one you started


# if st.session_state.messages:
#     for msg in st.session_state.messages:
#         st.markdown(msg)

# if task:
#     try:
#         if file is not None and task:
#             if not os.path.exists(DOCKER_WORK_DIR):
#                 os.makedirs(DOCKER_WORK_DIR)

#             with open(f"{DOCKER_WORK_DIR}/data.csv", "wb") as f:
#                 f.write(file.getbuffer())

#             openai_model_client=get_model_client()
#             docker = get_docker_executor() # <-- Executor created ONCE here

#             asyncio.run(run_agent_team(docker,openai_model_client,task)) # <-- And passed here

#             # vvv BONUS FIX: Changed to 'output.png' to match your agent prompt vvv
#             if os.path.exists(f'{DOCKER_WORK_DIR}/outputplot.png'):
#                 st.image(f'{DOCKER_WORK_DIR}/outputplot.png',caption='Generated Image')
                
#             if os.path.exists(f'{DOCKER_WORK_DIR}/output.html'):
#                 with open(f'{DOCKER_WORK_DIR}/output.html', 'r', encoding='utf-8') as f:
#                     html_string = f.read()
#                 st.components.v1.html(html_string, height=500, scrolling=True)
#             # ^^^ Added support for Plotly HTML files ^^^


#     except  Exception as e:
#         st.error("Please upload a file and enter a task")




# # working
# import streamlit as st
# import asyncio
# import os
# from config.docker_utils import start_docker_executor,stop_docker_executor
# from config.model_client import get_model_client
# from autogen_agentchat.base import TaskResult
# from autogen_agentchat.messages import TextMessage
# from config.constant import DOCKER_WORK_DIR
# from team.analysergpt_team import get_analyser_team
# from config.docker_container import get_docker_executor

# import warnings
# warnings.filterwarnings("ignore")


# st.title('InsightAI - Automated Data Analysis')

# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []
# if 'autogen_team_state' not in st.session_state:
#     st.session_state.autogen_team_state =  None #save_to_db(username,session_id,None)


# file = st.file_uploader("Upload a CSV file", type=["csv"])

# task = st.chat_input("Enter your task")

# async def run_agent_team(docker, model_client, task):

#     # --- NEW: Use st.status() to show a spinner and log messages ---
#     with st.status("InsightAI is processing your request...", state="running") as status_box:
#         try:
#             await start_docker_executor(docker)
            
#             data_analyzer_team = await get_analyser_team(docker, model_client)

#             if st.session_state.autogen_team_state is not None:
#                 await data_analyzer_team.load_state(st.session_state.autogen_team_state)

#             async for message in data_analyzer_team.run_stream(task=task):

#                 if isinstance(message, TextMessage):
                    
#                     if message.source == "CODE_EXECUTOR_AGENT":
#                         # Update status for code execution
#                         status_box.update(label="Running code in Docker...")
#                         # For the code executor, wrap content in a text block
#                         msg_content = f"**{message.source}:**\n```text\n{message.content}\n```"
#                     else:
#                         # Update status for analyst
#                         status_box.update(label="Analyst is thinking...")
#                         # For other agents, display as normal markdown
#                         msg_content = f"**{message.source}:** {message.content}"
                    
#                     status_box.markdown(msg_content) # Print message INSIDE the status box
#                     st.session_state.messages.append(msg_content)

#                 elif isinstance(message, TaskResult):
#                     msg_content = f'Task Result: {message.stop_reason}'
#                     status_box.markdown(msg_content)
#                     st.session_state.messages.append(msg_content)
                    
#                     if message.stop_reason != "in_progress":
#                         # --- NEW: Mark the status as complete when done ---
#                         status_box.update(label="Task Complete!", state="complete")
#                         break # Exit the loop
            
#             st.session_state.autogen_team_state = await data_analyzer_team.save_state()

#         except Exception as e:
#             st.error(e)
#             # --- NEW: Mark the status as error if it fails ---
#             status_box.update(label="An error occurred!", state="error")
#         finally:
#             await stop_docker_executor(docker)


# if st.session_state.messages:
#     # This logic needs to change slightly, as we don't want to
#     # re-display messages that were already in the status box.
#     # For now, this will re-display the entire chat history on
#     # every run, which is Streamlit's default behavior.
#     for msg in st.session_state.messages:
#         st.markdown(msg)

# if task:
#     # This part remains the same, but it's important that
#     # 'run_agent_team' is now self-contained.
#     try:
#         if file is not None and task:
#             # Clear previous messages when starting a new task
#             st.session_state.messages = [] 
            
#             if not os.path.exists(DOCKER_WORK_DIR):
#                 os.makedirs(DOCKER_WORK_DIR)

#             with open(f"{DOCKER_WORK_DIR}/data.csv", "wb") as f:
#                 f.write(file.getbuffer())

#             openai_model_client=get_model_client()
#             docker = get_docker_executor() 

#             asyncio.run(run_agent_team(docker,openai_model_client,task)) 

#             # Images and HTML will be displayed *outside* the status box,
#             # which is what we want.
#             if os.path.exists(f'{DOCKER_WORK_DIR}/outputplot.png'):
#                 st.image(f'{DOCKER_WORK_DIR}/outputplot.png',caption='Generated Image')
                
#             if os.path.exists(f'{DOCKER_WORK_DIR}/output.html'):
#                 with open(f'{DOCKER_WORK_DIR}/output.html', 'r', encoding='utf-8') as f:
#                     html_string = f.read()
#                 st.components.v1.html(html_string, height=500, scrolling=True)

#         elif file is None:
#             st.error("Please upload a file first.")
        
#     except  Exception as e:
#         st.error(f"An error occurred: {e}")








# import streamlit as st
# import asyncio
# import os
# import threading
# import queue  # <-- NEW IMPORT
# from config.docker_utils import start_docker_executor, stop_docker_executor
# from config.model_client import get_model_client
# from autogen_agentchat.base import TaskResult
# from autogen_agentchat.messages import TextMessage
# from config.constant import DOCKER_WORK_DIR
# from team.analysergpt_team import get_analyser_team
# from config.docker_container import get_docker_executor

# import warnings
# warnings.filterwarnings("ignore")


# st.title('InsightAI - Automated Data Analysis')

# # --- NEW: Session State Setup ---
# if 'messages' not in st.session_state:
#     st.session_state.messages = []
# if 'is_running' not in st.session_state:
#     st.session_state.is_running = False
# if 'msg_queue' not in st.session_state:
#     st.session_state.msg_queue = queue.Queue()
# if 'agent_thread' not in st.session_state:
#     st.session_state.agent_thread = None

# # Display all past messages
# for msg in st.session_state.messages:
#     st.markdown(msg)


# file = st.file_uploader("Upload a CSV file", type=["csv"])
# task = st.chat_input("Enter your task")


# # --- NEW THREADED FUNCTION ---
# # This function runs the agent team in a separate thread
# # and uses a queue to send messages back to Streamlit
# def run_agent_team_threaded(docker, model_client, task, msg_queue):
    
#     # Create a new event loop for this thread
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)

#     async def run_async():
#         try:
#             await start_docker_executor(docker)
#             data_analyzer_team = await get_analyser_team(docker, model_client)

#             if "autogen_team_state" in st.session_state:
#                  await data_analyzer_team.load_state(st.session_state.autogen_team_state)

#             # Send the first status update
#             msg_queue.put({"type": "status", "label": "Analyst is thinking..."})

#             async for message in data_analyzer_team.run_stream(task=task):
                
#                 if isinstance(message, TextMessage):
#                     if message.source == "DATA_ANALYSER_AGENT":
#                         # Send the message, then the *next* status
#                         msg_queue.put({"type": "message", "content": f"**{message.source}:** {message.content}"})
#                         msg_queue.put({"type": "status", "label": "Running code in Docker..."})
                    
#                     elif message.source == "CODE_EXECUTOR_AGENT":
#                         # Send the message, then the *next* status
#                         msg_queue.put({"type": "message", "content": f"**{message.source}:**\n```text\n{message.content}\n```"})
#                         msg_queue.put({"type": "status", "label": "Analyst is thinking..."})
                
#                 elif isinstance(message, TaskResult):
#                     msg_content = f'Task Result: {message.stop_reason}'
#                     msg_queue.put({"type": "message", "content": msg_content})
#                     if message.stop_reason != "in_progress":
#                         break
            
#             st.session_state.autogen_team_state = await data_analyzer_team.save_state()

#         except Exception as e:
#             msg_queue.put({"type": "error", "content": str(e)})
#         finally:
#             await stop_docker_executor(docker)
#             # Send a "done" signal
#             msg_queue.put({"type": "done"})
    
#     # Run the async function in the new event loop
#     loop.run_until_complete(run_async())


# # --- UPDATED MAIN LOGIC ---

# # 1. This block handles STARTING the task
# if task and not st.session_state.is_running:
#     try:
#         if file is not None:
#             # Set running flag
#             st.session_state.is_running = True
            
#             # Clear old messages and queue
#             st.session_state.messages = []
#             st.session_state.msg_queue = queue.Queue()
            
#             if not os.path.exists(DOCKER_WORK_DIR):
#                 os.makedirs(DOCKER_WORK_DIR)

#             with open(f"{DOCKER_WORK_DIR}/data.csv", "wb") as f:
#                 f.write(file.getbuffer())
            
#             # Immediately display user's task
#             user_msg = f"**You:** {task}"
#             st.markdown(user_msg)
#             st.session_state.messages.append(user_msg)

#             openai_model_client = get_model_client()
#             docker = get_docker_executor()
            
#             # Start the agent thread
#             st.session_state.agent_thread = threading.Thread(
#                 target=run_agent_team_threaded,
#                 args=(docker, openai_model_client, task, st.session_state.msg_queue)
#             )
#             st.session_state.agent_thread.start()
            
#             # Force a rerun to enter the "is_running" block
#             st.rerun() 
            
#         elif file is None:
#             st.error("Please upload a file first.")
            
#     except Exception as e:
#         st.error(f"An error occurred: {e}")
#         st.session_state.is_running = False

# # 2. This block handles POLLING while the task is running
# if st.session_state.is_running:
#     # Create the placeholder *once*
#     placeholder = st.empty()
    
#     while True:
#         try:
#             # Check for a new message
#             msg = st.session_state.msg_queue.get(timeout=0.1) 
            
#             if msg["type"] == "status":
#                 # This is the key: update the placeholder with a new status box
#                 placeholder.status(msg["label"])
            
#             elif msg["type"] == "message":
#                 # Clear the placeholder and show the message
#                 placeholder.empty()
#                 st.markdown(msg["content"])
#                 st.session_state.messages.append(msg["content"])
            
#             elif msg["type"] == "error":
#                 placeholder.empty()
#                 st.error(msg["content"])
            
#             elif msg["type"] == "done":
#                 placeholder.empty()
#                 st.session_state.is_running = False
#                 st.session_state.agent_thread.join()
#                 st.session_state.agent_thread = None
#                 break # Exit the while loop

#         except queue.Empty:
#             # If no message, rerun to check the queue again
#             # This is the magic that makes it feel iterative
#             st.rerun() 
    
#     # After the loop breaks (on "done"), rerun to show images
#     st.rerun()

# # 3. This block handles showing images *after* the run is complete
# if not st.session_state.is_running and len(st.session_state.messages) > 0:
    
#     # This check is now safe because it only runs *after* the chat is done
#     if os.path.exists(f'{DOCKER_WORK_DIR}/outputplot.png'):
#         with st.status("Generating Image...", state="running") as img_status:
#             img_status.update(label="Image Generated!", state="complete")
#         st.image(f'{DOCKER_WORK_DIR}/outputplot.png',caption='Generated Image')
        
#     if os.path.exists(f'{DOCKER_WORK_DIR}/output.html'):
#         with st.status("Loading Interactive Chart...", state="running") as html_status:
#             with open(f'{DOCKER_WORK_DIR}/output.html', 'r', encoding='utf-8') as f:
#                 html_string = f.read()
#             html_status.update(label="Chart Ready!", state="complete")
#         st.components.v1.html(html_string, height=500, scrolling=True)








# # properly working
# import streamlit as st
# import asyncio
# import os
# from config.docker_utils import start_docker_executor,stop_docker_executor
# from config.model_client import get_model_client
# from autogen_agentchat.base import TaskResult
# from autogen_agentchat.messages import TextMessage
# from config.constant import DOCKER_WORK_DIR
# from team.analysergpt_team import get_analyser_team
# from config.docker_container import get_docker_executor

# import warnings
# warnings.filterwarnings("ignore")


# st.title('InsightAI - Automated Data Analysis')

# # --- CHANGE 1: REMOVED the redundant message display block ---
# # The block "if st.session_state.messages:" that was here is GONE.
# # This stops the old chat from re-printing at the top.

# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []
# if 'autogen_team_state' not in st.session_state:
#     st.session_state.autogen_team_state =  None

# # --- CHANGE 2: Add session state for the final insight ---
# if 'final_insight' not in st.session_state:
#     st.session_state.final_insight = None


# file = st.file_uploader("Upload a CSV file", type=["csv"])

# task = st.chat_input("Enter your task")

# async def run_agent_team(docker, model_client, task):

#     # --- NEW: Use st.status() to show a spinner and log messages ---
#     with st.status("InsightAI is processing your request...", state="running") as status_box:
#         try:
#             await start_docker_executor(docker)
            
#             data_analyzer_team = await get_analyser_team(docker, model_client)

#             if st.session_state.autogen_team_state is not None:
#                 await data_analyzer_team.load_state(st.session_state.autogen_team_state)

#             async for message in data_analyzer_team.run_stream(task=task):

#                 if isinstance(message, TextMessage):
                    
#                     # --- CHANGE 3: Fixed 'message.source' bug ---
#                     if message.source == "CODE_EXECUTOR_AGENT":
#                         status_box.update(label="Running code in Docker...")
#                         msg_content = f"**{message.source}:**\n```text\n{message.content}\n```"
                    
#                     elif message.source == "DATA_ANALYSER_AGENT":
#                         status_box.update(label="Analyst is thinking...")
#                         msg_content = f"**{message.source}:** {message.content}"
                        
#                         # --- CHANGE 4: Capture the final insight ---
#                         # This will be overwritten by the plan, but then
#                         # by the final analysis, which is what we want.
#                         st.session_state.final_insight = message.content
                    
#                     else:
#                         # Handle other potential agents
#                         msg_content = f"**{message.source}:** {message.content}"

#                     status_box.markdown(msg_content) # Print message INSIDE the status box
#                     st.session_state.messages.append(msg_content)

#                 elif isinstance(message, TaskResult):
#                     msg_content = f'Task Result: {message.stop_reason}'
#                     status_box.markdown(msg_content)
#                     st.session_state.messages.append(msg_content)
                    
#                     if message.stop_reason != "in_progress":
#                         status_box.update(label="Task Complete!", state="complete")
#                         break 
            
#             st.session_state.autogen_team_state = await data_analyzer_team.save_state()

#         except Exception as e:
#             st.error(e)
#             status_box.update(label="An error occurred!", state="error")
#         finally:
#             await stop_docker_executor(docker)


# if task:
#     try:
#         if file is not None and task:
#             # Clear previous messages and insight
#             st.session_state.messages = []
#             st.session_state.final_insight = None # <-- Reset the insight
            
#             # --- NEW: Add file cleanup logic ---
#             if not os.path.exists(DOCKER_WORK_DIR):
#                 os.makedirs(DOCKER_WORK_DIR)
            
#             # Always delete old artifacts before starting a new task
#             if os.path.exists(f'{DOCKER_WORK_DIR}/outputplot.png'):
#                 os.remove(f'{DOCKER_WORK_DIR}/outputplot.png')
#             if os.path.exists(f'{DOCKER_WORK_DIR}/output.html'):
#                 os.remove(f'{DOCKER_WORK_DIR}/output.html')
#             # --- END OF CLEANUP LOGIC ---

#             with open(f"{DOCKER_WORK_DIR}/data.csv", "wb") as f:
#                 f.write(file.getbuffer())
            
#             # Immediately show the user's task
#             user_msg = f"**You:** {task}"
#             st.markdown(user_msg)
#             st.session_state.messages.append(user_msg)

#             openai_model_client=get_model_client()
#             docker = get_docker_executor() 

#             asyncio.run(run_agent_team(docker,openai_model_client,task)) 

#             # --- CHANGE 5: Display Final Insight Aesthetically ---
#             if st.session_state.final_insight:
#                 st.subheader("Final Analysis & Insights")
#                 st.markdown(st.session_state.final_insight)
#                 st.markdown("---") # Add a separator
#             # --- END OF NEW DISPLAY ---

#             # Images and HTML will be displayed *after* the insight
#             if os.path.exists(f'{DOCKER_WORK_DIR}/outputplot.png'):
#                 st.image(f'{DOCKER_WORK_DIR}/outputplot.png',caption='Generated Image')
                
#             if os.path.exists(f'{DOCKER_WORK_DIR}/output.html'):
#                 with open(f'{DOCKER_WORK_DIR}/output.html', 'r', encoding='utf-8') as f:
#                     html_string = f.read()
#                 st.components.v1.html(html_string, height=500, scrolling=True)

#         elif file is None:
#             st.error("Please upload a file first.")
        
#     except  Exception as e:
#         st.error(f"An error occurred: {e}")



# # final working
# import streamlit as st
# import asyncio
# import os
# from config.docker_utils import start_docker_executor,stop_docker_executor
# from config.model_client import get_model_client
# from autogen_agentchat.base import TaskResult
# from autogen_agentchat.messages import TextMessage
# from config.constant import DOCKER_WORK_DIR
# from team.analysergpt_team import get_analyser_team
# from config.docker_container import get_docker_executor

# import warnings
# warnings.filterwarnings("ignore")

# # --- CHANGE 1: Set Page Configuration (Aesthetic) ---
# st.set_page_config(
#     page_title="InsightAI",
#     page_icon="🤖",
#     layout="wide"
# )

# # --- CHANGE 2: New Title and Subheader (Aesthetic) ---
# # --- CHANGE 1: New Title and Subheader (Aesthetic) ---
# st.title("🤖 InsightAI")
# st.subheader("Your AI Data Agent. Perform any operation, from cleaning to analysis, just by asking.")

# # --- CHANGE 3: Sidebar for File Upload (Aesthetic) ---
# with st.sidebar:
#     st.title("Configuration")
#     file = st.file_uploader("Upload a CSV file", type=["csv"])
#     st.markdown("---")
#     st.markdown("Developed by Kartik") # You can put your name here


# # --- Session State Setup (No Change) ---
# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []
# if 'autogen_team_state' not in st.session_state:
#     st.session_state.autogen_team_state =  None
# if 'final_insight' not in st.session_state:
#     st.session_state.final_insight = None


# # --- CHANGE 4: Welcome Message (Aesthetic) ---
# # If no messages, show a welcome screen
# if not st.session_state.messages and not st.session_state.final_insight:
#     st.markdown(
#         """
#         ### Welcome to InsightAI!
        
#         To get started:
        
#         1.  **Upload a CSV file** in the sidebar on the left.
#         2.  **Ask a question** in the chat box below.
        
#         **Here are some ideas you can ask:**
#         * "What's the correlation between all numeric columns?"
#         * "Show me a bar chart of the average price by airline."
#         * "Give me an interactive scatter plot of price vs. duration."
#         """
#     )

# # --- Main Chat Input (No Change) ---
# task = st.chat_input("Ask a question about your data...")

# async def run_agent_team(docker, model_client, task):

#     with st.status("InsightAI is processing your request...", state="running") as status_box:
#         try:
#             await start_docker_executor(docker)
#             data_analyzer_team = await get_analyser_team(docker, model_client)

#             if st.session_state.autogen_team_state is not None:
#                 await data_analyzer_team.load_state(st.session_state.autogen_team_state)

#             async for message in data_analyzer_team.run_stream(task=task):
#                 if isinstance(message, TextMessage):
                    
#                     # (Fixed message.source.name bug)
#                     if message.source == "CODE_EXECUTOR_AGENT":
#                         status_box.update(label="Running code in Docker...")
#                         msg_content = f"**{message.source}:**\n```text\n{message.content}\n```"
                    
#                     elif message.source == "DATA_ANALYSER_AGENT":
#                         status_box.update(label="Analyst is thinking...")
#                         msg_content = f"**{message.source}:** {message.content}"
                        
#                         # (Capture final insight)
#                         st.session_state.final_insight = message.content
                    
#                     else:
#                         msg_content = f"**{message.source}:** {message.content}"

#                     status_box.markdown(msg_content)
#                     st.session_state.messages.append(msg_content)

#                 elif isinstance(message, TaskResult):
#                     msg_content = f'Task Result: {message.stop_reason}'
#                     status_box.markdown(msg_content)
#                     st.session_state.messages.append(msg_content)
                    
#                     if message.stop_reason != "in_progress":
#                         status_box.update(label="Task Complete!", state="complete")
#                         break 
            
#             st.session_state.autogen_team_state = await data_analyzer_team.save_state()

#         except Exception as e:
#             st.error(e)
#             status_box.update(label="An error occurred!", state="error")
#         finally:
#             await stop_docker_executor(docker)


# if task:
#     try:
#         if file is not None and task:
#             # Clear previous messages and insight
#             st.session_state.messages = []
#             st.session_state.final_insight = None # <-- Reset the insight
            
#             if not os.path.exists(DOCKER_WORK_DIR):
#                 os.makedirs(DOCKER_WORK_DIR)
            
#             # (File cleanup logic)
#             if os.path.exists(f'{DOCKER_WORK_DIR}/outputplot.png'):
#                 os.remove(f'{DOCKER_WORK_DIR}/outputplot.png')
#             if os.path.exists(f'{DOCKER_WORK_DIR}/output.html'):
#                 os.remove(f'{DOCKER_WORK_DIR}/output.html')

#             with open(f"{DOCKER_WORK_DIR}/data.csv", "wb") as f:
#                 f.write(file.getbuffer())
            
#             # Immediately show the user's task
#             user_msg = f"**You:** {task}"
#             st.markdown(user_msg)
#             st.session_state.messages.append(user_msg)

#             openai_model_client=get_model_client()
#             docker = get_docker_executor() 

#             asyncio.run(run_agent_team(docker,openai_model_client,task)) 

#             # (Display Final Insight Aesthetically)
#             if st.session_state.final_insight:
#                 st.subheader("Final Analysis & Insights")
#                 st.markdown(st.session_state.final_insight)
#                 st.markdown("---") 

#             # (Display plots)
#             if os.path.exists(f'{DOCKER_WORK_DIR}/outputplot.png'):
#                 st.image(f'{DOCKER_WORK_DIR}/outputplot.png',caption='Generated Image')
                
#             if os.path.exists(f'{DOCKER_WORK_DIR}/output.html'):
#                 with open(f'{DOCKER_WORK_DIR}/output.html', 'r', encoding='utf-8') as f:
#                     html_string = f.read()
#                 st.components.v1.html(html_string, height=500, scrolling=True)

#         elif file is None:
#             st.error("Please upload a file first.")
        
#     except  Exception as e:
#         st.error(f"An error occurred: {e}")


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

# --- 1. Page Configuration (Professional Look) ---
st.set_page_config(
    page_title="InsightAI",
    page_icon="🤖",
    layout="wide"
)

# # --- NEW: AESTHETIC BACKGROUND ---
# page_bg_css = """
# <style>

# .stApp {
#     background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
# }

# /* Remove the white overlay container */
# .main {
#     background-color: transparent !important;
# }

# /* Remove white background from the content area */
# .block-container {
#     background-color: transparent !important;
# }

# </style>
# """



# st.markdown(page_bg_css, unsafe_allow_html=True)
# --- END AESTHETIC BACKGROUND ---

# --- 2. Title and Subheader (Professional Look) ---
st.title("🤖 InsightAI")
st.subheader("Your On-Demand AI Data Agent. Securely analyze, clean, and visualize data using natural language.")

# --- 3. Sidebar (Professional Look) ---
with st.sidebar:
    st.title("Control Panel")
    file = st.file_uploader("Upload your .csv file", type=["csv"])
    
    st.markdown("---")
    st.info(
        """
        **Security & Privacy:** Your data is processed in a secure, isolated Docker 
        container and is deleted after your session.
        """
    )
    st.markdown("Developed by Kartik and Harshil") # Your name here

# --- 4. Session State Setup ---
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'autogen_team_state' not in st.session_state:
    st.session_state.autogen_team_state = None
if 'final_insight' not in st.session_state:
    st.session_state.final_insight = None

# --- 5. Welcome Message (Aesthetic) ---
# This shows only if no chat has started
if not st.session_state.messages and not st.session_state.final_insight:
    st.markdown(
        """
        ### Welcome to InsightAI.
        
        This tool empowers you to perform complex data operations using simple, plain English.
        
        **To begin, please upload your CSV file using the Control Panel on the left.**
        
        Once uploaded, you can request any operation:
        
        * **Data Cleaning:** "Find and fill all missing 'Age' values with the column median."
        * **Feature Engineering:** "Create a new column 'Price_per_Unit' by dividing 'Price' by 'Quantity'."
        * **Statistical Analysis:** "What is the statistical summary for all numeric columns?"
        * **Visualization:** "Generate an interactive scatter plot of 'Price' vs. 'Rating'."
        """
    )

# --- 6. Chat Input (Professional Look) ---
task = st.chat_input("Enter your data operation request... (e.g., 'Plot average price by airline')")

# --- 7. Agent Team Function (Your Core Logic) ---
async def run_agent_team(docker, model_client, task):

    # This status box will contain the *entire* chat log for this run
    with st.status("InsightAI is processing your request...", state="running") as status_box:
        try:
            await start_docker_executor(docker)
            data_analyzer_team = await get_analyser_team(docker, model_client)

            if st.session_state.autogen_team_state is not None:
                await data_analyzer_team.load_state(st.session_state.autogen_team_state)

            async for message in data_analyzer_team.run_stream(task=task):
                if isinstance(message, TextMessage):
                    
                    # Check source.name (bug fix)
                    if message.source == "CODE_EXECUTOR_AGENT":
                        status_box.update(label="Running code in Docker...")
                        msg_content = f"**{message.source}:**\n```text\n{message.content}\n```"
                    
                    elif message.source == "DATA_ANALYSER_AGENT":
                        status_box.update(label="Analyst is thinking...")
                        msg_content = f"**{message.source}:** {message.content}"
                        
                        # Capture the last thing the analyst says
                        st.session_state.final_insight = message.content
                    
                    else:
                        msg_content = f"**{message.source}:** {message.content}"

                    status_box.markdown(msg_content) # Print message INSIDE the status box
                    st.session_state.messages.append(msg_content) # Save to session

                elif isinstance(message, TaskResult):
                    msg_content = f'Task Result: {message.stop_reason}'
                    status_box.markdown(msg_content)
                    st.session_state.messages.append(msg_content)
                    
                    if message.stop_reason != "in_progress":
                        status_box.update(label="Task Complete!", state="complete")
                        break 
            
            st.session_state.autogen_team_state = await data_analyzer_team.save_state()

        except Exception as e:
            st.error(e)
            status_box.update(label="An error occurred!", state="error")
        finally:
            await stop_docker_executor(docker)

# --- 8. Main Execution Logic ---
if task:
    try:
        if file is not None and task:
            # Clear previous run's messages and insight
            st.session_state.messages = []
            st.session_state.final_insight = None 
            
            if not os.path.exists(DOCKER_WORK_DIR):
                os.makedirs(DOCKER_WORK_DIR)
            
            # --- FILE CLEANUP (Bug Fix) ---
            # Always delete old artifacts before starting a new task
            if os.path.exists(f'{DOCKER_WORK_DIR}/outputplot.png'):
                os.remove(f'{DOCKER_WORK_DIR}/outputplot.png')
            if os.path.exists(f'{DOCKER_WORK_DIR}/output.html'):
                os.remove(f'{DOCKER_WORK_DIR}/output.html')
            # Fix typo: outputplot.png -> output.png (in case agent uses it)
            if os.path.exists(f'{DOCKER_WORK_DIR}/output.png'):
                os.remove(f'{DOCKER_WORK_DIR}/output.png')
            # --- END OF CLEANUP ---

            with open(f"{DOCKER_WORK_DIR}/data.csv", "wb") as f:
                f.write(file.getbuffer())
            
            # Immediately show the user's task
            user_msg = f"**You:** {task}"
            st.markdown(user_msg)
            st.session_state.messages.append(user_msg)

            openai_model_client = get_model_client()
            docker = get_docker_executor() 

            # Run the agent team
            asyncio.run(run_agent_team(docker, openai_model_client, task)) 

            # --- 9. Final Insight Display (Aesthetic) ---
            # This runs *after* the status box is complete
            if st.session_state.final_insight:
                st.subheader("Final Analysis & Insights")
                with st.container(border=True): # Adds a clean border
                    st.markdown(st.session_state.final_insight)
                st.markdown("---") # Add a separator

            # --- 10. Plot/HTML Display ---
            # (Fixed typo to check for output.png as well)
            if os.path.exists(f'{DOCKER_WORK_DIR}/output.png'):
                st.image(f'{DOCKER_WORK_DIR}/output.png', caption='Generated Image')
            elif os.path.exists(f'{DOCKER_WORK_DIR}/outputplot.png'):
                st.image(f'{DOCKER_WORK_DIR}/outputplot.png', caption='Generated Image')
                
            if os.path.exists(f'{DOCKER_WORK_DIR}/output.html'):
                with open(f'{DOCKER_WORK_DIR}/output.html', 'r', encoding='utf-8') as f:
                    html_string = f.read()
                st.components.v1.html(html_string, height=500, scrolling=True)

        elif file is None:
            st.error("Please upload a file first.")
        
    except  Exception as e:
        st.error(f"An error occurred: {e}")