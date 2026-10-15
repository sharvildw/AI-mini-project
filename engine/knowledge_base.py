"""Knowledge Base Management and Validation Module.

Defines schemas for Facts, Rules, Truth Values, Fact Sources, and the
KnowledgeBase loader which rigorously validates rule syntax, references,
and expression tree structures.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class TruthValue(str, Enum):
    """Explicit tri-state truth values for educational logical calculus."""
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def from_bool_or_str(cls, val: Any) -> TruthValue:
        if isinstance(val, TruthValue):
            return val
        if isinstance(val, bool):
            return cls.TRUE if val else cls.FALSE
        if isinstance(val, str):
            val_upper = val.strip().upper()
            if val_upper in ("TRUE", "T", "PRESENT", "YES", "1"):
                return cls.TRUE
            if val_upper in ("FALSE", "F", "ABSENT", "NO", "0"):
                return cls.FALSE
            if val_upper in ("UNKNOWN", "U", "UNSET", "NONE", "NULL"):
                return cls.UNKNOWN
        return cls.UNKNOWN


class FactSource(str, Enum):
    """Distinguishes human-supplied facts from derived facts."""
    USER = "USER"
    INFERRED = "INFERRED"
    SYSTEM_DEFAULT = "SYSTEM_DEFAULT"


@dataclass
class Fact:
    """Represents a propositional fact held in working memory."""
    id: str
    value: TruthValue
    source: FactSource = FactSource.USER
    derivation_rule: Optional[str] = None
    step_number: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_true(self) -> bool:
        return self.value == TruthValue.TRUE

    def is_false(self) -> bool:
        return self.value == TruthValue.FALSE

    def is_unknown(self) -> bool:
        return self.value == TruthValue.UNKNOWN


@dataclass
class Rule:
    """Represents an IF-THEN production rule."""
    id: str
    name: str
    category: str
    readable_text: str
    antecedent: Dict[str, Any]
    consequent: Dict[str, Any]
    explanation: str
    source: str

    @property
    def consequent_fact_id(self) -> str:
        return self.consequent.get("fact", "")

    @property
    def consequent_value(self) -> TruthValue:
        return TruthValue.from_bool_or_str(self.consequent.get("value", "TRUE"))


class KnowledgeBaseValidationError(Exception):
    """Raised when knowledge base definitions violate validation constraints."""
    pass


class KnowledgeBase:
    """Loads, validates, and provides access to production rules and symptoms."""

    def __init__(self, data_dir: Optional[Path | str] = None) -> None:
        if data_dir is None:
            self.data_dir = Path(__file__).resolve().parent.parent / "data"
        else:
            self.data_dir = Path(data_dir)

        self.symptoms: Dict[str, Dict[str, Any]] = {}
        self.rules: List[Rule] = []
        self.rules_by_id: Dict[str, Rule] = {}
        self.rules_by_consequent: Dict[str, List[Rule]] = {}
        self.conditions: Dict[str, Dict[str, Any]] = {}
        self.references: Dict[str, Dict[str, Any]] = {}
        self._all_fact_symbols: Set[str] = set()

        self.reload()

    def reload(self) -> None:
        """Loads and strictly validates all knowledge base components."""
        self._load_references()
        self._load_symptoms()
        self._load_conditions()
        self._load_rules()
        self._validate_integrity()

    def _load_references(self) -> None:
        ref_file = self.data_dir / "references.json"
        if not ref_file.exists():
            raise FileNotFoundError(f"References file not found: {ref_file}")
        with open(ref_file, "r", encoding="utf-8") as f:
            self.references = json.load(f)

    def _load_symptoms(self) -> None:
        sym_file = self.data_dir / "symptoms.json"
        if not sym_file.exists():
            raise FileNotFoundError(f"Symptoms file not found: {sym_file}")
        with open(sym_file, "r", encoding="utf-8") as f:
            sym_list = json.load(f)

        self.symptoms = {}
        for s in sym_list:
            sid = s.get("id")
            if not sid:
                raise KnowledgeBaseValidationError("Symptom missing required 'id' attribute.")
            if sid in self.symptoms:
                raise KnowledgeBaseValidationError(f"Duplicate symptom ID detected: {sid}")
            self.symptoms[sid] = s
            self._all_fact_symbols.add(sid)

    def _load_conditions(self) -> None:
        cond_file = self.data_dir / "conditions.json"
        if not cond_file.exists():
            raise FileNotFoundError(f"Conditions file not found: {cond_file}")
        with open(cond_file, "r", encoding="utf-8") as f:
            cond_list = json.load(f)

        self.conditions = {}
        for c in cond_list:
            cid = c.get("id")
            if not cid:
                raise KnowledgeBaseValidationError("Condition missing required 'id' attribute.")
            if cid in self.conditions:
                raise KnowledgeBaseValidationError(f"Duplicate condition ID detected: {cid}")
            self.conditions[cid] = c
            self._all_fact_symbols.add(cid)

    def _load_rules(self) -> None:
        rules_file = self.data_dir / "rules.json"
        if not rules_file.exists():
            raise FileNotFoundError(f"Rules file not found: {rules_file}")
        with open(rules_file, "r", encoding="utf-8") as f:
            rules_data = json.load(f)

        self.rules = []
        self.rules_by_id = {}
        self.rules_by_consequent = {}

        seen_rule_ids: Set[str] = set()

        for r_dict in rules_data:
            rid = r_dict.get("id")
            if not rid:
                raise KnowledgeBaseValidationError("Rule missing required 'id' field.")
            if rid in seen_rule_ids:
                raise KnowledgeBaseValidationError(f"Duplicate rule ID found: {rid}")
            seen_rule_ids.add(rid)

            # Validate basic fields
            name = r_dict.get("name", rid)
            cat = r_dict.get("category", "General")
            readable = r_dict.get("readable_text", "")
            antecedent = r_dict.get("antecedent")
            consequent = r_dict.get("consequent")
            explanation = r_dict.get("explanation", "")
            source = r_dict.get("source", "")

            if not antecedent or not isinstance(antecedent, dict):
                raise KnowledgeBaseValidationError(f"Rule {rid} has invalid antecedent expression.")
            if not consequent or not isinstance(consequent, dict) or "fact" not in consequent:
                raise KnowledgeBaseValidationError(f"Rule {rid} has invalid consequent expression.")

            rule_obj = Rule(
                id=rid,
                name=name,
                category=cat,
                readable_text=readable,
                antecedent=antecedent,
                consequent=consequent,
                explanation=explanation,
                source=source,
            )

            self.rules.append(rule_obj)
            self.rules_by_id[rid] = rule_obj

            c_fact = rule_obj.consequent_fact_id
            self._all_fact_symbols.add(c_fact)
            if c_fact not in self.rules_by_consequent:
                self.rules_by_consequent[c_fact] = []
            self.rules_by_consequent[c_fact].append(rule_obj)

    def _validate_integrity(self) -> None:
        """Deep checks for expression syntax and symbol dependencies."""
        for rule in self.rules:
            # Validate source reference
            if rule.source and rule.source not in self.references:
                raise KnowledgeBaseValidationError(
                    f"Rule {rule.id} references undefined bibliographic source '{rule.source}'"
                )

            # Recursively validate expression tree
            self._validate_expression(rule.id, rule.antecedent)

    def _validate_expression(self, rule_id: str, expr: Any) -> None:
        if not isinstance(expr, dict):
            raise KnowledgeBaseValidationError(
                f"Rule {rule_id}: Expression node must be a dictionary, got {type(expr).__name__}"
            )

        keys = set(expr.keys())
        if "fact" in keys:
            fact_id = expr["fact"]
            if not isinstance(fact_id, str) or not fact_id:
                raise KnowledgeBaseValidationError(
                    f"Rule {rule_id}: 'fact' identifier must be a non-empty string"
                )
            self._all_fact_symbols.add(fact_id)
        elif "and" in keys:
            children = expr["and"]
            if not isinstance(children, list) or len(children) == 0:
                raise KnowledgeBaseValidationError(
                    f"Rule {rule_id}: 'and' operator requires a non-empty list of expressions"
                )
            for child in children:
                self._validate_expression(rule_id, child)
        elif "or" in keys:
            children = expr["or"]
            if not isinstance(children, list) or len(children) == 0:
                raise KnowledgeBaseValidationError(
                    f"Rule {rule_id}: 'or' operator requires a non-empty list of expressions"
                )
            for child in children:
                self._validate_expression(rule_id, child)
        elif "not" in keys:
            child = expr["not"]
            self._validate_expression(rule_id, child)
        else:
            raise KnowledgeBaseValidationError(
                f"Rule {rule_id}: Unrecognized logical expression structure: {keys}"
            )

    def get_candidate_rules_for_goal(self, goal_fact_id: str) -> List[Rule]:
        """Returns all rules whose consequent establishes the given fact."""
        return self.rules_by_consequent.get(goal_fact_id, [])

    def get_symptom(self, symptom_id: str) -> Optional[Dict[str, Any]]:
        return self.symptoms.get(symptom_id)

    def get_condition(self, condition_id: str) -> Optional[Dict[str, Any]]:
        return self.conditions.get(condition_id)

    def get_reference(self, ref_id: str) -> Optional[Dict[str, Any]]:
        return self.references.get(ref_id)

    def get_emergency_symptoms(self) -> List[Dict[str, Any]]:
        return [s for s in self.symptoms.values() if s.get("is_emergency", False)]

    def extract_leaf_facts_from_expression(self, expr: Dict[str, Any]) -> Set[str]:
        """Collects all base fact identifiers referenced in an expression."""
        facts: Set[str] = set()
        if "fact" in expr:
            facts.add(expr["fact"])
        elif "and" in expr:
            for child in expr["and"]:
                facts.update(self.extract_leaf_facts_from_expression(child))
        elif "or" in expr:
            for child in expr["or"]:
                facts.update(self.extract_leaf_facts_from_expression(child))
        elif "not" in expr:
            facts.update(self.extract_leaf_facts_from_expression(expr["not"]))
        return facts
