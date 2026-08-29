from autogen_agentchat.agents import CodeExecutorAgent 
from config.docker_container import get_docker_executor

def getCodeExecutorAgent(docker):
    # getting the docker contaier
    # docker = get_docker_executor()
    # Define the agent which runs the code in the docker container
    code_executor_agent = CodeExecutorAgent(
        name= 'CODE_EXECUTOR_AGENT',
        code_executor=docker
    )
    return code_executor_agent