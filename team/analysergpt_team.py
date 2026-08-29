from agents.code_executor_agent import getCodeExecutorAgent
from agents.data_analyser_agent import getDataAnalyserAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from config.constant import TERMINATION_TEXT,MAX_TURNS
from autogen_agentchat.conditions import TextMentionTermination
# from config.model_client import get_model_client

async def get_analyser_team(docker_executor, model_client):
    # model_client = get_model_client()
    problem_solver_agent = getDataAnalyserAgent(model_client)
    code_executor_agent = getCodeExecutorAgent(docker_executor)
    TERMINATION_CONDITION = TextMentionTermination(TERMINATION_TEXT)

    # Now configuring the team that solves the DSA problem
    team = RoundRobinGroupChat(
        participants = [
            problem_solver_agent,
            code_executor_agent
        ],
        termination_condition=TERMINATION_CONDITION,
        max_turns = MAX_TURNS
    )
    await team.reset()
    return team
