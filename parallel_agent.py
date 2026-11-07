"""
Breaking the Speed Limit: The Art of Parallel Execution for Faster AI Agents
------------------------------------------------------------------------
LangGraph Implementation: Fan-Out / Fan-In Parallel Execution Architecture.

In this example, three independent worker nodes (arXiv, Benchmarks, GitHub)
simulate fetching data concurrently. LangGraph's engine executes them in
parallel across worker threads, converging at the Synthesizer barrier.
"""

import os
import time
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END

# Disable remote LangSmith tracing for local offline benchmark runs
os.environ["LANGCHAIN_TRACING_V2"] = "false"


# =====================================================================
# 1. SHARED STATE DEFINITION
# =====================================================================
# operator.add acts as a state reducer: it automatically appends items
# returned from parallel workers into the 'findings' list without overwriting.
class ResearchState(TypedDict):
    topic: str
    findings: Annotated[list[str], operator.add]


# =====================================================================
# 2. WORKER NODES (SIMULATING EXTERNAL API / NETWORK DELAYS)
# =====================================================================
def fetch_arxiv(state: ResearchState):
    print("  -> [Worker 1: arXiv] Searching research papers...")
    time.sleep(1.5)  # Simulated API delay (e.g. arXiv REST API)
    print("  <- [Worker 1: arXiv] Search complete.")
    return {"findings": ["[arXiv] Found 12 recent research papers on parallel agents."]}


def fetch_benchmarks(state: ResearchState):
    print("  -> [Worker 2: Benchmarks] Fetching performance benchmarks...")
    time.sleep(1.2)  # Simulated API delay (e.g. Eval benchmarks)
    print("  <- [Worker 2: Benchmarks] Search complete.")
    return {"findings": ["[Benchmarks] Confirmed 60% latency reduction via Fan-Out."]}


def fetch_github(state: ResearchState):
    print("  -> [Worker 3: GitHub] Scanning open-source repositories...")
    time.sleep(1.5)  # Simulated API delay (e.g. GitHub API)
    print("  <- [Worker 3: GitHub] Search complete.")
    return {"findings": ["[GitHub] Found 3 leading open-source orchestrators."]}


# =====================================================================
# 3. SYNTHESIZER NODE (THE FAN-IN BARRIER)
# =====================================================================
def synthesize(state: ResearchState):
    print("\n  [Synthesizer: Brain] Synthesizing all parallel findings...")
    report = (
        f"\n======================================================\n"
        f" SUMMARY REPORT: '{state['topic']}'\n"
        f"======================================================\n"
        + "\n".join(f"  * {item}" for item in state["findings"])
        + f"\n======================================================\n"
    )
    return {"findings": [report]}


# =====================================================================
# 4. BUILD THE LANGGRAPH WORKFLOW (DIRECTED ACYCLIC GRAPH - DAG)
# =====================================================================
def create_agent_graph():
    builder = StateGraph(ResearchState)

    # Register Nodes
    builder.add_node("arxiv", fetch_arxiv)
    builder.add_node("benchmarks", fetch_benchmarks)
    builder.add_node("github", fetch_github)
    builder.add_node("synthesizer", synthesize)

    # Fan-Out: Connect START to all three workers simultaneously
    builder.add_edge(START, "arxiv")
    builder.add_edge(START, "benchmarks")
    builder.add_edge(START, "github")

    # Fan-In: All three workers must complete before reaching the synthesizer
    builder.add_edge("arxiv", "synthesizer")
    builder.add_edge("benchmarks", "synthesizer")
    builder.add_edge("github", "synthesizer")
    builder.add_edge("synthesizer", END)

    return builder.compile()


# =====================================================================
# 5. EXECUTION & BENCHMARK
# =====================================================================
def main():
    print("=" * 65)
    print("Starting Parallel AI Agent Execution (LangGraph Fan-Out / Fan-In)")
    print("=" * 65)

    app = create_agent_graph()

    start_time = time.time()
    result = app.invoke({"topic": "Parallel AI Agent Architectures", "findings": []})
    duration = time.time() - start_time

    print(result["findings"][-1])
    print(f"[+] Total Execution Time: {duration:.2f} seconds")
    print(f"[+] Notice: Bound by max(1.5s, 1.2s, 1.5s) ~1.5s, NOT the sum (4.2s)!\n")


if __name__ == "__main__":
    main()
