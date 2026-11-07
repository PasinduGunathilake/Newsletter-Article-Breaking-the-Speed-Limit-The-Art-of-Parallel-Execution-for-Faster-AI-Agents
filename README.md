# Breaking the Speed Limit: The Art of Parallel Execution for Faster AI Agents

### Official Code Repository & Reproduction Package
**Author:** A. P. P. N. Gunathilake (Registration No: 2022/CSC/011)  
*Department of Computer Science, University of Jaffna*  


---

## Overview for Reviewers
This standalone package contains the exact, reproducible code and benchmark experiments described in the article:
**"Breaking the Speed Limit: The Art of Parallel Execution for Faster AI Agents"**.

The scripts are **100% self-contained**:
* **No API keys or external accounts required** (all network/tool delays are simulated locally).
* **No database or cloud setup required**.
* **Can be executed completely offline** on any operating system (Windows, macOS, Linux).

---

## Repository Structure
```text
├── Article/
│   ├── Breaking the Speed Limit The Art of Parallel Execution for Faster AI Agents.docx  # Word document version
│   └── Breaking_the_Speed_Limit_The_Art_of_Parallel_Execution_for_Faster_AI_Agents.pdf   # Publication-ready PDF version
├── parallel_agent.py      # Standalone Fan-Out / Fan-In LangGraph Agent implementation
├── run_comparison.py      # Sequential vs. Parallel benchmark comparison script
├── requirements.txt       # Minimal dependency specification (langgraph)
└── README.md              # Instructions for reviewers and developers
```

---

## How to Run (Step-by-Step Reproduction Guide)

### 1. Prerequisites
Ensure you have **Python 3.9 or higher** installed.

### 2. Setup Virtual Environment (Recommended)
Open a terminal in this folder and create an isolated environment:

**On Windows (PowerShell / Command Prompt):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install the single required framework (`langgraph`):
```bash
pip install -r requirements.txt
```

### 4. Execute the Scripts

#### Option A: Run the Parallel Agent (LangGraph Fan-Out / Fan-In)
```bash
python parallel_agent.py
```
* **Expected Result:** All three worker tasks (arXiv, Benchmarks, GitHub) execute concurrently across threads. Total execution time is bounded by the slowest single task (`~1.51s`), rather than their cumulative sum (`4.2s`).

#### Option B: Run the Sequential vs. Parallel Benchmark Comparison
```bash
python run_comparison.py
```
* **Expected Result:**
  * Sequential Execution: `~3.00 seconds` ($T_1 + T_2 + T_3$)
  * Parallel Fan-Out Execution: `~1.01 seconds` max(T_1, T_2, T_3)
  * **Verified Speedup: ~66% Latency Reduction!**

---

## Key Architecture Highlights in Code
1. **State Reducer (`Annotated[list[str], operator.add]`):**  
   Ensures thread safety inside LangGraph by safely appending findings from parallel workers to the shared state without race conditions.
2. **Offline Safety (`os.environ["LANGCHAIN_TRACING_V2"] = "false"`):**  
   Prevents the framework from trying to connect to remote tracing servers, ensuring instant, deterministic offline execution.
