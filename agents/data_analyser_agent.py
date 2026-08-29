from autogen_agentchat.agents import AssistantAgent
from agents.prompts.data_analyser_agent_prompt import DATA_ANALYSER_PROMPT

def getDataAnalyserAgent(model_client):
    data_analyser_agent = AssistantAgent(
        name = 'DATA_ANALYSER_AGENT',
        description = 'An agent that analyses the data and extracts the useful insights',
        model_client = model_client,
        system_message = DATA_ANALYSER_PROMPT
    )
    return data_analyser_agent