# MediLogic: Complete User & Developer Manual

**Application Name:** MediLogic  
**Version:** 1.0.0  
**Technology:** Python 3.11+, Streamlit, Pytest  

---

## 1. System Requirements & Prerequisites

- **Operating System:** Windows 10/11, macOS, or Linux.
- **Python:** Python 3.11 or newer (Verified on Python 3.13.6).
- **Disk Space:** Less than 100 MB.
- **Dependencies:** Listed in `requirements.txt`:
  - `streamlit >= 1.36.0`
  - `pytest >= 8.0.0`
- **Network Requirements:** Runs 100% locally. Zero internet access or API keys required during runtime.

---

## 2. Installation & Quick Start

### Step 1: Open Terminal in Project Directory
```powershell
cd d:\AI
```

### Step 2: Initialize Virtual Environment (If not already created)
```powershell
python -m venv .venv
```

### Step 3: Install Required Dependencies
```powershell
.\.venv\Scripts\pip install -r requirements.txt
```

### Step 4: Run Automated Verification Tests
```powershell
.\.venv\Scripts\pytest -v
```
You should see:
```text
============================= 42 passed in 0.61s ==============================
```

### Step 5: Launch the MediLogic Web Interface
```powershell
.\.venv\Scripts\streamlit run app.py
```
Streamlit will automatically open your default browser at:
`http://localhost:8501`

---

## 3. User Interface Walkthrough

### 3.1 Executive Dashboard (`📊 Executive Dashboard`)
- **Top Hero:** Academic project information, primary syllabus unit badge, and educational notice.
- **System Metrics:** Dynamic counts of symptoms, rules, target hypotheses, and medical citations.
- **System Architecture:** Visual Mermaid flowchart illustrating how user inputs flow into working memory, the independent safety monitor, and dual inference engines.
- **Quick Test Presets:** Six 1-click clinical cases (Influenza, Severe ILI, Common Cold, Allergic Rhinitis, Migraine, Gastroenteritis) that instantly populate working memory for demonstration.

### 3.2 Symptom Assessment (`🩺 Symptom Assessment`)
- **Tri-State Radio Buttons:** Every symptom can be explicitly marked as:
  - `PRESENT (TRUE)`: Symptom is confirmed experienced by patient.
  - `ABSENT (FALSE)`: Explicitly verified that patient does NOT have this symptom.
  - `UNKNOWN`: Unchecked / unobserved symptom.
- **Search Filter:** Type keywords (e.g., `throat`, `headache`, `fever`) to quickly filter the 34 symptoms.
- **Categorized Expanders:** Symptoms grouped logically into Respiratory, Allergic, Neurological, Gastrointestinal, Urological, and Emergency Signs.
- **Immediate Emergency Banner:** If any red-flag symptom is set to `PRESENT`, a prominent red emergency directive is displayed immediately at the top of the interface.

### 3.3 Forward Chaining (`⏩ Forward Chaining`)
- **Action:** Click `⚡ Execute Forward Chaining Now`.
- **Results Card:** Displays all derived intermediate syndromic facts and final supported educational hypotheses.
- **Detailed Audit Trail:** Expandable cards showing why each rule fired (Modus Ponens) or failed (identifying missing or contradicting facts).
- **Filter Controls:** Toggle between showing all rules, only fired rules, or only non-fired rules.

### 3.4 Backward Chaining (`⏪ Backward Chaining`)
- **Goal Selection:** Pick any target educational hypothesis from the dropdown (e.g. `influenza_like_illness_supported`).
- **Action:** Click `🔍 Prove Goal`.
- **Proof Outcome Badge:** Conclusively reports `SUPPORTED`, `UNRESOLVED (INSUFFICIENT EVIDENCE)`, or `CONTRADICTED / FAILED`.
- **Missing Prerequisites Box:** Lists the exact symptoms that are missing from working memory to prove the hypothesis.
- **Proof Tree Visualizer:** Pre-formatted tree displaying recursive subgoals, candidate rules, and sub-evaluations.

### 3.5 Algorithm Comparison (`⚖️ Algorithm Comparison`)
- **Side-by-Side View:** Runs both Forward and Backward chaining against the exact same working memory facts.
- **Comparison Table:** Highlights the differences in search paradigm (bottom-up vs top-down), rule traversal order, and steps explored.
- **Agreement Metric:** Confirms whether both algorithms reach harmonious conclusions on the target goal.

### 3.6 Knowledge Base Explorer (`📚 Knowledge Base Explorer`)
- Browse all 21 production rules with readable IF-THEN text and raw JSON expression trees.
- Browse all 34 symptoms, 8 condition hypotheses, and 7 authoritative medical citations.
- View interactive multi-step chaining graph (R001 $\to$ R002 $\to$ R003).

### 3.7 Academic Project & Viva Guide (`🎓 Academic Project & Viva`)
- Authoritative syllabus mapping table.
- Mathematical formalisms and Modus Ponens derivations.
- Curated top 15 high-yield viva questions with detailed model answers.

---

## 4. How to Extend the Knowledge Base

MediLogic uses declarative JSON files in `data/`. You can add new symptoms and rules without modifying a single line of inference engine code!

### Adding a New Symptom (`data/symptoms.json`)
Append a new JSON object:
```json
{
  "id": "loss_of_smell_present",
  "name": "Anosmia / Loss of Smell",
  "category": "Respiratory & Constitutional",
  "description": "Sudden partial or complete loss of the sense of smell.",
  "question": "Have you noticed a sudden loss or reduction in your sense of smell?",
  "is_emergency": false
}
```

### Adding a New Production Rule (`data/rules.json`)
Append a new rule object:
```json
{
  "id": "R022",
  "name": "Viral Anosmia Respiratory Syndrome",
  "category": "Respiratory",
  "readable_text": "IF loss_of_smell_present AND cough_present THEN viral_anosmia_syndrome_supported",
  "antecedent": {
    "and": [
      {"fact": "loss_of_smell_present", "value": "TRUE"},
      {"fact": "cough_present", "value": "TRUE"}
    ]
  },
  "consequent": {
    "fact": "viral_anosmia_syndrome_supported",
    "value": "TRUE"
  },
  "explanation": "Loss of smell combined with cough strongly indicates viral olfactory neuroepithelial disruption.",
  "source": "REF_WHO_ILI"
}
```

### Startup Validation
When the application reloads, `KnowledgeBase._validate_integrity()` will automatically:
1. Verify rule ID `R022` is unique.
2. Verify all referenced facts are valid strings.
3. Validate expression tree syntax.
4. Verify source reference `REF_WHO_ILI` exists in `references.json`.

---

## 5. Troubleshooting & FAQ

### Issue: "Port 8501 is already in use"
**Solution:** Specify a custom port when launching Streamlit:
```powershell
.\.venv\Scripts\streamlit run app.py --server.port 8502
```

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Ensure you are executing Streamlit via the project virtual environment:
```powershell
.\.venv\Scripts\python -m streamlit run app.py
```

### Issue: "Tests fail with KnowledgeBaseValidationError"
**Solution:** Check `data/rules.json` for syntax errors, missing brackets, duplicate IDs, or invalid operator keys.
