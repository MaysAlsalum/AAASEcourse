from typing import TypedDict
from urllib import response
from pathlib import Path

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END

import re

import os



# LLM Configuration

load_dotenv()


llm = ChatOpenAI(

    api_key=os.getenv("OPENAI_API_KEY"),

    base_url=os.getenv("LLM_BASE_URL"),

    model=os.getenv("LLM_MODEL"),

    temperature=0
)



# Define the state structure for the workflow
# Shared State

class ResumeState(TypedDict):

    resume: str

    analysis: str

    ats_score: int

    ats_feedback: str

    improved_resume: str

    

# Helper Functions

# Load Resume Function
def load_resume(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()




# Save Report Function

def save_report(state: ResumeState):

    report = f"""
============================================================
ATS SCORE
============================================================

{state["ats_score"]}

============================================================
ATS FEEDBACK
============================================================

{state["ats_feedback"]}

============================================================
IMPROVED RESUME
============================================================

{state["improved_resume"]}
"""

    output_path = BASE_DIR / "reports" / "report.txt"

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"\nReport saved to: {output_path}")






#Agents

# Agent 1 - Resume Analyzer Agent
def resume_analyzer(state: ResumeState):

    prompt = f"""
You are an expert ATS Resume Analyzer.

Analyze the following resume.

Extract:

- Education
- Skills
- Experience
- Missing Sections

Resume:

{state["resume"]}
"""

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return {
        "analysis": response.content
    }



# Agent 2 - ATS Evaluation Agent
def ats_evaluator(state: ResumeState):
    prompt = f"""
You are an ATS Resume Expert.

Based ONLY on the following resume analysis, evaluate the resume.

Provide:

1. ATS Score (0-100)

2. Strengths

3. Weaknesses

4. Suggestions for improvement

Resume Analysis:

{state["analysis"]}
"""
    
    response = llm.invoke(
    [
        HumanMessage(content=prompt)
    ]
)

    
    match = re.search(r"(\d+)\s*/\s*100", response.content)

    score = int(match.group(1)) if match else 0


    return {

        "ats_score": score,

        "ats_feedback": response.content
    }




# Agent 3 - Resume Improvement Agent

def improve_resume(state):
    """
    Improves the resume using the ATS feedback.
    """

    prompt = f"""
You are a professional resume writer.

Original Resume:

{state["resume"]}

ATS Feedback:

{state["ats_feedback"]}

Rewrite the resume to make it more ATS-friendly.

Requirements:
- Keep professional formatting
- Add missing sections if needed
- Improve wording
- Keep it realistic
- Return ONLY the improved resume
"""

    response = llm.invoke([
    HumanMessage(content=prompt)
    ])

    return {
        "improved_resume": response.content
    }





# Build LangGraph Workflow

builder = StateGraph(ResumeState)

# Add nodes for each agent
builder.add_node("resume_analyzer", resume_analyzer)

builder.add_node("ats_evaluator", ats_evaluator)

builder.add_node("improve_resume", improve_resume)


# Add edges to define the workflow
builder.add_edge(START, "resume_analyzer")

builder.add_edge("resume_analyzer", "ats_evaluator")

builder.add_edge("ats_evaluator", "improve_resume")

builder.add_edge("improve_resume", END)


graph = builder.compile()












## Main Program
BASE_DIR = Path(__file__).parent

resume = load_resume(BASE_DIR / "resumes" / "sample_resume.txt")

state = {
    "resume": resume,
    "analysis": "",
    "ats_score": 0,
    "ats_feedback": "",
    "improved_resume": ""
}

result = graph.invoke(state)

save_report(result)



print("=" * 60)
print("ATS SCORE")
print("=" * 60)
print(result["ats_score"])

print("\n" + "=" * 60)
print("ATS FEEDBACK")
print("=" * 60)
print(result["ats_feedback"])

print("\n" + "=" * 60)
print("IMPROVED RESUME")
print("=" * 60)
print(result["improved_resume"])


"""
# Agent 1
analysis_result = resume_analyzer(state)
state.update(analysis_result)

# Agent 2
ats_result = ats_evaluator(state)
state.update(ats_result)

# Agent 3
improve_result = improve_resume(state)
state.update(improve_result)
"""


