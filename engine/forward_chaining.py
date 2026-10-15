"""Data-Driven Forward Chaining Inference Engine.

Iteratively applies Modus Ponens over production rules against working memory,
deriving intermediate syndromic representations and educational condition hypotheses
until reaching a fixed point or safety execution limit.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
from .knowledge_base import Fact, FactSource, KnowledgeBase, Rule, TruthValue
from .rule_evaluator import EvaluationResult, RuleEvaluator


@dataclass
class ForwardStepTrace:
    """Detailed audit record for a single rule evaluation step in forward chaining."""
    step_number: int
    iteration: int
    rule_id: str
    rule_name: str
    rule_text: str
    evaluation_value: TruthValue
    fired: bool
    consequent_fact: str
    consequent_value: TruthValue
    is_new_fact: bool
    explanation: str
    evaluation_result: EvaluationResult


@dataclass
class ForwardChainingResult:
    """Comprehensive output of forward chaining inference."""
    initial_facts: Dict[str, Fact]
    working_memory: Dict[str, Fact]
    derived_facts: Dict[str, Fact]
    fired_rules: List[Rule]
    trace: List[ForwardStepTrace]
    supported_hypotheses: List[Dict[str, Any]]
    iterations_run: int
    termination_reason: str
    execution_limit_reached: bool


class ForwardChainingEngine:
    """Executes data-driven forward chaining inference with cycle and duplicate safeguards."""

    def __init__(self, kb: KnowledgeBase, max_iterations: int = 50) -> None:
        self.kb = kb
        self.max_iterations = max_iterations

    def run(self, initial_facts: Dict[str, Fact]) -> ForwardChainingResult:
        """Executes the forward chaining cycle until fixed-point or max iterations."""
        working_memory: Dict[str, Fact] = {}
        # Clone initial facts into working memory
        for fid, fact in initial_facts.items():
            working_memory[fid] = Fact(
                id=fact.id,
                value=fact.value,
                source=fact.source,
                step_number=0,
                derivation_rule=fact.derivation_rule,
            )

        derived_facts: Dict[str, Fact] = {}
        fired_rules: List[Rule] = []
        already_fired_rule_ids: Set[str] = set()
        trace: List[ForwardStepTrace] = []

        step_counter = 0
        iteration = 0
        execution_limit_reached = False
        termination_reason = "Fixed-point reached: No additional rules satisfied."

        while iteration < self.max_iterations:
            iteration += 1
            new_facts_in_iteration = 0

            # Deterministic evaluation order: sorted by rule ID
            for rule in sorted(self.kb.rules, key=lambda r: r.id):
                step_counter += 1

                # If rule already fired and produced its consequent, avoid redundant refiring
                if rule.id in already_fired_rule_ids:
                    continue

                eval_res = RuleEvaluator.evaluate(rule.antecedent, working_memory)

                if eval_res.is_true:
                    c_fact_id = rule.consequent_fact_id
                    c_val = rule.consequent_value

                    # Check if working memory already has this exact fact
                    existing = working_memory.get(c_fact_id)
                    is_new = existing is None or existing.value != c_val

                    # Modus Ponens fires rule
                    already_fired_rule_ids.add(rule.id)
                    fired_rules.append(rule)

                    if is_new:
                        new_fact = Fact(
                            id=c_fact_id,
                            value=c_val,
                            source=FactSource.INFERRED,
                            derivation_rule=rule.id,
                            step_number=step_counter,
                        )
                        working_memory[c_fact_id] = new_fact
                        derived_facts[c_fact_id] = new_fact
                        new_facts_in_iteration += 1

                    trace_step = ForwardStepTrace(
                        step_number=step_counter,
                        iteration=iteration,
                        rule_id=rule.id,
                        rule_name=rule.name,
                        rule_text=rule.readable_text,
                        evaluation_value=TruthValue.TRUE,
                        fired=True,
                        consequent_fact=c_fact_id,
                        consequent_value=c_val,
                        is_new_fact=is_new,
                        explanation=f"Rule {rule.id} fired via Modus Ponens: Antecedent satisfied. Added/confirmed '{c_fact_id}' as {c_val.value}.",
                        evaluation_result=eval_res,
                    )
                    trace.append(trace_step)

                else:
                    # Record non-firing step for complete auditability
                    reason_msg = (
                        f"Rule {rule.id} did not fire: Antecedent evaluated to {eval_res.value.value}. "
                        f"{eval_res.explanation}"
                    )
                    trace_step = ForwardStepTrace(
                        step_number=step_counter,
                        iteration=iteration,
                        rule_id=rule.id,
                        rule_name=rule.name,
                        rule_text=rule.readable_text,
                        evaluation_value=eval_res.value,
                        fired=False,
                        consequent_fact=rule.consequent_fact_id,
                        consequent_value=rule.consequent_value,
                        is_new_fact=False,
                        explanation=reason_msg,
                        evaluation_result=eval_res,
                    )
                    trace.append(trace_step)

            # If no new facts derived in this complete pass, fixed-point reached
            if new_facts_in_iteration == 0:
                termination_reason = f"Fixed-point reached at iteration {iteration}: Working memory saturated."
                break
        else:
            execution_limit_reached = True
            termination_reason = f"Execution safety limit reached: {self.max_iterations} iterations exceeded."

        # Compile supported educational condition hypotheses
        supported_hypotheses: List[Dict[str, Any]] = []
        for cond_id, cond_data in self.kb.conditions.items():
            fact = working_memory.get(cond_id)
            if fact and fact.is_true():
                supported_hypotheses.append({
                    "condition_id": cond_id,
                    "condition_name": cond_data.get("name", cond_id),
                    "category": cond_data.get("category", "General"),
                    "description": cond_data.get("description", ""),
                    "clinical_features": cond_data.get("clinical_features", []),
                    "differential_considerations": cond_data.get("differential_considerations", []),
                    "primary_reference": cond_data.get("primary_reference", ""),
                    "derivation_rule": fact.derivation_rule,
                })

        return ForwardChainingResult(
            initial_facts=initial_facts,
            working_memory=working_memory,
            derived_facts=derived_facts,
            fired_rules=fired_rules,
            trace=trace,
            supported_hypotheses=supported_hypotheses,
            iterations_run=iteration,
            termination_reason=termination_reason,
            execution_limit_reached=execution_limit_reached,
        )
