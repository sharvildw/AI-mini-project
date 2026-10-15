"""MediLogic Expert System Engine Package.

Provides rule-based inference mechanisms (Forward Chaining & Backward Chaining),
three-valued logical evaluation, knowledge base management, safety monitoring,
and audit explanation facilities.
"""

from .knowledge_base import KnowledgeBase, Fact, TruthValue, FactSource, Rule
from .rule_evaluator import RuleEvaluator, EvaluationResult
from .forward_chaining import ForwardChainingEngine, ForwardChainingResult
from .backward_chaining import BackwardChainingEngine, BackwardChainingResult, GoalStatus
from .explanation import ExplanationEngine
from .safety import SafetyEngine, EmergencyAlert

__all__ = [
    "KnowledgeBase",
    "Fact",
    "TruthValue",
    "FactSource",
    "Rule",
    "RuleEvaluator",
    "EvaluationResult",
    "ForwardChainingEngine",
    "ForwardChainingResult",
    "BackwardChainingEngine",
    "BackwardChainingResult",
    "GoalStatus",
    "ExplanationEngine",
    "SafetyEngine",
    "EmergencyAlert",
]
