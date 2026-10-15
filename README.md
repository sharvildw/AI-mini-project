# MediLogic: Medical Diagnosis Rule-Based Expert System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Framework: Streamlit](https://img.shields.io/badge/framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Tests: Pytest 42 Passed](https://img.shields.io/badge/tests-42%20passed-brightgreen.svg)](docs/TEST_REPORT.md)
[![Academic Syllabus: Unit IV](https://img.shields.io/badge/curriculum-AI%20Unit%20IV-teal.svg)](docs/SYLLABUS_MAPPING.md)

**Academic Subject:** Artificial Intelligence  
**Primary Curriculum Unit:** **Unit IV — Knowledge Representation Using Logical Formalisms, Propositional and First-Order Predicate Calculus**  
**Engineering Discipline:** Computer Science & Engineering (B.E. / B.Tech Mini-Project)  

---

## 🌟 Executive Summary

**MediLogic** is an autonomous, explainable, rule-based medical expert system developed from first principles to demonstrate classical symbolic artificial intelligence. Unlike opaque machine learning models or hallucination-prone Large Language Models, MediLogic performs **deterministic, inspectable logical deduction** where every conclusion is traceable back to verified medical guidelines and formal logical inference rules (Modus Ponens).

### Key Architectural Highlights
1. **Propositional Logic & Well-Formed Formulas:** 34 symptoms and intermediate syndromes modeled as propositional symbols combined with logical connectives ($\land, \lor, \neg$).
2. **Kleene Three-Valued Logic ($K_3$):** Strict evaluation over explicit `TRUE`, `FALSE`, and `UNKNOWN` states, eliminating fallacious closed-world assumptions.
3. **Data-Driven Forward Chaining:** Iterative Modus Ponens application deriving all reachable working memory facts until fixed-point saturation.
4. **Goal-Directed Backward Chaining:** Recursive depth-first proof search over an AND/OR state-space with active call-stack cycle detection and tri-state goal resolution.
5. **Autonomous Clinical Safety Layer:** Non-suppressible monitor detecting life-threatening red flags (chest pain, acute dyspnea, stroke signs) and issuing immediate hospital triage directives.
6. **Transparent Explanation Subsystem:** Step-by-step audit narratives explaining *why* rules fired, *why* rules failed, and *what* prerequisites are missing.
7. **Professional Streamlit Web Interface:** Healthcare-themed navy/teal UI featuring 1-click clinical presets, interactive proof trees, and side-by-side comparative benchmarking.

---

## 📁 Repository Directory Structure

```text
d:\AI/
├── app.py                      # Main Streamlit web application
├── requirements.txt            # Project dependencies (Streamlit, Pytest)
├── pytest.ini                  # Pytest configuration
├── README.md                   # Project overview & execution guide
├── .gitignore                  # Git ignore rules
│
├── data/                       # Declarative Knowledge Base
│   ├── symptoms.json           # 34 Structured propositional symptoms
│   ├── rules.json              # 21 Multi-tier production rules
│   ├── conditions.json         # 8 Educational syndromic condition hypotheses
│   └── references.json         # 7 Authoritative medical reference citations
│
├── engine/                     # Core Symbolic AI Engines
│   ├── __init__.py             # Module exports
│   ├── knowledge_base.py       # Knowledge base loader & integrity validator
│   ├── rule_evaluator.py       # Kleene 3-valued (K3) logical calculus
│   ├── forward_chaining.py     # Data-driven Modus Ponens forward deduction
│   ├── backward_chaining.py    # Goal-directed backward proof with cycle detection
│   ├── explanation.py          # Audit narrative & proof tree generator
│   └── safety.py               # Autonomous emergency red-flag triage monitor
│
├── ui/                         # Presentation Layer
│   ├── __init__.py             # UI module exports
│   ├── styles.py               # Custom CSS design system (Navy & Teal theme)
│   └── components.py           # Reusable cards, badges, banners & case presets
│
├── tests/                      # Automated Verification Test Suite
│   ├── __init__.py
│   ├── test_knowledge_base.py  # 9 KB validation & schema tests
│   ├── test_rule_evaluator.py  # 12 Kleene 3-valued logic tests
│   ├── test_forward_chaining.py# 7 Forward chaining & cycle tests
│   ├── test_backward_chaining.py# 7 Backward chaining & proof tests
│   ├── test_safety.py          # 4 Emergency triage tests
│   └── test_integration.py     # 3 Cross-algorithm consistency tests
│
└── docs/                       # Academic Deliverables & Diagrams
    ├── SYLLABUS_MAPPING.md     # Authoritative syllabus alignment matrix
    ├── PROJECT_REPORT.md       # Exhaustive 33-section academic project report
    ├── ALGORITHMS.md           # Mathematical formalisms, pseudocode & complexity
    ├── TEST_REPORT.md          # 42/42 Pytest execution log & test matrix
    ├── VIVA_QUESTIONS.md       # 40 High-yield viva questions with model answers
    ├── USER_MANUAL.md          # User & developer guide + rule authoring tutorial
    ├── REFERENCES.md           # Annotated clinical & AI bibliography
    └── diagrams/               # System architecture & Mermaid flowcharts
        ├── architecture.mermaid
        ├── forward_chaining_flowchart.mermaid
        ├── backward_chaining_flowchart.mermaid
        ├── dfd.mermaid
        ├── use_case.mermaid
        └── rule_dependency.mermaid
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure Python 3.11 or newer is installed on your workstation.

### 2. Environment Setup & Dependency Installation
Open your terminal in the workspace root (`d:\AI`):
```powershell
# Create local virtual environment
python -m venv .venv

# Activate and install dependencies
.\.venv\Scripts\pip install -r requirements.txt
```

### 3. Run Automated Pytest Suite
```powershell
.\.venv\Scripts\pytest -v
```
**Expected Output:** `42 passed in 0.61s` (100% Pass Rate).

### 4. Launch the MediLogic Web Interface
```powershell
.\.venv\Scripts\streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🩺 Clinical Domains Covered

MediLogic encodes educational diagnostic criteria from authoritative public health standards:
- **Influenza-Like Illness (ILI):** WHO GISRS case definitions (fever $\ge 38^\circ\text{C}$, cough, fatigue, myalgia, rapid onset).
- **Common Cold:** CDC clinical criteria (nasal congestion, pharyngitis, sneezing, absence of high fever).
- **Allergic Rhinitis:** AAAAI practice parameters (sneezing, watery rhinorrhea, ocular pruritus, allergen trigger).
- **Migraine Cephalalgia:** International Headache Society ICHD-3 criteria (unilateral throbbing pain, photophobia, nausea).
- **Acute Gastroenteritis:** American College of Gastroenterology guidelines (watery diarrhea, vomiting, abdominal cramps).
- **Urinary Tract Infection:** European Association of Urology guidelines (dysuria, frequency, urgency, flank pain).
- **Emergency Red Flags:** ACEP guidelines (crushing chest pain, severe dyspnea, acute neurological deficit, meningeal stiffness, acute abdomen).

---

## 📖 Academic Documentation Links

- **[Syllabus Mapping Matrix](docs/SYLLABUS_MAPPING.md):** Exact alignment with Unit I, II, IV, and V.
- **[Full Academic Project Report](docs/PROJECT_REPORT.md):** 33-section formal report with certificate and acknowledgements.
- **[Algorithms & Mathematical Specs](docs/ALGORITHMS.md):** Formal logic derivations, pseudocode, and proofs.
- **[Automated Test Report](docs/TEST_REPORT.md):** Verification logs and test matrices.
- **[Viva Voce Examination Questions](docs/VIVA_QUESTIONS.md):** 40 in-depth viva questions & answers.
- **[User & Developer Manual](docs/USER_MANUAL.md):** UI walkthrough and knowledge base authoring guide.
- **[Annotated Bibliography](docs/REFERENCES.md):** Authoritative citations.

---

## ⚠️ Academic & Medical Disclaimer
MediLogic is an **academic computer engineering mini-project** built to demonstrate knowledge representation and logical inference. It is **NOT** a certified medical diagnostic device, does not prescribe pharmaceuticals, and must never replace examination by a licensed medical professional.
