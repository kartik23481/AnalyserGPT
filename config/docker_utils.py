import asyncio
async def start_docker_executor(docker_executor):
    """
    Starts the Docker command line code executor.
    
    Args:
        docker_executor (DockerCommandLineCodeExecutor): The Docker command line code executor to start.
    """
    await docker_executor.start()
    print("Docker executor started.")

async def stop_docker_executor(docker_executor):
    """
    Stops the Docker command line code executor.
    Args:
        docker_executor (DockerCommandLineCodeExecutor): The Docker command line code executor to stop.
    """
    await docker_executor.stop()
    print("Docker executor stopped.")