"""
Comparison Benchmark: Sequential Execution vs. Parallel Execution (LangGraph)
-----------------------------------------------------------------------------
This script runs:
  1. A traditional Sequential Agent pattern (like ReAct: T1 + T2 + T3)
  2. A modern Parallel Fan-Out / Fan-In pattern using LangGraph

You can see the exact runtime difference live on your terminal.
"""

import os
import time
import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END

os.environ["LANGCHAIN_TRACING_V2"] = "false"


# 1. State Definition
class ResearchState(TypedDict):
    topic: str
    findings: Annotated[list[str], operator.add]


# 2. Worker definitions (simulating 1.0s API delay each)
DELAY = 1.0

def fetch_arxiv(state: ResearchState):
    print("    [Worker: arXiv] Searching...")
    time.sleep(DELAY)
    return {"findings": ["[arXiv] Found 12 recent research papers."]}

def fetch_benchmarks(state: ResearchState):
    print("    [Worker: Benchmarks] Fetching...")
    time.sleep(DELAY)
    return {"findings": ["[Benchmarks] Confirmed 60% latency reduction."]}

def fetch_github(state: ResearchState):
    print("    [Worker: GitHub] Scanning...")
    time.sleep(DELAY)
    return {"findings": ["[GitHub] Found 3 leading open-source orchestrators."]}

def synthesize(state: ResearchState):
    print("    [Synthesizer] Fusing findings into final report...")
    return {"findings": ["Synthesized report complete."]}


# 3. Build Parallel LangGraph
def build_parallel_app():
    b = StateGraph(ResearchState)
    b.add_node("arxiv", fetch_arxiv)
    b.add_node("benchmarks", fetch_benchmarks)
    b.add_node("github", fetch_github)
    b.add_node("synthesizer", synthesize)

    b.add_edge(START, "arxiv")
    b.add_edge(START, "benchmarks")
    b.add_edge(START, "github")
    b.add_edge("arxiv", "synthesizer")
    b.add_edge("benchmarks", "synthesizer")
    b.add_edge("github", "synthesizer")
    b.add_edge("synthesizer", END)
    return b.compile()


# 4. Sequential Runner
def run_sequential(topic: str):
    print("\n" + "=" * 65)
    print(">>> 1. RUNNING SEQUENTIAL AGENT (Step-by-step: ReAct Pattern)")
    print("=" * 65)
    start = time.time()
    
    state: ResearchState = {"topic": topic, "findings": []}
    
    # Run step 1
    state["findings"].extend(fetch_arxiv(state)["findings"])
    # Run step 2
    state["findings"].extend(fetch_benchmarks(state)["findings"])
    # Run step 3
    state["findings"].extend(fetch_github(state)["findings"])
    # Synthesize
    synthesize(state)
    
    elapsed = time.time() - start
    print(f"[-] Sequential Total Duration: {elapsed:.2f} seconds")
    return elapsed


# 5. Parallel Runner
def run_parallel(topic: str):
    print("\n" + "=" * 65)
    print(">>> 2. RUNNING PARALLEL AGENT (LangGraph Fan-Out / Fan-In)")
    print("=" * 65)
    
    app = build_parallel_app()
    start = time.time()
    app.invoke({"topic": topic, "findings": []})
    elapsed = time.time() - start
    
    print(f"[+] Parallel Total Duration  : {elapsed:.2f} seconds")
    return elapsed


def main():
    topic = "Parallel Execution in AI Agents"
    print("=" * 65)
    print(f"BENCHMARK: Sequential vs. Parallel for '{topic}'")
    print(f"Each of the 3 tasks has a {DELAY}s simulated API delay.")
    print("=" * 65)

    seq_time = run_sequential(topic)
    par_time = run_parallel(topic)

    speedup = ((seq_time - par_time) / seq_time) * 100
    print("\n" + "=" * 65)
    print("BENCHMARK RESULTS:")
    print(f"  * Sequential Duration : {seq_time:.2f}s  (Formula: T1 + T2 + T3)")
    print(f"  * Parallel Duration   : {par_time:.2f}s  (Formula: max(T1, T2, T3))")
    print(f"  * Speed Improvement   : {speedup:.1f}% FASTER!")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
