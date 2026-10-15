"""Goal-Directed Backward Chaining Inference Engine.

Performs recursive, goal-directed depth-first exploration of rules and subgoals
to prove or disprove educational hypotheses, featuring cycle detection, tri-state
resolution (SUPPORTED, CONTRADICTED, UNRESOLVED_UNKNOWN), and proof tree generation.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from .knowledge_base import Fact, FactSource, KnowledgeBase, Rule, TruthValue


class GoalStatus(str, Enum):
    """Rigorous evaluation outcome for a backward-chaining goal or subgoal."""
    SUPPORTED = "SUPPORTED"
    CONTRADICTED_OR_FAILED = "CONTRADICTED_OR_FAILED"
    UNRESOLVED_UNKNOWN = "UNRESOLVED_UNKNOWN"
    CYCLE_DETECTED = "CYCLE_DETECTED"
    DEPTH_LIMIT_EXCEEDED = "DEPTH_LIMIT_EXCEEDED"


@dataclass
class ProofNode:
    """Hierarchical node in the backward chaining proof tree."""
    goal_fact: str
    target_value: TruthValue
    status: GoalStatus
    explanation: str
    depth: int
    rule_id: Optional[str] = None
    sub_nodes: List[ProofNode] = field(default_factory=list)
    missing_facts: Set[str] = field(default_factory=set)


@dataclass
class BackwardStepTrace:
    """Individual search step audit in backward chaining."""
    step_number: int
    depth: int
    goal_fact: str
    action: str
    rule_id: Optional[str]
    status: GoalStatus
    details: str


@dataclass
class BackwardChainingResult:
    """Comprehensive output of goal-directed backward chaining proof."""
    target_goal: str
    target_value: TruthValue
    status: GoalStatus
    proof_tree: ProofNode
    applied_rules: List[Rule]
    missing_prerequisites: List[str]
    contradicted_prerequisites: List[str]
    trace: List[BackwardStepTrace]
    depth_reached: int
    steps_count: int
    explanation_summary: str


class BackwardChainingEngine:
    """Executes goal-directed backward chaining with cycle detection and proof tracing."""

    def __init__(self, kb: KnowledgeBase, max_depth: int = 15) -> None:
        self.kb = kb
        self.max_depth = max_depth

    def run(
        self,
        target_goal: str,
        initial_facts: Dict[str, Fact],
        target_value: TruthValue = TruthValue.TRUE,
    ) -> BackwardChainingResult:
        """Attempts to prove target_goal == target_value starting from working facts."""
        working_memory: Dict[str, Fact] = dict(initial_facts)
        active_goal_stack: Set[str] = set()
        trace: List[BackwardStepTrace] = []
        applied_rules_dict: Dict[str, Rule] = {}
        missing_facts: Set[str] = set()
        contradicted_facts: Set[str] = set()
        step_counter = [0]
        max_depth_reached = [0]

        root_proof_node = self._prove_fact_goal(
            goal_fact=target_goal,
            target_value=target_value,
            working_memory=working_memory,
            active_goal_stack=active_goal_stack,
            trace=trace,
            applied_rules=applied_rules_dict,
            missing_facts=missing_facts,
            contradicted_facts=contradicted_facts,
            step_counter=step_counter,
            max_depth_reached=max_depth_reached,
            current_depth=0,
        )

        # Generate human-readable summary
        if root_proof_node.status == GoalStatus.SUPPORTED:
            summary = (
                f"Goal '{target_goal}' is conclusively SUPPORTED (established as {target_value.value}) "
                f"using {len(applied_rules_dict)} supporting production rule(s)."
            )
        elif root_proof_node.status == GoalStatus.UNRESOLVED_UNKNOWN:
            missing_list_str = ", ".join(sorted(missing_facts)) if missing_facts else "unspecified prerequisites"
            summary = (
                f"Goal '{target_goal}' remains UNRESOLVED due to insufficient evidence. "
                f"Missing prerequisite fact(s): {missing_list_str}."
            )
        elif root_proof_node.status == GoalStatus.CONTRADICTED_OR_FAILED:
            contra_str = ", ".join(sorted(contradicted_facts)) if contradicted_facts else "no satisfying rule found"
            summary = (
                f"Goal '{target_goal}' FAILED / CONTRADICTED: Unable to establish {target_value.value}. "
                f"Contradicting elements: {contra_str}."
            )
        elif root_proof_node.status == GoalStatus.CYCLE_DETECTED:
            summary = f"Goal '{target_goal}' failed due to circular rule dependency detection."
        else:
            summary = f"Goal '{target_goal}' halted: Maximum search depth of {self.max_depth} reached."

        return BackwardChainingResult(
            target_goal=target_goal,
            target_value=target_value,
            status=root_proof_node.status,
            proof_tree=root_proof_node,
            applied_rules=list(applied_rules_dict.values()),
            missing_prerequisites=sorted(list(missing_facts)),
            contradicted_prerequisites=sorted(list(contradicted_facts)),
            trace=trace,
            depth_reached=max_depth_reached[0],
            steps_count=step_counter[0],
            explanation_summary=summary,
        )

    def _prove_fact_goal(
        self,
        goal_fact: str,
        target_value: TruthValue,
        working_memory: Dict[str, Fact],
        active_goal_stack: Set[str],
        trace: List[BackwardStepTrace],
        applied_rules: Dict[str, Rule],
        missing_facts: Set[str],
        contradicted_facts: Set[str],
        step_counter: List[int],
        max_depth_reached: List[int],
        current_depth: int,
    ) -> ProofNode:
        step_counter[0] += 1
        curr_step = step_counter[0]
        max_depth_reached[0] = max(max_depth_reached[0], current_depth)

        # 1. Depth limit guard
        if current_depth > self.max_depth:
            node = ProofNode(
                goal_fact=goal_fact,
                target_value=target_value,
                status=GoalStatus.DEPTH_LIMIT_EXCEEDED,
                explanation=f"Maximum proof depth ({self.max_depth}) exceeded while investigating '{goal_fact}'.",
                depth=current_depth,
            )
            trace.append(BackwardStepTrace(
                step_number=curr_step,
                depth=current_depth,
                goal_fact=goal_fact,
                action="DEPTH_LIMIT_EXCEEDED",
                rule_id=None,
                status=GoalStatus.DEPTH_LIMIT_EXCEEDED,
                details=node.explanation,
            ))
            return node

        # 2. Cycle detection guard
        if goal_fact in active_goal_stack:
            node = ProofNode(
                goal_fact=goal_fact,
                target_value=target_value,
                status=GoalStatus.CYCLE_DETECTED,
                explanation=f"Circular dependency detected: Subgoal '{goal_fact}' is already being explored on current proof path.",
                depth=current_depth,
            )
            trace.append(BackwardStepTrace(
                step_number=curr_step,
                depth=current_depth,
                goal_fact=goal_fact,
                action="CYCLE_DETECTED",
                rule_id=None,
                status=GoalStatus.CYCLE_DETECTED,
                details=node.explanation,
            ))
            return node

        # 3. Check if goal is already directly established in working memory
        if goal_fact in working_memory:
            known_fact = working_memory[goal_fact]
            if known_fact.value == target_value:
                node = ProofNode(
                    goal_fact=goal_fact,
                    target_value=target_value,
                    status=GoalStatus.SUPPORTED,
                    explanation=f"Goal '{goal_fact}' is directly known as {target_value.value} from working memory ({known_fact.source.value}).",
                    depth=current_depth,
                )
                trace.append(BackwardStepTrace(
                    step_number=curr_step,
                    depth=current_depth,
                    goal_fact=goal_fact,
                    action="DIRECT_FACT_MATCH",
                    rule_id=known_fact.derivation_rule,
                    status=GoalStatus.SUPPORTED,
                    details=node.explanation,
                ))
                return node
            elif known_fact.value != TruthValue.UNKNOWN:
                contradicted_facts.add(goal_fact)
                node = ProofNode(
                    goal_fact=goal_fact,
                    target_value=target_value,
                    status=GoalStatus.CONTRADICTED_OR_FAILED,
                    explanation=f"Goal '{goal_fact}' is established as {known_fact.value.value}, contradicting requested {target_value.value}.",
                    depth=current_depth,
                )
                trace.append(BackwardStepTrace(
                    step_number=curr_step,
                    depth=current_depth,
                    goal_fact=goal_fact,
                    action="DIRECT_FACT_CONTRADICTED",
                    rule_id=None,
                    status=GoalStatus.CONTRADICTED_OR_FAILED,
                    details=node.explanation,
                ))
                return node

        # 4. Search for candidate production rules concluding this goal
        candidate_rules = self.kb.get_candidate_rules_for_goal(goal_fact)

        if not candidate_rules:
            # Fact is not derived by any rule and is not in working memory -> UNKNOWN leaf fact
            missing_facts.add(goal_fact)
            node = ProofNode(
                goal_fact=goal_fact,
                target_value=target_value,
                status=GoalStatus.UNRESOLVED_UNKNOWN,
                explanation=f"Prerequisite '{goal_fact}' is not present in working memory and no rule derives it (UNKNOWN).",
                depth=current_depth,
                missing_facts={goal_fact},
            )
            trace.append(BackwardStepTrace(
                step_number=curr_step,
                depth=current_depth,
                goal_fact=goal_fact,
                action="UNKNOWN_BASE_FACT",
                rule_id=None,
                status=GoalStatus.UNRESOLVED_UNKNOWN,
                details=node.explanation,
            ))
            return node

        # 5. Explore candidate rules with cycle tracking
        active_goal_stack.add(goal_fact)
        explored_subnodes: List[ProofNode] = []
        rule_missing_sets: List[Set[str]] = []
        all_rules_contradicted = True
        has_unknown_branch = False

        try:
            for rule in candidate_rules:
                if rule.consequent_value != target_value:
                    continue  # Rule concludes a different truth value

                step_counter[0] += 1
                trace.append(BackwardStepTrace(
                    step_number=step_counter[0],
                    depth=current_depth,
                    goal_fact=goal_fact,
                    action="EVALUATING_CANDIDATE_RULE",
                    rule_id=rule.id,
                    status=GoalStatus.UNRESOLVED_UNKNOWN,
                    details=f"Evaluating candidate rule {rule.id}: {rule.readable_text}",
                ))

                rule_missing: Set[str] = set()
                rule_contra: Set[str] = set()

                expr_node = self._prove_expression(
                    expression=rule.antecedent,
                    working_memory=working_memory,
                    active_goal_stack=active_goal_stack,
                    trace=trace,
                    applied_rules=applied_rules,
                    missing_facts=rule_missing,
                    contradicted_facts=rule_contra,
                    step_counter=step_counter,
                    max_depth_reached=max_depth_reached,
                    current_depth=current_depth + 1,
                    parent_rule_id=rule.id,
                )

                rule_missing_sets.append(rule_missing)

                if expr_node.status == GoalStatus.SUPPORTED:
                    # Successful proof branch found!
                    applied_rules[rule.id] = rule
                    # Add deduced fact into working memory for memoized reuse
                    working_memory[goal_fact] = Fact(
                        id=goal_fact,
                        value=target_value,
                        source=FactSource.INFERRED,
                        derivation_rule=rule.id,
                        step_number=step_counter[0],
                    )

                    succ_node = ProofNode(
                        goal_fact=goal_fact,
                        target_value=target_value,
                        status=GoalStatus.SUPPORTED,
                        explanation=f"Goal '{goal_fact}' was successfully proven via rule {rule.id} ({rule.name}).",
                        depth=current_depth,
                        rule_id=rule.id,
                        sub_nodes=[expr_node],
                    )
                    trace.append(BackwardStepTrace(
                        step_number=step_counter[0],
                        depth=current_depth,
                        goal_fact=goal_fact,
                        action="RULE_PROOF_SUCCESS",
                        rule_id=rule.id,
                        status=GoalStatus.SUPPORTED,
                        details=succ_node.explanation,
                    ))
                    return succ_node

                elif expr_node.status == GoalStatus.UNRESOLVED_UNKNOWN:
                    all_rules_contradicted = False
                    has_unknown_branch = True
                    explored_subnodes.append(expr_node)
                else:
                    # Contradicted or failed
                    explored_subnodes.append(expr_node)

            # If loop finishes without returning, no candidate rule succeeded
            if has_unknown_branch or not all_rules_contradicted:
                # Aggregate missing facts from all unknown branches
                for rms in rule_missing_sets:
                    missing_facts.update(rms)

                unres_node = ProofNode(
                    goal_fact=goal_fact,
                    target_value=target_value,
                    status=GoalStatus.UNRESOLVED_UNKNOWN,
                    explanation=f"Goal '{goal_fact}' cannot be confirmed because required prerequisites remain unknown across all candidate rules.",
                    depth=current_depth,
                    sub_nodes=explored_subnodes,
                    missing_facts=missing_facts,
                )
                trace.append(BackwardStepTrace(
                    step_number=step_counter[0],
                    depth=current_depth,
                    goal_fact=goal_fact,
                    action="GOAL_UNRESOLVED_UNKNOWN",
                    rule_id=None,
                    status=GoalStatus.UNRESOLVED_UNKNOWN,
                    details=unres_node.explanation,
                ))
                return unres_node
            else:
                fail_node = ProofNode(
                    goal_fact=goal_fact,
                    target_value=target_value,
                    status=GoalStatus.CONTRADICTED_OR_FAILED,
                    explanation=f"Goal '{goal_fact}' failed: All candidate rules were explicitly contradicted or failed.",
                    depth=current_depth,
                    sub_nodes=explored_subnodes,
                )
                trace.append(BackwardStepTrace(
                    step_number=step_counter[0],
                    depth=current_depth,
                    goal_fact=goal_fact,
                    action="GOAL_PROOF_FAILED",
                    rule_id=None,
                    status=GoalStatus.CONTRADICTED_OR_FAILED,
                    details=fail_node.explanation,
                ))
                return fail_node

        finally:
            active_goal_stack.remove(goal_fact)

    def _prove_expression(
        self,
        expression: Dict[str, Any],
        working_memory: Dict[str, Fact],
        active_goal_stack: Set[str],
        trace: List[BackwardStepTrace],
        applied_rules: Dict[str, Rule],
        missing_facts: Set[str],
        contradicted_facts: Set[str],
        step_counter: List[int],
        max_depth_reached: List[int],
        current_depth: int,
        parent_rule_id: Optional[str],
    ) -> ProofNode:
        """Evaluates an antecedent expression tree (ATOMIC, NOT, AND, OR) by backward deduction."""
        if "fact" in expression:
            f_id = expression["fact"]
            f_val = TruthValue.from_bool_or_str(expression.get("value", "TRUE"))
            return self._prove_fact_goal(
                goal_fact=f_id,
                target_value=f_val,
                working_memory=working_memory,
                active_goal_stack=active_goal_stack,
                trace=trace,
                applied_rules=applied_rules,
                missing_facts=missing_facts,
                contradicted_facts=contradicted_facts,
                step_counter=step_counter,
                max_depth_reached=max_depth_reached,
                current_depth=current_depth,
            )

        elif "and" in expression:
            children = expression["and"]
            child_nodes: List[ProofNode] = []
            has_failed = False
            has_unknown = False

            for ch in children:
                ch_node = self._prove_expression(
                    expression=ch,
                    working_memory=working_memory,
                    active_goal_stack=active_goal_stack,
                    trace=trace,
                    applied_rules=applied_rules,
                    missing_facts=missing_facts,
                    contradicted_facts=contradicted_facts,
                    step_counter=step_counter,
                    max_depth_reached=max_depth_reached,
                    current_depth=current_depth + 1,
                    parent_rule_id=parent_rule_id,
                )
                child_nodes.append(ch_node)
                if ch_node.status in (GoalStatus.CONTRADICTED_OR_FAILED, GoalStatus.CYCLE_DETECTED):
                    has_failed = True
                elif ch_node.status in (GoalStatus.UNRESOLVED_UNKNOWN, GoalStatus.DEPTH_LIMIT_EXCEEDED):
                    has_unknown = True

            if has_failed:
                overall_status = GoalStatus.CONTRADICTED_OR_FAILED
                expl = "AND conjunction failed: One or more conjuncts failed or were contradicted."
            elif has_unknown:
                overall_status = GoalStatus.UNRESOLVED_UNKNOWN
                expl = "AND conjunction unresolved: One or more conjuncts lack sufficient evidence."
            else:
                overall_status = GoalStatus.SUPPORTED
                expl = "AND conjunction succeeded: All conjuncts were conclusively established."

            return ProofNode(
                goal_fact="AND_EXPRESSION",
                target_value=TruthValue.TRUE,
                status=overall_status,
                explanation=expl,
                depth=current_depth,
                sub_nodes=child_nodes,
            )

        elif "or" in expression:
            children = expression["or"]
            child_nodes = []
            has_supported = False
            all_failed = True

            for ch in children:
                ch_node = self._prove_expression(
                    expression=ch,
                    working_memory=working_memory,
                    active_goal_stack=active_goal_stack,
                    trace=trace,
                    applied_rules=applied_rules,
                    missing_facts=missing_facts,
                    contradicted_facts=contradicted_facts,
                    step_counter=step_counter,
                    max_depth_reached=max_depth_reached,
                    current_depth=current_depth + 1,
                    parent_rule_id=parent_rule_id,
                )
                child_nodes.append(ch_node)
                if ch_node.status == GoalStatus.SUPPORTED:
                    has_supported = True
                    all_failed = False
                    break  # Early success on OR!
                elif ch_node.status in (GoalStatus.UNRESOLVED_UNKNOWN, GoalStatus.DEPTH_LIMIT_EXCEEDED):
                    all_failed = False

            if has_supported:
                overall_status = GoalStatus.SUPPORTED
                expl = "OR disjunction succeeded: At least one alternative branch was established."
            elif all_failed:
                overall_status = GoalStatus.CONTRADICTED_OR_FAILED
                expl = "OR disjunction failed: All alternative branches were contradicted or failed."
            else:
                overall_status = GoalStatus.UNRESOLVED_UNKNOWN
                expl = "OR disjunction unresolved: No branch succeeded and some branches remain unknown."

            return ProofNode(
                goal_fact="OR_EXPRESSION",
                target_value=TruthValue.TRUE,
                status=overall_status,
                explanation=expl,
                depth=current_depth,
                sub_nodes=child_nodes,
            )

        elif "not" in expression:
            ch_node = self._prove_expression(
                expression=expression["not"],
                working_memory=working_memory,
                active_goal_stack=active_goal_stack,
                trace=trace,
                applied_rules=applied_rules,
                missing_facts=missing_facts,
                contradicted_facts=contradicted_facts,
                step_counter=step_counter,
                max_depth_reached=max_depth_reached,
                current_depth=current_depth + 1,
                parent_rule_id=parent_rule_id,
            )
            if ch_node.status == GoalStatus.SUPPORTED:
                stat = GoalStatus.CONTRADICTED_OR_FAILED
                expl = "NOT negation inverted child SUPPORTED into FAILED."
            elif ch_node.status == GoalStatus.CONTRADICTED_OR_FAILED:
                stat = GoalStatus.SUPPORTED
                expl = "NOT negation inverted child FAILED into SUPPORTED."
            else:
                stat = ch_node.status
                expl = f"NOT negation preserves unresolved status: {ch_node.status.value}."

            return ProofNode(
                goal_fact="NOT_EXPRESSION",
                target_value=TruthValue.TRUE,
                status=stat,
                explanation=expl,
                depth=current_depth,
                sub_nodes=[ch_node],
            )

        else:
            raise ValueError(f"Unknown expression format: {expression}")
