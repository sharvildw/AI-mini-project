"""Audit and Transparent Explanation Generation Module.

Translates internal execution traces from both Forward Chaining and Backward Chaining
into clear, educational, step-by-step diagnostic narratives and prerequisite breakdowns.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from .backward_chaining import BackwardChainingResult, GoalStatus, ProofNode
from .forward_chaining import ForwardChainingResult, ForwardStepTrace
from .knowledge_base import Fact, KnowledgeBase, Rule, TruthValue


@dataclass
class RuleExplanationCard:
    """Structured inspection card for a single production rule."""
    rule_id: str
    name: str
    category: str
    readable_text: str
    consequent: str
    status: str
    step_number: Optional[int]
    narrative: str
    prerequisites_breakdown: List[Dict[str, str]]
    source_reference: str


class ExplanationEngine:
    """Produces explainable audit narratives from real engine execution traces."""

    def __init__(self, kb: KnowledgeBase) -> None:
        self.kb = kb

    def explain_forward_step(self, step: ForwardStepTrace) -> str:
        """Generates detailed explanation for a forward chaining execution step."""
        if step.fired:
            return (
                f"Step {step.step_number} [Iteration {step.iteration}]: Rule {step.rule_id} ('{step.rule_name}') "
                f"successfully fired via Modus Ponens. All antecedent conditions were verified as TRUE. "
                f"Consequent fact '{step.consequent_fact}' was confirmed as {step.consequent_value.value} "
                f"{'(New fact added to working memory)' if step.is_new_fact else '(Already in working memory)'}."
            )
        else:
            if step.evaluation_value == TruthValue.FALSE:
                return (
                    f"Step {step.step_number} [Iteration {step.iteration}]: Rule {step.rule_id} did NOT fire. "
                    f"One or more antecedent conditions were explicitly contradicted (FALSE). "
                    f"Details: {step.evaluation_result.explanation}"
                )
            else:
                missing_str = ", ".join(sorted(step.evaluation_result.missing_facts)) if step.evaluation_result.missing_facts else "unspecified"
                return (
                    f"Step {step.step_number} [Iteration {step.iteration}]: Rule {step.rule_id} did NOT fire. "
                    f"Antecedent conditions remain UNKNOWN because prerequisite(s) [{missing_str}] "
                    f"have not been established by the user or derived by previous rules."
                )

    def generate_forward_summary(self, result: ForwardChainingResult) -> Dict[str, Any]:
        """Summarizes forward chaining run for the user interface."""
        cards: List[RuleExplanationCard] = []

        # Find the latest evaluation step for each rule
        latest_steps_by_rule: Dict[str, ForwardStepTrace] = {}
        for step in result.trace:
            latest_steps_by_rule[step.rule_id] = step

        for rule in self.kb.rules:
            step = latest_steps_by_rule.get(rule.id)
            if step is None:
                continue

            prereqs: List[Dict[str, str]] = []
            leaf_facts = self.kb.extract_leaf_facts_from_expression(rule.antecedent)
            for f in sorted(leaf_facts):
                fact_obj = result.working_memory.get(f)
                val_str = fact_obj.value.value if fact_obj else "UNKNOWN"
                src_str = fact_obj.source.value if fact_obj else "NOT_SUPPLIED"
                prereqs.append({
                    "fact": f,
                    "state": val_str,
                    "source": src_str,
                })

            status_str = "FIRED" if step.fired else ("CONTRADICTED (FALSE)" if step.evaluation_value == TruthValue.FALSE else "UNRESOLVED (UNKNOWN)")
            narrative = self.explain_forward_step(step)

            cards.append(RuleExplanationCard(
                rule_id=rule.id,
                name=rule.name,
                category=rule.category,
                readable_text=rule.readable_text,
                consequent=rule.consequent_fact_id,
                status=status_str,
                step_number=step.step_number,
                narrative=narrative,
                prerequisites_breakdown=prereqs,
                source_reference=rule.source,
            ))

        return {
            "initial_facts_count": len(result.initial_facts),
            "derived_facts_count": len(result.derived_facts),
            "total_working_memory": len(result.working_memory),
            "fired_rules_count": len(result.fired_rules),
            "iterations_run": result.iterations_run,
            "termination_reason": result.termination_reason,
            "rule_cards": cards,
        }

    def format_backward_proof_tree(self, node: ProofNode, indent_level: int = 0) -> List[Dict[str, Any]]:
        """Flattens recursive proof tree into an ordered, indented visualization structure."""
        items: List[Dict[str, Any]] = []
        indent = "    " * indent_level

        icon_map = {
            GoalStatus.SUPPORTED: "[PROVEN]",
            GoalStatus.CONTRADICTED_OR_FAILED: "[FAILED]",
            GoalStatus.UNRESOLVED_UNKNOWN: "[UNKNOWN]",
            GoalStatus.CYCLE_DETECTED: "[CYCLE]",
            GoalStatus.DEPTH_LIMIT_EXCEEDED: "[LIMIT]",
        }

        tag = icon_map.get(node.status, "[?]")
        items.append({
            "indent": indent_level,
            "goal": node.goal_fact,
            "target_value": node.target_value.value,
            "status": node.status.value,
            "rule_id": node.rule_id,
            "tag": tag,
            "text": f"{indent}{tag} Subgoal: '{node.goal_fact}' -> {node.status.value}. {node.explanation}",
        })

        for child in node.sub_nodes:
            items.extend(self.format_backward_proof_tree(child, indent_level + 1))

        return items

    def find_candidate_and_differential_hypotheses(
        self,
        working_memory: Dict[str, Fact],
        supported_condition_ids: Set[str],
    ) -> List[Dict[str, Any]]:
        """Identifies differential candidate conditions that partially match the patient's facts.

        Calculates diagnostic alignment and pinpoints missing vs present symptoms to produce
        reliable, clinically actionable guidance even when rules have not 100% saturated.
        """
        candidates: List[Dict[str, Any]] = []

        for cond_id, cond_data in self.kb.conditions.items():
            if cond_id in supported_condition_ids:
                continue

            candidate_rules = self.kb.get_candidate_rules_for_goal(cond_id)
            if not candidate_rules:
                continue

            best_match_for_condition: Optional[Dict[str, Any]] = None
            highest_score = 0.0

            for rule in candidate_rules:
                leaf_facts = self.kb.extract_leaf_facts_from_expression(rule.antecedent)
                true_facts = []
                false_facts = []
                unknown_facts = []

                for fid in leaf_facts:
                    f_obj = working_memory.get(fid)
                    sym_info = self.kb.symptoms.get(fid, {})
                    sym_name = sym_info.get("name", fid)
                    if f_obj and f_obj.is_true():
                        true_facts.append(sym_name)
                    elif f_obj and f_obj.is_false():
                        false_facts.append(sym_name)
                    else:
                        unknown_facts.append(sym_name)

                total_facts = len(leaf_facts)
                if total_facts == 0:
                    continue

                score = len(true_facts) / total_facts

                # To be considered a plausible candidate:
                # At least 1 matching symptom, no explicit contradictions, and highest score
                if len(true_facts) >= 1 and score > highest_score and len(false_facts) == 0:
                    highest_score = score
                    best_match_for_condition = {
                        "condition_id": cond_id,
                        "condition_name": cond_data.get("name", cond_id),
                        "category": cond_data.get("category", "General"),
                        "description": cond_data.get("description", ""),
                        "match_score": round(score * 100),
                        "matching_symptoms": true_facts,
                        "missing_symptoms": unknown_facts,
                        "contradicted_symptoms": false_facts,
                        "clinical_features": cond_data.get("clinical_features", []),
                        "differential_considerations": cond_data.get("differential_considerations", []),
                        "primary_reference": cond_data.get("primary_reference", ""),
                        "rule_id": rule.id,
                        "rule_name": rule.name,
                    }

            if best_match_for_condition and best_match_for_condition["match_score"] >= 33:
                candidates.append(best_match_for_condition)

        # Sort by match score descending
        candidates.sort(key=lambda c: c["match_score"], reverse=True)
        return candidates

    def compare_engines(
        self,
        forward_res: ForwardChainingResult,
        backward_res: BackwardChainingResult,
    ) -> Dict[str, Any]:
        """Provides analytical side-by-side comparison between both algorithms."""
        fw_hypotheses = {h["condition_id"] for h in forward_res.supported_hypotheses}
        bw_supported = backward_res.status == GoalStatus.SUPPORTED
        target = backward_res.target_goal

        both_agree = (target in fw_hypotheses) == bw_supported

        return {
            "target_goal": target,
            "forward_supported_all": sorted(list(fw_hypotheses)),
            "forward_target_supported": target in fw_hypotheses,
            "backward_target_status": backward_res.status.value,
            "backward_target_supported": bw_supported,
            "agreement": both_agree,
            "forward_steps_count": len(forward_res.trace),
            "forward_rules_fired": [r.id for r in forward_res.fired_rules],
            "backward_steps_count": backward_res.steps_count,
            "backward_rules_applied": [r.id for r in backward_res.applied_rules],
            "backward_depth_reached": backward_res.depth_reached,
            "missing_prerequisites": backward_res.missing_prerequisites,
            "comparison_notes": (
                "Forward Chaining operates bottom-up (data-driven), iteratively deriving ALL reachable conclusions "
                "from the initially known facts. Backward Chaining operates top-down (goal-driven), focusing solely "
                f"on establishing the targeted hypothesis '{target}' and investigating only necessary prerequisites."
            ),
        }


