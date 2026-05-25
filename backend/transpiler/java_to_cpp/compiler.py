import subprocess
import os
from ..config import TEMP_DIR

def run_cpp(code):
    cpp_file = os.path.join(TEMP_DIR, "main.cpp")

    executable = os.path.join(TEMP_DIR, "main")

    # Windows executable
    if os.name == "nt":
        executable += ".exe"

    # WRITE SOURCE CODE
    with open(cpp_file, "w") as file:
        file.write(code)

    # COMPILE C++ CODE
    compile_process = subprocess.run(
        ["g++", cpp_file, "-o", executable],
        capture_output=True,
        text=True
    )

    # Compilation Error
    if compile_process.returncode != 0:
        return {
            "success": False,
            "stage": "compilation",
            "error": compile_process.stderr
        }

    # RUN EXECUTABLE
    try:
        run_process = subprocess.run(
            [executable],
            capture_output=True,
            text=True,
            timeout=5
        )

        # Runtime Error
        if run_process.returncode != 0:

            return {
                "success": False,
                "stage": "runtime",
                "error": run_process.stderr
            }

        return {
            "success": True,
            "output": run_process.stdout
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stage": "timeout",
            "error": "Program execution exceeded time limit"
        }
