import asyncio
import os
from typing import List, Any
from autogen_core.code_executor import CodeExecutor, CodeBlock, CodeResult
from e2b_code_interpreter import AsyncSandbox

from config.constant import DOCKER_TIMEOUT


class E2BCodeExecutor(CodeExecutor):
    """
    A drop-in CodeExecutor that runs code inside an E2B cloud sandbox.
    Uses the default 'code-interpreter-v1' template which already includes
    pandas, numpy, matplotlib, seaborn, scikit-learn, etc.
    """

    def __init__(self, timeout: int = DOCKER_TIMEOUT):
        self.timeout = timeout
        self.sandbox: AsyncSandbox | None = None

    async def start(self) -> None:
        """Starts the E2B Sandbox using the default code-interpreter template."""
        if not self.sandbox:
            # Use the default template - it already has all data science libraries.
            # Do NOT pass a custom template_id here; AsyncSandbox requires its own
            # code-interpreter-v1 kernel to be running on port 49999.
            self.sandbox = await AsyncSandbox.create(timeout=self.timeout)
            print("E2B Sandbox started.")

    async def upload_file(self, filename: str, file_bytes: bytes) -> None:
        """Uploads a file (as raw bytes) into the E2B sandbox filesystem.
        
        Args:
            filename: The filename to save as inside the sandbox (e.g., 'data.csv').
            file_bytes: The raw bytes content of the file.
        """
        if not self.sandbox:
            await self.start()
        import io
        await self.sandbox.files.write(f"/home/user/{filename}", io.BytesIO(file_bytes))
        # Also set working directory so pd.read_csv('data.csv') resolves correctly
        await self.sandbox.run_code("import os; os.chdir('/home/user')")
        print(f"Uploaded '{filename}' to E2B sandbox.")

    async def download_file(self, remote_filename: str, local_path: str) -> bool:
        """Downloads a file from the E2B sandbox to the local disk.
        
        Args:
            remote_filename: Filename inside the sandbox under /home/user/ (e.g., 'outputplot.png').
            local_path: Full local path to save the file to (e.g., 'temp/outputplot.png').
        
        Returns:
            True if file was found and downloaded, False if it doesn't exist in sandbox.
        """
        if not self.sandbox:
            return False
        try:
            content = await self.sandbox.files.read(f"/home/user/{remote_filename}", format="bytes")
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(content)
            print(f"Downloaded '{remote_filename}' from E2B sandbox to '{local_path}'.")
            return True
        except Exception:
            return False

    async def stop(self) -> None:
        """Stops the E2B Sandbox."""
        if self.sandbox:
            try:
                await self.sandbox.kill()
            except Exception:
                pass
            self.sandbox = None
            print("E2B Sandbox stopped.")

    async def restart(self) -> None:
        """Restarts the E2B Sandbox."""
        await self.stop()
        await self.start()

    async def execute_code_blocks(
        self, code_blocks: List[CodeBlock], cancellation_token: Any
    ) -> CodeResult:
        """Executes a list of code blocks inside the E2B sandbox with retry logic."""
        if not self.sandbox:
            await self.start()

        output = ""
        exit_code = 0

        for block in code_blocks:
            if block.language.lower() in ["python", "py"]:
                # Retry up to 2 times on network/timeout errors
                for attempt in range(3):
                    try:
                        execution = await self.sandbox.run_code(block.code)
                        break
                    except Exception as e:
                        if attempt < 2:
                            print(f"E2B run_code attempt {attempt + 1} failed ({e}), retrying...")
                            # Restart sandbox on connection errors
                            await self.restart()
                            await asyncio.sleep(2)
                        else:
                            return CodeResult(exit_code=1, output=f"E2B execution failed after 3 attempts: {e}")

                if execution.logs.stdout:
                    output += "\n".join(execution.logs.stdout) + "\n"
                if execution.logs.stderr:
                    output += "\n".join(execution.logs.stderr) + "\n"

                if execution.error:
                    output += (
                        f"Error: {execution.error.name} - {execution.error.value}\n"
                        f"{execution.error.traceback}\n"
                    )
                    exit_code = 1
                    break

            elif block.language.lower() in ["sh", "bash"]:
                try:
                    process = await self.sandbox.commands.run(block.code)
                    output += process.stdout + "\n" + process.stderr + "\n"
                    if process.exit_code != 0:
                        exit_code = process.exit_code
                        break
                except Exception as e:
                    return CodeResult(exit_code=1, output=f"E2B shell command failed: {e}")

        return CodeResult(exit_code=exit_code, output=output)


def get_docker_executor() -> E2BCodeExecutor:
    """
    Returns an E2BCodeExecutor instance.
    (Kept name get_docker_executor so we don't break existing app.py imports!)
    """
    return E2BCodeExecutor(timeout=DOCKER_TIMEOUT)
