# MediLogic: Academic Viva Voce Examination Guide

**Subject:** Artificial Intelligence (Unit IV: Knowledge Representation Using Logical Formalisms)  
**Total Questions:** 40 Comprehensive Questions with Rigorous Answers  

---

## Category 1: Syllabus & Academic Context (Units I, II, IV, V)

### Q1: Which syllabus unit does this mini-project primarily address?
**Answer:** The project primarily addresses **Unit IV: Knowledge Representation Using Logical Formalisms, Propositional and First-Order Predicate Calculus**. Specifically, it implements production-rule knowledge representation, propositional symbols, well-formed formulas, logical connectives (AND, OR, NOT), Modus Ponens inference, forward chaining, backward chaining, and transparent explanation facilities.

### Q2: How does this expert system connect to Unit I (Intelligent Agents)?
**Answer:** MediLogic implements a **knowledge-based intelligent agent**. It receives environmental percepts (patient symptom observations with tri-state values), maintains internal state (working memory), executes inference via logical deduction, and outputs goal-directed actions (diagnostic educational hypotheses and emergency directives).

### Q3: What is the connection between backward chaining and Unit II (State-Space Search)?
**Answer:** Backward chaining is a **goal-directed depth-first search (DFS)** through an AND/OR state-space tree of production rules. The start state is the hypothesized goal, state transitions are candidate rule prerequisite expansions, and goal states are primitive facts established in working memory.

### Q4: Why did you not implement game search algorithms like Minimax or Alpha-Beta pruning?
**Answer:** Game-playing algorithms model competitive adversarial utility optimization across two-player zero-sum environments. Medical diagnostic inference is a cooperative, deductive knowledge-based classification problem. Implementing Minimax would represent ungrounded academic inflation unrelated to clinical reasoning.

### Q5: How does the project connect to Unit V (Planning and Healthcare AI)?
**Answer:** Unit V addresses real-world applications of AI in healthcare, clinical decision support, and safety constraints. MediLogic implements an independent safety layer that prioritizes red-flag symptoms and surfaces emergency directives regardless of diagnostic reasoning.

---

## Category 2: Logical Formalisms & Propositional Calculus

### Q6: What is a propositional symbol in the context of MediLogic?
**Answer:** A propositional symbol is an atomic declarative statement that evaluates to a truth state. In MediLogic, symptom observations (e.g., `fever_present`, `cough_present`) and intermediate syndromes (e.g., `acute_febrile_respiratory_syndrome_supported`) are represented as propositional symbols.

### Q7: What is a Well-Formed Formula (WFF) in your rule base?
**Answer:** A WFF is a syntactically valid propositional formula constructed recursively: an atomic fact is a WFF; if $\alpha$ and $\beta$ are WFFs, then $(\neg \alpha)$, $(\alpha \land \beta)$, and $(\alpha \lor \beta)$ are WFFs. In MediLogic, rule antecedents are represented as validated JSON expression trees strictly adhering to this definition.

### Q8: What truth values does your system support, and why?
**Answer:** MediLogic supports **three explicit truth values**: `TRUE` (established present), `FALSE` (established absent), and `UNKNOWN` (unobserved or unasked). This tri-state system prevents the "Closed World Assumption," ensuring unasked questions are not erroneously treated as false.

### Q9: Which three-valued logic system is implemented?
**Answer:** **Kleene's strong logic of indeterminacy ($K_3$)**. In Kleene logic:
- $\mathbf{T} \land \mathbf{T} = \mathbf{T}$; $\mathbf{F} \land x = \mathbf{F}$; $\mathbf{U} \land \mathbf{T} = \mathbf{U}$.
- $\mathbf{T} \lor x = \mathbf{T}$; $\mathbf{F} \lor \mathbf{F} = \mathbf{F}$; $\mathbf{U} \lor \mathbf{F} = \mathbf{U}$.
- $\neg \mathbf{T} = \mathbf{F}$; $\neg \mathbf{F} = \mathbf{T}$; $\neg \mathbf{U} = \mathbf{U}$.

### Q10: What is Modus Ponens and how is it used in your system?
**Answer:** Modus Ponens (Rule of Detachment) states that given premise $P$ and conditional $P \to Q$, one can infer $Q$:
$$\frac{P, \quad P \to Q}{Q}$$
In our forward chaining engine, each production rule represents a material conditional $\text{Antecedent} \to \text{Consequent}$. When the antecedent evaluates to `TRUE`, Modus Ponens fires the rule and detaches the consequent fact into working memory.

### Q11: What is Modus Tollens, and is it implemented?
**Answer:** Modus Tollens states that given $\neg Q$ and $P \to Q$, one can infer $\neg P$. While covered in Unit IV theory, production rule engines traditionally use Modus Ponens for forward deduction. Modus Tollens is not automatically applied because medical rules are not necessarily biconditionals ($P \leftrightarrow Q$); the absence of a symptom does not universally negate every potential cause if multiple causes exist.

### Q12: Did you implement First-Order Predicate Logic (FOL) or Resolution?
**Answer:** No. Full first-order resolution with Robinson's unification was not implemented. To maintain academic honesty, the report clearly documents FOL and resolution refutation as theoretical background. Propositional production rules were deliberately chosen because they provide direct, inspectable, human-readable causal explanation trails that match clinical diagnostic reasoning.

---

## Category 3: Forward Chaining Algorithm & Implementation

### Q13: Define forward chaining in one sentence.
**Answer:** Forward chaining is a data-driven, bottom-up inference strategy that starts with known facts and iteratively applies Modus Ponens to applicable rules, adding new consequents to working memory until a fixed point is reached.

### Q14: What is a "fixed point" in forward chaining?
**Answer:** A fixed point is the state of saturation where a full evaluation pass over all production rules yields zero new facts. At this point, working memory is closed under rule deduction, and the algorithm halts.

### Q15: How does your forward chaining engine prevent infinite loops on cyclic rules?
**Answer:** First, by maintaining an `already_fired_rule_ids` set so a rule whose consequent is already derived does not refire redundantly. Second, through a monotonicity property (facts are only added, never retracted). Third, by enforcing a hard safety limit (`max_iterations = 50`).

### Q16: How does forward chaining handle duplicate facts?
**Answer:** Before adding an inferred consequent to working memory, the engine checks whether that exact propositional fact symbol is already present with the same truth value. If so, it updates provenance metadata without duplicating the working memory entry.

### Q17: Give an example of multi-step chaining in your rule base.
**Answer:** 
1. Level 1: `fever_present` $\land$ `cough_present` $\land$ `fatigue_present` fires **R001**, deriving `acute_febrile_respiratory_syndrome_supported`.
2. Level 2: `acute_febrile_respiratory_syndrome_supported` $\land$ `body_aches_present` fires **R002**, deriving `influenza_like_illness_supported`.
3. Level 3: `influenza_like_illness_supported` $\land$ `high_fever_present` $\land$ `chills_present` fires **R003**, deriving `severe_influenza_like_pattern_supported`.

### Q18: What is the time complexity of forward chaining?
**Answer:** If there are $R$ rules, $F$ facts, and each rule antecedent has at most $k$ terms, the engine evaluates at most $R$ rules per iteration over at most $R$ iterations. The worst-case time complexity is $O(R^2 \cdot k)$.

### Q19: Where is forward chaining implemented in the source code?
**Answer:** In `engine/forward_chaining.py` within the `ForwardChainingEngine` class and its `run()` method.

---

## Category 4: Backward Chaining Algorithm & State-Space Search

### Q20: Define backward chaining in one sentence.
**Answer:** Backward chaining is a goal-directed, top-down inference strategy that starts with a hypothesized goal, finds rules concluding that goal, and recursively attempts to prove the prerequisite subgoals.

### Q21: What are the three possible outcomes of a backward chaining goal evaluation?
**Answer:**
1. `SUPPORTED`: Conclusively proven `TRUE` through direct facts or deductive rule firing.
2. `CONTRADICTED_OR_FAILED`: Conclusively refuted or explicitly contradicted by known facts.
3. `UNRESOLVED_UNKNOWN`: Unproven because one or more necessary prerequisites remain unknown (unobserved) without explicit contradiction.

### Q22: Why is it critical that an unproven goal is NOT automatically classified as FALSE?
**Answer:** In clinical diagnosis, the absence of evidence is not evidence of absence. If a patient has not yet had a blood test or temperature check, the system must report that the condition is unverified due to missing evidence, rather than falsely telling the patient they do not have the condition.

### Q23: How does your backward chaining engine detect circular dependencies?
**Answer:** It maintains an `active_goal_stack` representing the current path in the proof tree. When a subgoal is called, the engine checks whether that symbol is already in `active_goal_stack`. If present, it flags `CYCLE_DETECTED` and immediately terminates that branch.

### Q24: How does backward chaining evaluate an OR expression?
**Answer:** It iterates over alternative disjunctive branches. If any branch succeeds (`SUPPORTED`), the OR expression succeeds immediately (short-circuit proof). It only fails if all branches fail or are contradicted.

### Q25: How does backward chaining evaluate an AND expression?
**Answer:** All conjuncts must be proven `SUPPORTED`. If any conjunct is contradicted (`FALSE`), the entire conjunction fails immediately. If some conjuncts are `UNKNOWN` and none are `FALSE`, the conjunction evaluates to `UNRESOLVED_UNKNOWN`.

### Q26: What is fact memoization in backward chaining?
**Answer:** When a subgoal is successfully proven through rule deduction, the derived fact is cached in working memory. Subsequent rules that share this prerequisite can retrieve it in $O(1)$ time without repeating the recursive proof subtree.

### Q27: Where is backward chaining implemented in the codebase?
**Answer:** In `engine/backward_chaining.py` within the `BackwardChainingEngine` class.

---

## Category 5: Architecture, Safety & Engineering Design

### Q28: Describe the overall architecture of MediLogic.
**Answer:** MediLogic follows a strict modular 5-layer architecture:
1. **Data Layer (`data/`):** Declarative JSON schemas for symptoms, rules, conditions, and references.
2. **Evaluation Layer (`engine/rule_evaluator.py`):** Kleene K3 logical calculus.
3. **Reasoning Layer (`engine/`):** Independent Forward Chaining, Backward Chaining, and Safety Engines.
4. **Audit Layer (`engine/explanation.py`):** Trace transformation and proof tree generation.
5. **Presentation Layer (`app.py`, `ui/`):** Streamlit healthcare interface with custom CSS.

### Q29: How does the Independent Safety Layer work?
**Answer:** Implemented in `engine/safety.py`, the `SafetyEngine` inspects working facts for configured life-threatening "red flag" symptoms (e.g., chest pain, severe shortness of breath, sudden neurological deficit). It operates autonomously from the diagnosis engines, meaning no rule failure or diagnostic conclusion can suppress an emergency triage alert.

### Q30: What is the purpose of the Explanation Engine?
**Answer:** Located in `engine/explanation.py`, it translates raw internal execution traces into human-readable clinical narratives, answering:
- *Why did rule X fire?* (Lists all satisfied antecedents and Modus Ponens detachment).
- *Why did rule Y fail to fire?* (Pinpoints missing or contradicting symptoms).
- *What evidence is missing to confirm hypothesis Z?*

### Q31: How do you validate the knowledge base at startup?
**Answer:** In `engine/knowledge_base.py`, `KnowledgeBase._validate_integrity()` verifies:
- Uniqueness of all rule and symptom IDs.
- Valid existence of all bibliographic references in `references.json`.
- Recursive syntactic validity of all antecedent expression trees (ensuring operators and leaf facts are valid strings).

### Q32: What automated testing did you perform?
**Answer:** We wrote 42 automated Pytest unit and integration tests covering knowledge base validation, Kleene logic, forward chaining, backward chaining, safety red-flag triage, and cross-algorithm consistency. All 42 tests pass with 100% success rate.

---

## Category 6: Medical Boundaries, Ethics & MYCIN Comparison

### Q33: How does MediLogic relate to the historical MYCIN system (1976)?
**Answer:** Developed at Stanford by Edward Shortliffe, MYCIN was the seminal rule-based medical expert system for diagnosing blood infections (bacteremia and meningitis). MediLogic adopts MYCIN's core architectural paradigms:
- Strict separation of knowledge base from inference engine.
- Step-by-step explainability facility.
- Multi-step rule chaining.

### Q34: What is the main technical difference between MediLogic and original MYCIN?
**Answer:** MYCIN used ad-hoc **Certainty Factors (CFs)** between -1.0 and +1.0 to model probabilistic uncertainty. MediLogic implements deterministic **three-valued propositional logic ($K_3$)**. MediLogic does not assign arbitrary numeric percentages to diagnoses because clinical probabilities cannot be scientifically stated without empirical clinical validation studies.

### Q35: Why does MediLogic refrain from computing diagnostic probabilities?
**Answer:** In medical ethics, assigning an arbitrary confidence percentage (e.g. "87% probability of flu") without an epidemiological validation study creates a dangerous illusion of clinical precision. MediLogic ethically reports logical support: whether clinical criteria are met, contradicted, or unresolved.

### Q36: Does MediLogic prescribe medications or clinical treatments?
**Answer:** Absolutely not. MediLogic is an educational engineering system designed to demonstrate symbolic AI and logic formalisms. Prescribing medical treatments requires medical board certification and pharmacovigilance beyond the scope of a computer engineering mini-project.

### Q37: Can the system rule out a disease simply because its rule did not fire?
**Answer:** No. In clinical reasoning, failure of a rule to fire merely indicates that the system's codified criteria were not satisfied with the available facts. It does not establish that the patient is free of the condition.

### Q38: When is Forward Chaining preferred over Backward Chaining in clinical practice?
**Answer:** Forward chaining is preferred when an unconstrained set of observations is collected (e.g., routine intake triage or laboratory panel screening) and the clinician wants to know *all* possible syndromic conclusions that can be deduced. Backward chaining is preferred when evaluating a specific suspected differential diagnosis (e.g., "Does this patient have Acute Gastroenteritis?").

### Q39: What external AI APIs or Machine Learning libraries does MediLogic use?
**Answer:** None. MediLogic contains **zero external AI APIs, zero Large Language Models, and zero black-box neural networks**. All inferences are generated deterministically by pure Python algorithms executing classical symbolic logic over verified JSON rule definitions.

### Q40: What are the primary future enhancements for this project?
**Answer:**
1. Integration of Fuzzy Logic or Dempster-Shafer theory for handling graduated symptom severities (e.g., mild vs severe fever).
2. Knowledge base authoring interface allowing clinicians to graphically author rules without touching JSON.
3. Translation of production rules into First-Order Predicate Logic with temporal constraints (e.g., "symptom onset duration $\le 7$ days").
