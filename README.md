# MediLogic: Medical Diagnosis Rule-Based Expert System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Framework: Streamlit](https://img.shields.io/badge/framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Tests: Pytest 47 Passed](https://img.shields.io/badge/tests-47%20passed-brightgreen.svg)](docs/TEST_REPORT.md)
[![Academic Syllabus: Unit IV](https://img.shields.io/badge/curriculum-AI%20Unit%20IV-teal.svg)](docs/SYLLABUS_MAPPING.md)

**Academic Subject:** Artificial Intelligence  
**Primary Curriculum Unit:** **Unit IV — Knowledge Representation Using Logical Formalisms, Propositional and First-Order Predicate Calculus**  
**Engineering Discipline:** Computer Science & Engineering (B.E. / B.Tech Mini-Project)  

---

## 🌟 Executive Summary

**MediLogic** is an autonomous, explainable, rule-based medical expert system developed from first principles to demonstrate classical symbolic artificial intelligence. Unlike opaque machine learning models or hallucination-prone Large Language Models, MediLogic performs **deterministic, inspectable logical deduction** where every conclusion is traceable back to verified medical guidelines and formal logical inference rules (Modus Ponens).

### Key Architectural Highlights
1. **Propositional Logic & Well-Formed Formulas:** 58 symptoms and intermediate syndromes modeled as propositional symbols combined with logical connectives ($\land, \lor, \neg$).
2. **Kleene Three-Valued Logic ($K_3$):** Strict evaluation over explicit `TRUE`, `FALSE`, and `UNKNOWN` states, eliminating fallacious closed-world assumptions.
3. **Data-Driven Forward Chaining:** Iterative Modus Ponens application deriving all reachable working memory facts until fixed-point saturation.
4. **Goal-Directed Backward Chaining:** Recursive depth-first proof search over an AND/OR state-space with active call-stack cycle detection and tri-state goal resolution.
5. **Differential Diagnostic Alignment:** Transparent candidate hypothesis evaluator identifying partially matching conditions with percentage alignment and missing symptoms.
6. **Autonomous Clinical Safety Layer:** Non-suppressible monitor detecting 11 life-threatening red flags (chest pain, acute dyspnea, stroke signs, syncope, hemoptysis) and issuing immediate hospital triage directives.
7. **Transparent Explanation Subsystem:** Step-by-step audit narratives explaining *why* rules fired, *why* rules failed, and *what* prerequisites are missing.
8. **Professional Streamlit Web Interface:** Healthcare-themed navy/teal UI featuring 1-click clinical presets, interactive proof trees, and side-by-side comparative benchmarking.

---

## ☁️ Deploy to Streamlit Community Cloud

Deploying MediLogic to **Streamlit Community Cloud** is free, takes under 2 minutes, and requires zero server configuration:

### Quick Deployment Steps
1. Fork or push this repository to your GitHub account (`https://github.com/sharvildw/AI-mini-project`).
2. Visit **[share.streamlit.io](https://share.streamlit.io)** and sign in with your GitHub account.
3. Click the **"New app"** button.
4. Fill in the deployment form:
   - **Repository:** `sharvildw/AI-mini-project`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** Customize your subdomain (e.g., `medilogic-ai.streamlit.app`)
5. Click **"Deploy!"**

### Pre-Configured Cloud Assets
- **`.streamlit/config.toml`**: Pre-configures the custom healthcare teal theme, headless execution, and security flags.
- **`.python-version`**: Pins the cloud runtime to Python `3.11` for rapid builds.
- **`requirements.txt`**: Minimal, lightweight dependencies (`streamlit`, `pytest`) for fast container startup.
- **`.github/workflows/ci.yml`**: Automated continuous integration running all 47 tests on push.

---

## 📁 Repository Directory Structure

```text
AI/
├── .github/workflows/ci.yml    # Continuous Integration automated test pipeline
├── .streamlit/config.toml      # Streamlit Cloud production styling & server config
├── .python-version             # Python 3.11 runtime specification
├── app.py                      # Main Streamlit web application
├── requirements.txt            # Streamlit Cloud dependencies
├── pytest.ini                  # Pytest configuration
├── README.md                   # Project overview & deployment guide
├── .gitignore                  # Git ignore rules
│
├── data/                       # Declarative Knowledge Base
│   ├── symptoms.json           # 58 Structured propositional symptoms (7 categories)
│   ├── rules.json              # 48 Multi-tier production rules (R001–R048)
│   ├── conditions.json         # 18 Clinical condition hypotheses
│   └── references.json         # 17 Authoritative medical reference citations
│
├── engine/                     # Core Symbolic AI Engines
│   ├── __init__.py             # Module exports
│   ├── knowledge_base.py       # Knowledge base loader & integrity validator
│   ├── rule_evaluator.py       # Kleene 3-valued (K3) logical calculus
│   ├── forward_chaining.py     # Data-driven Modus Ponens forward deduction
│   ├── backward_chaining.py    # Goal-directed backward proof with cycle detection
│   ├── explanation.py          # Differential evaluator, proof tree & narrative generator
│   └── safety.py               # Autonomous emergency red-flag triage monitor
│
├── ui/                         # Presentation Layer
│   ├── __init__.py             # UI module exports
│   ├── styles.py               # Custom CSS design system (Navy & Teal theme)
│   └── components.py           # Reusable cards, badges, banners & 10 case presets
│
├── tests/                      # Automated Verification Test Suite
│   ├── __init__.py
│   ├── test_knowledge_base.py  # 9 KB validation & schema tests
│   ├── test_rule_evaluator.py  # 12 Kleene 3-valued logic tests
│   ├── test_forward_chaining.py# 7 Forward chaining & cycle tests
│   ├── test_backward_chaining.py# 7 Backward chaining & proof tests
│   ├── test_safety.py          # 4 Emergency triage tests
│   └── test_integration.py     # 8 Cross-algorithm & expanded KB tests
│
└── docs/                       # Academic Deliverables & Diagrams
    ├── SYLLABUS_MAPPING.md     # Authoritative syllabus alignment matrix
    ├── PROJECT_REPORT.md       # Exhaustive 33-section academic project report
    ├── ALGORITHMS.md           # Mathematical formalisms, pseudocode & complexity
    ├── TEST_REPORT.md          # Pytest verification log & test matrix
    ├── VIVA_QUESTIONS.md       # 40 High-yield viva questions with model answers
    ├── USER_MANUAL.md          # User & developer guide + rule authoring tutorial
    ├── REFERENCES.md           # Annotated clinical & AI bibliography
    └── diagrams/               # System architecture & Mermaid flowcharts
```

---

## 🚀 Local Execution Guide

### 1. Prerequisites
Ensure Python 3.11 or newer is installed on your workstation.

### 2. Environment Setup & Dependency Installation
Open your terminal in the workspace root:
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
**Expected Output:** `47 passed in 0.81s` (100% Pass Rate).

### 4. Launch the MediLogic Web Interface
```powershell
.\.venv\Scripts\streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🩺 Clinical Domains Covered

MediLogic encodes educational diagnostic criteria from authoritative public health standards:
- **COVID-19 (SARS-CoV-2):** CDC clinical criteria (fever, dry cough, fatigue, acute anosmia/ageusia).
- **Influenza-Like Illness (ILI):** WHO GISRS case definitions (fever $\ge 38^\circ\text{C}$, cough, fatigue, myalgia, rapid onset).
- **Streptococcal Pharyngitis:** IDSA clinical guidelines (Centor criteria: sore throat, fever, tonsillar exudate, tender cervical adenopathy, absence of cough).
- **Acute Bacterial Rhinosinusitis:** AAO-HNS guidelines (purulent rhinorrhea, facial pressure/pain, nasal obstruction).
- **Acute Bronchitis:** CHEST clinical guidelines (persistent cough, sputum production, rhonchi/wheeze, absence of consolidation).
- **Asthma / Bronchospasm:** GINA global strategy guidelines (dyspnea, expiratory wheezing, chest tightness, reversibility).
- **Common Cold:** CDC clinical criteria (nasal congestion, pharyngitis, sneezing, absence of high fever).
- **Allergic Rhinitis:** AAAAI practice parameters (sneezing, watery rhinorrhea, ocular pruritus, allergen trigger).
- **Allergic Conjunctivitis:** AAO guidelines (bilateral ocular injection, watery discharge, itching).
- **Acute Otitis Media:** AAP guidelines (otalgia, fever, tympanic erythema/bulging).
- **Tension-Type Headache:** International Headache Society ICHD-3 (bilateral band-like pressing pain, absence of vomiting).
- **Migraine Cephalalgia:** International Headache Society ICHD-3 criteria (unilateral throbbing pain, photophobia, nausea).
- **Gastroesophageal Reflux Disease (GERD):** ACG guidelines (pyrosis/heartburn, acid regurgitation, postprandial symptom aggravation).
- **Acute Gastroenteritis:** ACG guidelines (watery diarrhea, vomiting, abdominal cramps).
- **Acute Invasive Enteritis:** IDSA guidelines (bloody diarrhea, severe abdominal cramps, fever).
- **Urinary Tract Infection:** EAU guidelines (dysuria, frequency, urgency, flank pain).
- **Emergency Red Flags:** ACEP guidelines (crushing/radiating chest pain, severe dyspnea, syncope, acute neurological deficit, meningeal stiffness, hemoptysis, acute abdomen).

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
