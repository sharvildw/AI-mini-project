# MediLogic: Authoritative Syllabus Alignment Matrix

**Course:** Artificial Intelligence  
**Academic Degree:** Bachelor of Engineering / Technology in Computer Science & Engineering  
**Primary Focal Unit:** **Unit IV — Knowledge Representation Using Logical Formalisms, Propositional and First-Order Predicate Calculus**  
**Associated Units:** Unit I (Intelligent Agents & Healthcare AI), Unit II (State Space Search & Goal-Directed Problem Solving), Unit V (AI Safety & Healthcare Applications)  

---

## 1. Syllabus Mapping Summary

The following matrix provides an exact, rigorous mapping between the academic syllabus topics and the MediLogic implementation.  
To ensure absolute academic integrity:
- **Directly Implemented:** Algorithmic logic and data structures functioning directly in the Python source code and verified by automated Pytest unit tests.
- **Demonstrated Through Concrete Examples:** Concepts illustrated via interactive UI case studies or production rule schemas.
- **Theoretical Background:** Academic concepts discussed in the project documentation and report as foundational theory, without falsely claiming full algorithmic implementation (e.g., full first-order resolution theorem proving or Robinson unification).

---

## 2. Comprehensive Syllabus Mapping Table

| Unit | Exact Syllabus Topic | Academic & Project Relevance | Implementation Level | Relevant Source File(s) | Verification & Demonstration Method |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Unit I** | AI Components and Architectures | Expert system architecture comprising user interface, working memory, knowledge base, inference engine, explanation facility, and safety layer. | **Directly Implemented** | `app.py`<br>`engine/knowledge_base.py`<br>`engine/forward_chaining.py` | Architecture diagram in `docs/diagrams/architecture.mermaid`; modular Python architecture verified via automated test suite. |
| **Unit I** | Intelligent Agents and Environments | MediLogic operates as a knowledge-based, goal-driven and utility-conscious intelligent agent interacting with an episodic, discrete, partially observable environment. | **Directly Implemented** | `engine/forward_chaining.py`<br>`engine/backward_chaining.py` | Agent percepts (symptom truth states) translated into action/hypotheses; test suite `test_integration.py`. |
| **Unit I** | Goal-Oriented, Model-Based, and Reflex Agents | Comparison of forward chaining (data-driven reflex-to-deduction) versus backward chaining (goal-driven exploration). | **Directly Implemented** | `engine/forward_chaining.py`<br>`engine/backward_chaining.py` | Side-by-side execution on identical patient facts in the `⚖️ Algorithm Comparison` UI tab. |
| **Unit I** | Nature of Environments | Clinical symptom intake represents a partially observable, static, discrete, deterministic environment with tri-state truth semantics. | **Directly Implemented** | `engine/knowledge_base.py`<br>`engine/rule_evaluator.py` | Kleene K3 logic handles missing observations without making false closed-world assumptions. |
| **Unit I** | Case Study: AI in Healthcare — IBM Watson & Limitations | Contextual comparison between probabilistic/natural-language clinical systems and deterministic rule-based systems. Limitations of symbolic systems in clinical medicine. | **Theoretical Background** | `docs/PROJECT_REPORT.md` (Section 11 & 28) | Academic discussion of validation limitations, lack of clinical sensitivity/specificity without empirical validation studies. |
| **Unit II** | State-Space Search & Problem Solving | Backward chaining formalizes goal-directed depth-first search through the state space of production rules and subgoals. | **Directly Implemented** | `engine/backward_chaining.py` | Recursive traversal of candidate rules; state transitions tracked in `BackwardStepTrace`. |
| **Unit II** | Depth-First Search (DFS) | Subgoal evaluation traverses prerequisites depth-first until reaching known working memory facts or unprovable base facts. | **Directly Implemented** | `engine/backward_chaining.py` | Step-by-step depth logging (`depth` attribute) and proof tree visualization in `test_backward_chaining.py`. |
| **Unit II** | Cycle Detection & Graph Search | Production rule dependencies may contain circular loops ($A \to B$ and $B \to A$). Cycle detection prevents infinite recursion. | **Directly Implemented** | `engine/backward_chaining.py` | Active goal call stack (`active_goal_stack`) flags `CYCLE_DETECTED`; verified in `test_backward_chaining_cycle_detection()`. |
| **Unit II** | Search Termination & Resource Limits | Boundless search prevention through explicit recursion depth bounds and forward chaining iteration limits. | **Directly Implemented** | `engine/forward_chaining.py`<br>`engine/backward_chaining.py` | `max_iterations=50` and `max_depth=15`; verified in `test_forward_chaining_cyclic_rule_termination()`. |
| **Unit III** | Adversarial Search & Minimax | Game search is not applicable to medical diagnosis. Excluded to prevent academic bloat. | *Excluded by Design* | N/A | Documented in `docs/SYLLABUS_MAPPING.md` as non-applicable to medical expert systems. |
| **Unit IV** | **Introduction to Logical Formalisms** | Logical formalisms provide unambiguous syntax and formal semantics for representing medical knowledge. | **Directly Implemented** | `data/rules.json`<br>`engine/rule_evaluator.py` | Declarative JSON expression trees; validated on startup by `KnowledgeBase._validate_expression()`. |
| **Unit IV** | **Propositional Logic & Well-Formed Formulas (WFFs)** | Medical symptoms and clinical patterns are modeled as propositional symbols combined with logical connectives ($\land, \lor, \neg$). | **Directly Implemented** | `data/symptoms.json`<br>`data/rules.json`<br>`engine/rule_evaluator.py` | Kleene 3-valued truth model evaluated in `RuleEvaluator.evaluate()`; verified in `tests/test_rule_evaluator.py`. |
| **Unit IV** | **Logical Connectives (AND, OR, NOT)** | Production rule antecedents contain explicit nested conjunctions, disjunctions, and negations. | **Directly Implemented** | `engine/rule_evaluator.py` | Evaluated under Kleene K3 strong indeterminacy logic; 12 dedicated tests in `test_rule_evaluator.py`. |
| **Unit IV** | **Modus Ponens Inference Rule** | Foundation of rule firing: $(P \land (P \to Q)) \vdash Q$. When antecedent $P$ is established as `TRUE`, consequent $Q$ is deduced. | **Directly Implemented** | `engine/forward_chaining.py` | Rule firing in forward chaining explicitly logs Modus Ponens detachment in the execution trace. |
| **Unit IV** | **Modus Tollens Inference Rule** | $(\neg Q \land (P \to Q)) \vdash \neg P$. If consequent is known false and rule is biconditional or sole derivation, antecedent can be negated. | **Theoretical Background** | `docs/PROJECT_REPORT.md` (Section 16) | Discussed theoretically; not used in standard production systems where rules are one-way material implications. |
| **Unit IV** | **Forward Chaining Algorithm** | Data-driven inference repeatedly firing rules from known facts until reaching a fixed point. | **Directly Implemented** | `engine/forward_chaining.py` | `ForwardChainingEngine.run()`; multi-step chaining verified in `test_forward_chaining.py`. |
| **Unit IV** | **Backward Chaining Algorithm** | Goal-directed recursive inference starting from a target hypothesis and seeking supporting rules and subgoals. | **Directly Implemented** | `engine/backward_chaining.py` | `BackwardChainingEngine.run()`; tri-state goal resolution verified in `test_backward_chaining.py`. |
| **Unit IV** | **Medical Expert System: MYCIN** | Case study on rule-based medical expert systems; separation of knowledge base from inference engine; explanation facilities. | **Demonstrated Through Architecture** | `engine/knowledge_base.py`<br>`engine/explanation.py` | Separation of declarative rules from Python engine; transparent explanation audit trails; detailed historical comparison in report. |
| **Unit IV** | Resolution Refutation & First-Order Predicate Calculus (FOL) | Clausal normal form, unification algorithms, and universal/existential quantifiers ($\forall, \exists$). | **Theoretical Background** | `docs/PROJECT_REPORT.md` (Section 12 & 15) | Academic comparison detailing why propositional production systems were chosen over first-order resolution theorem provers for clinical explainability. |
| **Unit V** | AI in Healthcare & Ethical Safety | Independent safety protocols detecting life-threatening red-flag symptoms regardless of diagnostic reasoning. | **Directly Implemented** | `engine/safety.py` | `SafetyEngine.check_safety()` triggers non-suppressible emergency alerts; verified in `test_safety.py`. |

---

## 3. Detailed Academic Justification of Direct vs Theoretical Topics

### Why Propositional Production Rules Rather than First-Order Resolution?
1. **Explainability & Medical Transparency:** First-order resolution refutation converts formulas into Conjunctive Normal Form (CNF) and derives empty clauses ($\Box$) via indirect proof (proof by contradiction). While mathematically complete, resolution refutation produces inverted, non-intuitive proofs that clinical users and examiners cannot read as natural clinical logic. In contrast, production rules $(P \to Q)$ preserve human-intelligible causal clinical reasoning.
2. **Deterministic Predictability:** In medical expert systems, predictability and deterministic auditability are paramount. Pure first-order logic is semi-decidable (Church-Turing thesis), meaning an unprovable query may result in an infinite loop without an artificial bound. Propositional production systems over finite working memory are decidable and guaranteed to terminate at a fixed point.
3. **Open-World Tri-State Semantics:** Standard first-order resolution assumes two-valued Boolean logic. Clinical medicine requires three-valued logic (Kleene $K_3$), where unasked or unexamined symptoms remain explicitly `UNKNOWN` rather than arbitrarily assuming closed-world falsehood.

---

## 4. Viva Voce Alignment Summary
This mapping directly prepares students for external university examiner questions:
- **"Which syllabus unit does this mini-project belong to?"** &rarr; Unit IV (Knowledge Representation Using Logical Formalisms).
- **"Which inference rule justifies rule firing?"** &rarr; Modus Ponens (Rule of Detachment).
- **"Where is state-space search implemented?"** &rarr; In Backward Chaining (`engine/backward_chaining.py`), searching the rule-dependency space depth-first with cycle detection.
- **"Did you implement Resolution?"** &rarr; No, resolution is discussed as theoretical background in the project report. MediLogic implements production rules with Modus Ponens, forward chaining, and backward chaining to provide natural, transparent clinical explanations.
