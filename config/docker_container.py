# from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor

# from config.constant import DOCKER_TIMEOUT,DOCKER_WORK_DIR
# def get_docker_executor():
#     """
#     Returns a DockerCommandLineCodeExecutor instance configured with the specified work directory and timeout.
    
#     Returns:
#         DockerCommandLineCodeExecutor: Configured Docker command line code executor.
#     """
#     docker_executor = DockerCommandLineCodeExecutor(
#         image='analysergpt-image',
#         work_dir=DOCKER_WORK_DIR,
#         timeout=DOCKER_TIMEOUT
#     )
#     return docker_executor

from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from config.constant import DOCKER_TIMEOUT, DOCKER_WORK_DIR

def get_docker_executor(): # You might want to rename this function
    local_executor = LocalCommandLineCodeExecutor(
        work_dir=DOCKER_WORK_DIR,
        timeout=DOCKER_TIMEOUT
    )
    return local_executor
