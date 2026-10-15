# MediLogic: Algorithms & Mathematical Formalisms

**Document Version:** 1.0  
**Subject:** Artificial Intelligence (Unit IV: Knowledge Representation Using Logic)  

---

## 1. Mathematical Formalisms & Logical Calculus

### 1.1 Propositional Syntax and Working Memory
Let $\mathcal{P} = \{p_1, p_2, \dots, p_N\}$ denote the finite set of propositional symptom and syndromic symbols (e.g., $p_1 = \text{fever\_present}$, $p_2 = \text{cough\_present}$).

Working memory $\mathcal{W}$ is a partial mapping from $\mathcal{P}$ to the three-valued truth set $\mathbb{T}$:
$$\mathcal{W}: \mathcal{P} \to \mathbb{T}, \quad \mathbb{T} = \{\mathbf{T}, \mathbf{F}, \mathbf{U}\}$$
where:
- $\mathbf{T}$ represents `TRUE` (confirmed present).
- $\mathbf{F}$ represents `FALSE` (confirmed absent).
- $\mathbf{U}$ represents `UNKNOWN` (unobserved, untested, or unprovided).

### 1.2 Kleene Three-Valued Logic ($K_3$)
To avoid fallacious closed-world assumptions (where unobserved symptoms are incorrectly treated as false), MediLogic implements **Kleene's strong logic of indeterminacy ($K_3$)**:

#### Negation ($\neg$)
$$\neg \mathbf{T} = \mathbf{F}, \quad \neg \mathbf{F} = \mathbf{T}, \quad \neg \mathbf{U} = \mathbf{U}$$

#### Conjunction ($\land$)
$$\alpha \land \beta = \min(\alpha, \beta) \quad \text{under order } \mathbf{F} < \mathbf{U} < \mathbf{T}$$
- $\mathbf{T} \land \mathbf{T} = \mathbf{T}$
- $\mathbf{F} \land x = \mathbf{F} \quad (\forall x \in \mathbb{T})$
- $\mathbf{U} \land \mathbf{T} = \mathbf{U}, \quad \mathbf{U} \land \mathbf{U} = \mathbf{U}$

#### Disjunction ($\lor$)
$$\alpha \lor \beta = \max(\alpha, \beta) \quad \text{under order } \mathbf{F} < \mathbf{U} < \mathbf{T}$$
- $\mathbf{T} \lor x = \mathbf{T} \quad (\forall x \in \mathbb{T})$
- $\mathbf{F} \lor \mathbf{F} = \mathbf{F}$
- $\mathbf{U} \lor \mathbf{F} = \mathbf{U}, \quad \mathbf{U} \lor \mathbf{U} = \mathbf{U}$

---

## 2. Production Rules and Modus Ponens

A production rule $R_i$ has the form:
$$R_i: \quad \text{IF } \phi_i \text{ THEN } \psi_i$$
where $\phi_i$ is a well-formed antecedent formula constructed over $\mathcal{P}$ using connectives $\{\land, \lor, \neg\}$, and $\psi_i$ is an atomic consequent assignment $(q_i = \mathbf{T})$.

### 2.1 The Rule of Detachment (Modus Ponens)
Classical Modus Ponens states:
$$\frac{\phi, \quad \phi \to \psi}{\psi}$$
In our production rule engine:
1. The antecedent expression $\phi_i$ is evaluated against current working memory $\mathcal{W}$ using Kleene semantics: $\text{val}(\phi_i, \mathcal{W}) \in \{\mathbf{T}, \mathbf{F}, \mathbf{U}\}$.
2. If and only if $\text{val}(\phi_i, \mathcal{W}) = \mathbf{T}$, rule $R_i$ fires via Modus Ponens.
3. The consequent assignment $q_i = \mathbf{T}$ is detached and committed to working memory: $\mathcal{W} \leftarrow \mathcal{W} \cup \{q_i \mapsto \mathbf{T}\}$.

---

## 3. Forward Chaining Algorithm (Data-Driven)

### 3.1 Pseudocode
```text
Algorithm: FORWARD_CHAINING
Input: Initial fact store W_0, Knowledge Base Rules R, MaxIterations M
Output: Result (WorkingMemory W, DerivedFacts D, FiredRules F, Trace T)

1. W <- W_0
2. D <- EmptyDictionary
3. F <- EmptyList
4. T <- EmptyList
5. Iteration <- 1
6. FiredRuleIDs <- EmptySet

7. WHILE Iteration <= M DO:
8.     NewFactsDerived <- 0
9.     FOR EACH Rule r IN SortByID(R) DO:
10.        IF r.id IN FiredRuleIDs THEN
11.            CONTINUE
12.        END IF
13.        
14.        EvalResult <- EVALUATE_EXPRESSION(r.antecedent, W)
15.        StepNumber <- StepNumber + 1
16.        
17.        IF EvalResult.value == TRUE THEN
18.            FiredRuleIDs.Add(r.id)
19.            F.Append(r)
20.            ConsequentFact <- r.consequent.fact
21.            ConsequentVal <- r.consequent.value
22.            
23.            IsNew <- (ConsequentFact NOT IN W) OR (W[ConsequentFact] != ConsequentVal)
24.            IF IsNew THEN
25.                NewFact <- CreateFact(ConsequentFact, ConsequentVal, source=INFERRED, rule=r.id)
26.                W[ConsequentFact] <- NewFact
27.                D[ConsequentFact] <- NewFact
28.                NewFactsDerived <- NewFactsDerived + 1
29.            END IF
30.            
31.            T.Append(CreateTraceStep(StepNumber, Iteration, r, TRUE, IsNew, EvalResult))
32.        ELSE
33.            T.Append(CreateTraceStep(StepNumber, Iteration, r, FALSE, FALSE, EvalResult))
34.        END IF
35.    END FOR
36.    
37.    IF NewFactsDerived == 0 THEN
38.        RETURN Result(W, D, F, T, termination="Fixed-Point Saturated")
39.    END IF
40.    Iteration <- Iteration + 1
41. END WHILE

42. RETURN Result(W, D, F, T, termination="Iteration Safety Limit Exceeded")
```

### 3.2 Termination Proof & Complexity
- **Monotonicity:** In our production system, fireable rules only assert positive conclusions (no rule retracts facts). Thus, working memory $\mathcal{W}$ grows monotonically: $\mathcal{W}_t \subseteq \mathcal{W}_{t+1}$.
- **Finite Horizon:** The set of propositional symbols $\mathcal{P}$ is finite ($|\mathcal{P}| = N$). A rule can fire at most once during an entire run (`already_fired_rule_ids`).
- **Fixed-Point Guarantee:** Since $|R|$ is finite, the loop must either add at least one new fact per iteration or terminate. The algorithm is guaranteed to terminate in at most $|R|$ iterations.
- **Asymptotic Time Complexity:** In each iteration, at most $|R|$ rules are evaluated. Each evaluation takes $O(k)$ where $k$ is the maximum number of terms in an antecedent expression tree. Thus, worst-case time complexity is $O(|R|^2 \cdot k)$. For $|R|=21, k \le 5$, this executes in $< 10$ milliseconds.
- **Space Complexity:** $O(|\mathcal{P}| + |R|)$ for working memory and firing set.

---

## 4. Backward Chaining Algorithm (Goal-Driven)

### 4.1 Pseudocode
```text
Algorithm: BACKWARD_CHAINING
Input: TargetGoal G, TargetValue V, WorkingMemory W, KnowledgeBase KB, MaxDepth D
Output: BackwardResult (Status, ProofTree, AppliedRules, MissingPrereqs, Trace)

Function PROVE_GOAL(G, V, CurrentDepth, ActiveStack):
1.  IF CurrentDepth > D THEN
2.      RETURN ProofNode(G, DEPTH_LIMIT_EXCEEDED)
3.  END IF
4.  
5.  // Cycle Detection Guard
6.  IF G IN ActiveStack THEN
7.      RETURN ProofNode(G, CYCLE_DETECTED, "Circular dependency detected")
8.  END IF
9.  
10. // Direct Working Memory Lookup
11. IF G IN W THEN
12.     IF W[G].value == V THEN
13.         RETURN ProofNode(G, SUPPORTED, "Direct fact match in memory")
14.     ELSE IF W[G].value != UNKNOWN THEN
15.         RETURN ProofNode(G, CONTRADICTED_OR_FAILED, "Contradicts known fact")
16.     END IF
17. END IF
18. 
19. CandidateRules <- KB.GetRulesConcluding(G, V)
20. IF CandidateRules IS EMPTY THEN
21.     MissingPrereqs.Add(G)
22.     RETURN ProofNode(G, UNRESOLVED_UNKNOWN, "No rule derives this unobserved fact")
23. END IF
24. 
25. ActiveStack.Add(G)
26. ExploredSubnodes <- EmptyList
27. AllContradicted <- TRUE
28. HasUnknown <- FALSE
29. 
30. FOR EACH Rule r IN CandidateRules DO:
31.     SubProofNode <- PROVE_EXPRESSION(r.antecedent, CurrentDepth + 1, ActiveStack)
32.     ExploredSubnodes.Append(SubProofNode)
33.     
34.     IF SubProofNode.status == SUPPORTED THEN
35.         W[G] <- CreateFact(G, V, source=INFERRED, rule=r.id)
36.         ActiveStack.Remove(G)
37.         AppliedRules.Add(r)
38.         RETURN ProofNode(G, SUPPORTED, rule=r.id, subnodes=[SubProofNode])
39.     ELSE IF SubProofNode.status == UNRESOLVED_UNKNOWN THEN
40.         AllContradicted <- FALSE
41.         HasUnknown <- TRUE
42.     END IF
43. END FOR
44. 
45. ActiveStack.Remove(G)
46. IF HasUnknown THEN
47.     RETURN ProofNode(G, UNRESOLVED_UNKNOWN, subnodes=ExploredSubnodes)
48. ELSE
49.     RETURN ProofNode(G, CONTRADICTED_OR_FAILED, subnodes=ExploredSubnodes)
50. END IF

Function PROVE_EXPRESSION(Expr, CurrentDepth, ActiveStack):
1.  IF Expr is ATOMIC (fact=f, value=v) THEN
2.      RETURN PROVE_GOAL(f, v, CurrentDepth, ActiveStack)
3.  ELSE IF Expr is AND [c1, c2, ...] THEN
4.      Children <- [PROVE_EXPRESSION(c, CurrentDepth+1, ActiveStack) for c in Expr.and]
5.      IF ANY Child in Children is FAILED/CYCLE THEN RETURN Status=CONTRADICTED_OR_FAILED
6.      IF ALL Children in Children are SUPPORTED THEN RETURN Status=SUPPORTED
7.      RETURN Status=UNRESOLVED_UNKNOWN
8.  ELSE IF Expr is OR [c1, c2, ...] THEN
9.      Children <- EmptyList
10.     FOR EACH c in Expr.or DO:
11.         ChildRes <- PROVE_EXPRESSION(c, CurrentDepth+1, ActiveStack)
12.         Children.Append(ChildRes)
13.         IF ChildRes.status == SUPPORTED THEN RETURN Status=SUPPORTED (Short-circuit!)
14.     END FOR
15.     IF ALL Children are FAILED THEN RETURN Status=CONTRADICTED_OR_FAILED
16.     RETURN Status=UNRESOLVED_UNKNOWN
17. END IF
```

### 4.2 Cycle Prevention & Depth Guard Proof
- **Active Goal Stack Invariant:** Let $\mathcal{S}$ denote `active_goal_stack`. A goal $G$ is added to $\mathcal{S}$ when investigation begins and removed upon return. If $G \in \mathcal{S}$ during a recursive call, a directed cycle $G \to \dots \to G$ exists in the goal dependency graph. The engine flags `CYCLE_DETECTED` and immediately terminates that branch.
- **Complexity:** In a tree with branching factor $b$ and max depth $D$, unpruned search is $O(b^D)$. With cycle detection and fact memoization (once proven, $G$ is cached in working memory $\mathcal{W}$), each distinct subgoal is evaluated at most once, reducing search complexity to $O(|R| \cdot k)$.

---

## 5. Independent Clinical Safety Protocol Algorithm

```text
Algorithm: CLINICAL_SAFETY_MONITOR
Input: WorkingMemory W, ConfiguredRedFlags RF
Output: SafetyReport (HasEmergency, Alerts)

1. Alerts <- EmptyList
2. FOR EACH (SymptomID, WarningData) IN RF DO:
3.     FactObj <- W.Get(SymptomID)
4.     IF FactObj != NULL AND FactObj.value == TRUE THEN
5.         Alerts.Append(CreateEmergencyAlert(SymptomID, WarningData))
6.     END IF
7. END FOR
8. 
9. HasEmergency <- (Length(Alerts) > 0)
10. RETURN SafetyReport(HasEmergency, Alerts)
```

**Non-Suppression Theorem:** Because `CLINICAL_SAFETY_MONITOR` executes directly over working memory independently of `FORWARD_CHAINING` and `BACKWARD_CHAINING`, no diagnostic conclusion, rule failure, or missing prerequisite can suppress or alter an emergency alert.
