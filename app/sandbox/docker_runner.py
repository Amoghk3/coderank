import tempfile
import subprocess

from pathlib import Path


class DockerRunner:

    EXECUTION_TIMEOUT = 2

    LANGUAGE_CONFIG = {

        "python": {
            "filename": "main.py",

            "image": "python:3.12-slim",

            "run": [
                "python",
                "/code/main.py",
            ],
        },

        "javascript": {
            "filename": "main.js",

            "image": "node:20-alpine",

            "run": [
                "node",
                "/code/main.js",
            ],
        },
    }

    @classmethod
    def run_code(
        cls,
        language_name: str,
        source_code: str,
        stdin_input: str = "",
    ):

        config = cls.LANGUAGE_CONFIG.get(
            language_name.lower()
        )

        if not config:

            return {
                "stdout": "",
                "stderr": "Unsupported language",
                "exit_code": -1,
                "timeout": False,
            }

        with tempfile.TemporaryDirectory() as tmpdir:

            code_path = (
                Path(tmpdir)
                / config["filename"]
            )

            code_path.write_text(source_code)

            command = [
                "docker",
                "run",

                "-i",

                "--rm",

                "--network",
                "none",

                "--memory",
                "128m",

                "--cpus",
                "0.5",

                "-v",
                f"{tmpdir}:/code",

                config["image"],
            ] + config["run"]

            try:

                process = subprocess.run(
                    command,
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