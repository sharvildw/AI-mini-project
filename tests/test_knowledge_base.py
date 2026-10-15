"""Tests for Knowledge Base Loading, Schema Validation, and Integrity Checks."""

import json
from pathlib import Path
import pytest

from engine.knowledge_base import (
    KnowledgeBase,
    KnowledgeBaseValidationError,
    TruthValue,
    FactSource,
    Fact,
    Rule,
)


def test_knowledge_base_loads_successfully():
    """Verify that the standard knowledge base loads without errors."""
    kb = KnowledgeBase()
    assert len(kb.rules) >= 20
    assert len(kb.symptoms) >= 30
    assert len(kb.conditions) >= 6
    assert len(kb.references) >= 5


def test_unique_rule_ids():
    """Ensure all rule IDs in knowledge base are unique."""
    kb = KnowledgeBase()
    rule_ids = [r.id for r in kb.rules]
    assert len(rule_ids) == len(set(rule_ids))


def test_rule_references_valid_sources():
    """Ensure every rule points to a valid entry in references.json."""
    kb = KnowledgeBase()
    for rule in kb.rules:
        if rule.source:
            assert rule.source in kb.references, f"Rule {rule.id} references missing source {rule.source}"


def test_symptom_attributes():
    """Verify that symptoms contain expected attributes."""
    kb = KnowledgeBase()
    for sid, s in kb.symptoms.items():
        assert "name" in s
        assert "category" in s
        assert "description" in s
        assert "is_emergency" in s
        assert isinstance(s["is_emergency"], bool)


def test_conditions_have_features_and_differentials():
    """Verify condition schema integrity."""
    kb = KnowledgeBase()
    for cid, cond in kb.conditions.items():
        assert "name" in cond
        assert "clinical_features" in cond
        assert "differential_considerations" in cond


def test_duplicate_rule_id_detection(tmp_path):
    """Test that a duplicate rule ID raises KnowledgeBaseValidationError."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    # Write minimal references
    (data_dir / "references.json").write_text(json.dumps({"REF1": {"id": "REF1"}}))
    (data_dir / "symptoms.json").write_text(json.dumps([{"id": "s1", "name": "S1", "category": "C", "description": "D", "is_emergency": False}]))
    (data_dir / "conditions.json").write_text(json.dumps([{"id": "c1", "name": "C1", "category": "C", "description": "D", "clinical_features": []}]))

    # Duplicate rules
    dup_rules = [
        {"id": "R1", "name": "Rule 1", "antecedent": {"fact": "s1"}, "consequent": {"fact": "c1"}},
        {"id": "R1", "name": "Duplicate Rule 1", "antecedent": {"fact": "s1"}, "consequent": {"fact": "c1"}},
    ]
    (data_dir / "rules.json").write_text(json.dumps(dup_rules))

    with pytest.raises(KnowledgeBaseValidationError, match="Duplicate rule ID"):
        KnowledgeBase(data_dir=data_dir)


def test_malformed_expression_detection(tmp_path):
    """Test that an invalid expression structure raises KnowledgeBaseValidationError."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    (data_dir / "references.json").write_text(json.dumps({}))
    (data_dir / "symptoms.json").write_text(json.dumps([]))
    (data_dir / "conditions.json").write_text(json.dumps([]))

    invalid_rules = [
        {"id": "R1", "name": "Bad Expr", "antecedent": {"invalid_operator": 123}, "consequent": {"fact": "c1"}}
    ]
    (data_dir / "rules.json").write_text(json.dumps(invalid_rules))

    with pytest.raises(KnowledgeBaseValidationError, match="Unrecognized logical expression structure"):
        KnowledgeBase(data_dir=data_dir)


def test_missing_files_handling(tmp_path):
    """Test that missing required files raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        KnowledgeBase(data_dir=tmp_path)


def test_truth_value_conversion():
    """Test conversion helper for tri-state logic."""
    assert TruthValue.from_bool_or_str(True) == TruthValue.TRUE
    assert TruthValue.from_bool_or_str(False) == TruthValue.FALSE
    assert TruthValue.from_bool_or_str("true") == TruthValue.TRUE
    assert TruthValue.from_bool_or_str("false") == TruthValue.FALSE
    assert TruthValue.from_bool_or_str("unknown") == TruthValue.UNKNOWN
    assert TruthValue.from_bool_or_str(None) == TruthValue.UNKNOWN
