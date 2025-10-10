# CLO ♻️  
**Carbon-Lite Orchestration (CLO)** is an AI backend that dynamically measures and minimizes the energy cost of each model inference.  
It routes tasks between models and tracks estimated energy and CO₂ emissions per request — all running through Azure Functions and local inference.

---

## 🚀 Tech Stack
- **Azure Functions (Python)** – API and backend orchestration  
- **Ollama (Local LLM runtime)** – runs lightweight and large models  
- **Azure SDK + Carbon SDK (planned)** – real-time carbon data tracking  
- **Python** – measurement logic and routing between models  

---

## ⚙️ Getting Started
```bash
# clone the repo
git clone https://github.com/Sweeyya/CLO.git
cd CLO

# create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# start Azure Function
func start
