import re
import subprocess
import os
from ..config import TEMP_DIR

def run_java(code):
    # Detect public class name from generated code
    match = re.search(r'public class (\w+)', code)
    class_name = match.group(1) if match else "Main"

    java_file = os.path.join(TEMP_DIR, f"{class_name}.java")  # ← named correctly

    with open(java_file, "w") as f:
        f.write(code)

    # Compile
    compile_process = subprocess.run(
        ["javac", java_file],
        capture_output=True, text=True
    )
    if compile_process.returncode != 0:
        return {
            "success": False,
            "stage": "compilation",
            "error": compile_process.stderr
        }

    # Run  (javac outputs .class into same folder as .java)
    try:
        run_process = subprocess.run(
            ["java", "-cp", TEMP_DIR, class_name],
            capture_output=True, text=True,
            timeout=5
        )
        if run_process.returncode != 0:
            return {"success": False, "stage": "runtime", "error": run_process.stderr}
        return {"success": True, "output": run_process.stdout}

    except subprocess.TimeoutExpired:
        return {"success": False, "stage": "timeout", "error": "Execution exceeded time limit"}
