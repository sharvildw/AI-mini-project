"""Three-Valued Logical Rule Evaluator Module.

Implements rigorous Kleene 3-Valued Logic (K3) evaluation over propositional
well-formed formulas: Atomic terms, NOT, AND, and OR connectives.
Preserves explicit UNKNOWN semantics and generates detailed step-by-step
audit breakdowns.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
from .knowledge_base import Fact, TruthValue


@dataclass
class EvaluationResult:
    """Detailed result of evaluating a logical expression tree."""
    value: TruthValue
    explanation: str
    expression_summary: str
    missing_facts: Set[str] = field(default_factory=set)
    contradicted_facts: Set[str] = field(default_factory=set)
    sub_evaluations: List[EvaluationResult] = field(default_factory=list)

    @property
    def is_true(self) -> bool:
        return self.value == TruthValue.TRUE

    @property
    def is_false(self) -> bool:
        return self.value == TruthValue.FALSE

    @property
    def is_unknown(self) -> bool:
        return self.value == TruthValue.UNKNOWN


class RuleEvaluator:
    """Evaluates rule antecedents against working memory using 3-valued logic."""

    @staticmethod
    def evaluate(expression: Dict[str, Any], fact_store: Dict[str, Fact]) -> EvaluationResult:
        """Recursively evaluates an expression dictionary against working memory."""
        if "fact" in expression:
            return RuleEvaluator._evaluate_atomic(expression, fact_store)
        elif "and" in expression:
            return RuleEvaluator._evaluate_and(expression["and"], fact_store)
        elif "or" in expression:
            return RuleEvaluator._evaluate_or(expression["or"], fact_store)
        elif "not" in expression:
            return RuleEvaluator._evaluate_not(expression["not"], fact_store)
        else:
            raise ValueError(f"Malformed expression node encountered: {expression}")

    @staticmethod
    def _evaluate_atomic(node: Dict[str, Any], fact_store: Dict[str, Fact]) -> EvaluationResult:
        fact_id = node["fact"]
        expected_val_str = node.get("value", "TRUE")
        expected_val = TruthValue.from_bool_or_str(expected_val_str)

        fact = fact_store.get(fact_id)
        expr_summary = f"{fact_id} == {expected_val.value}"

        if fact is None or fact.value == TruthValue.UNKNOWN:
            return EvaluationResult(
                value=TruthValue.UNKNOWN,
                explanation=f"Prerequisite '{fact_id}' has not been established (UNKNOWN).",
                expression_summary=expr_summary,
                missing_facts={fact_id},
            )

        if fact.value == expected_val:
            return EvaluationResult(
                value=TruthValue.TRUE,
                explanation=f"Prerequisite '{fact_id}' is verified as {fact.value.value} (matches expected).",
                expression_summary=expr_summary,
            )
        else:
            return EvaluationResult(
                value=TruthValue.FALSE,
                explanation=f"Prerequisite '{fact_id}' is established as {fact.value.value}, which contradicts expected {expected_val.value}.",
                expression_summary=expr_summary,
                contradicted_facts={fact_id},
            )

    @staticmethod
    def _evaluate_not(child_node: Dict[str, Any], fact_store: Dict[str, Fact]) -> EvaluationResult:
        child_res = RuleEvaluator.evaluate(child_node, fact_store)
        expr_summary = f"NOT ({child_res.expression_summary})"

        if child_res.value == TruthValue.TRUE:
            val = TruthValue.FALSE
            expl = f"NOT operator evaluated child TRUE into FALSE."
        elif child_res.value == TruthValue.FALSE:
            val = TruthValue.TRUE
            expl = f"NOT operator evaluated child FALSE into TRUE."
        else:
            val = TruthValue.UNKNOWN
            expl = f"NOT operator with child UNKNOWN remains UNKNOWN."

        return EvaluationResult(
            value=val,
            explanation=expl,
            expression_summary=expr_summary,
            missing_facts=set(child_res.missing_facts),
            contradicted_facts=set(child_res.contradicted_facts),
            sub_evaluations=[child_res],
        )

    @staticmethod
    def _evaluate_and(children: List[Dict[str, Any]], fact_store: Dict[str, Fact]) -> EvaluationResult:
        sub_results: List[EvaluationResult] = [
            RuleEvaluator.evaluate(child, fact_store) for child in children
        ]

        missing: Set[str] = set()
        contradicted: Set[str] = set()
        for sr in sub_results:
            missing.update(sr.missing_facts)
            contradicted.update(sr.contradicted_facts)

        summaries = [f"({sr.expression_summary})" for sr in sub_results]
        expr_summary = " AND ".join(summaries)

        # 3-valued Kleene AND semantics:
        # If ANY child is FALSE, overall AND is FALSE immediately.
        # If ALL children are TRUE, overall AND is TRUE.
        # Otherwise (some TRUE/UNKNOWN and none FALSE), overall AND is UNKNOWN.
        has_false = any(sr.value == TruthValue.FALSE for sr in sub_results)
        all_true = all(sr.value == TruthValue.TRUE for sr in sub_results)

        if has_false:
            failed_items = [sr.expression_summary for sr in sub_results if sr.value == TruthValue.FALSE]
            return EvaluationResult(
                value=TruthValue.FALSE,
                explanation=f"AND conjunction failed because one or more terms evaluated to FALSE: {', '.join(failed_items)}.",
                expression_summary=expr_summary,
                missing_facts=missing,
                contradicted_facts=contradicted,
                sub_evaluations=sub_results,
            )

        if all_true:
            return EvaluationResult(
                value=TruthValue.TRUE,
                explanation=f"AND conjunction satisfied because all {len(sub_results)} terms evaluated to TRUE.",
                expression_summary=expr_summary,
                missing_facts=missing,
                contradicted_facts=contradicted,
                sub_evaluations=sub_results,
            )

        # Remaining case: some UNKNOWN, no FALSE
        unknown_items = [sr.expression_summary for sr in sub_results if sr.value == TruthValue.UNKNOWN]
        return EvaluationResult(
            value=TruthValue.UNKNOWN,
            explanation=f"AND conjunction cannot be resolved because terms remain UNKNOWN: {', '.join(unknown_items)}.",
            expression_summary=expr_summary,
            missing_facts=missing,
            contradicted_facts=contradicted,
            sub_evaluations=sub_results,
        )

    @staticmethod
    def _evaluate_or(children: List[Dict[str, Any]], fact_store: Dict[str, Fact]) -> EvaluationResult:
        sub_results: List[EvaluationResult] = [
            RuleEvaluator.evaluate(child, fact_store) for child in children
        ]

        missing: Set[str] = set()
        contradicted: Set[str] = set()
        for sr in sub_results:
            missing.update(sr.missing_facts)
            contradicted.update(sr.contradicted_facts)

        summaries = [f"({sr.expression_summary})" for sr in sub_results]
        expr_summary = " OR ".join(summaries)

        # 3-valued Kleene OR semantics:
        # If ANY child is TRUE, overall OR is TRUE immediately.
        # If ALL children are FALSE, overall OR is FALSE.
        # Otherwise (mix of FALSE and UNKNOWN, no TRUE), overall OR is UNKNOWN.
        has_true = any(sr.value == TruthValue.TRUE for sr in sub_results)
        all_false = all(sr.value == TruthValue.FALSE for sr in sub_results)

        if has_true:
            satisfied_items = [sr.expression_summary for sr in sub_results if sr.value == TruthValue.TRUE]
            return EvaluationResult(
                value=TruthValue.TRUE,
                explanation=f"OR disjunction satisfied because term(s) evaluated to TRUE: {', '.join(satisfied_items)}.",
                expression_summary=expr_summary,
                missing_facts=missing,
                contradicted_facts=contradicted,
                sub_evaluations=sub_results,
            )

        if all_false:
            return EvaluationResult(
                value=TruthValue.FALSE,
                explanation=f"OR disjunction failed because all {len(sub_results)} terms evaluated to FALSE.",
                expression_summary=expr_summary,
                missing_facts=missing,
                contradicted_facts=contradicted,
                sub_evaluations=sub_results,
            )

        # Remaining case: mix of FALSE and UNKNOWN
        return EvaluationResult(
            value=TruthValue.UNKNOWN,
            explanation=f"OR disjunction unresolved because no term evaluated to TRUE and some terms remain UNKNOWN.",
            expression_summary=expr_summary,
            missing_facts=missing,
            contradicted_facts=contradicted,
            sub_evaluations=sub_results,
        )
