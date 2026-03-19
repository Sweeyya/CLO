import subprocess
import json

def run_local_model(prompt: str, model: str = "phi3:mini") -> str:
    """
    Runs the local Ollama model and returns its text output.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Model error: {result.stderr}"
    except Exception as e:
        return f"Error running local model: {e}"
