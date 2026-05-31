import tempfile
import subprocess
from pathlib import Path


class DockerRunner:

    EXECUTION_TIMEOUT = 2

    @classmethod
    def run_code(
        cls,
        language_name: str,
        source_code: str,
        stdin_input: str = "",
    ):

        if language_name.lower() != "python":
            return {
                "stdout": "",
                "stderr": "Only Python enabled in local mode",
                "exit_code": -1,
                "timeout": False,
            }

        with tempfile.TemporaryDirectory() as tmpdir:

            code_file = Path(tmpdir) / "main.py"
            code_file.write_text(source_code)

            try:

                process = subprocess.run(
                    ["python", str(code_file)],
                    input=stdin_input,
                    text=True,
                    capture_output=True,
                    timeout=cls.EXECUTION_TIMEOUT,
                )

                return {
                    "stdout": process.stdout,
                    "stderr": process.stderr,
                    "exit_code": process.returncode,
                    "timeout": False,
                }

            except subprocess.TimeoutExpired:

                return {
                    "stdout": "",
                    "stderr": "Time limit exceeded",
                    "exit_code": -1,
                    "timeout": True,
                }