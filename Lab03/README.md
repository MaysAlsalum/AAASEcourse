# Enterprise AI Resume Reviewer

## Description

This project is a multi-agent AI system built using LangGraph and LangChain.

The application analyzes a resume, evaluates its ATS compatibility, and generates an improved version.

---

## Technologies

- Python
- LangGraph
- LangChain
- OpenRouter
- ChatOpenAI

---

## AI Agents

### 1. Resume Analyzer

Analyzes the resume and extracts important information.

### 2. ATS Evaluator

Evaluates the resume and generates an ATS score with feedback.

### 3. Resume Improvement Agent

Rewrites the resume using the ATS recommendations.

---

## Workflow

Resume

↓

Resume Analyzer

↓

ATS Evaluator

↓

Resume Improvement

↓

Final Report

---

## Run

```bash
python resume_reviewer.py
```