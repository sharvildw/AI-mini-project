"""Tests for Goal-Directed Backward Chaining Inference Engine."""

import pytest
from engine.knowledge_base import Fact, FactSource, KnowledgeBase, Rule, TruthValue
from engine.backward_chaining import BackwardChainingEngine, GoalStatus


@pytest.fixture
def kb():
    return KnowledgeBase()


def test_backward_chaining_direct_fact(kb):
    """Test goal directly proven because it is already known in working memory."""
    engine = BackwardChainingEngine(kb)
    facts = {
        "influenza_like_illness_supported": Fact(
            id="influenza_like_illness_supported",
            value=TruthValue.TRUE,
            source=FactSource.USER,
        )
    }
    result = engine.run("influenza_like_illness_supported", facts)
    assert result.status == GoalStatus.SUPPORTED
    assert result.proof_tree.status == GoalStatus.SUPPORTED
    assert "directly known" in result.proof_tree.explanation


def test_backward_chaining_intermediate_goal_deduction(kb):
    """Test goal requiring recursive backward search across multiple levels:
    Goal: influenza_like_illness_supported
    Rule candidate: R002 (requires acute_febrile_respiratory_syndrome_supported AND body_aches_present)
    Subgoal acute_febrile_respiratory_syndrome_supported requires R001 (fever, cough, fatigue).
    """
    engine = BackwardChainingEngine(kb)
    facts = {
        "fever_present": Fact(id="fever_present", value=TruthValue.TRUE),
        "cough_present": Fact(id="cough_present", value=TruthValue.TRUE),
        "fatigue_present": Fact(id="fatigue_present", value=TruthValue.TRUE),
        "body_aches_present": Fact(id="body_aches_present", value=TruthValue.TRUE),
    }
    result = engine.run("influenza_like_illness_supported", facts)
    assert result.status == GoalStatus.SUPPORTED
    applied_ids = [r.id for r in result.applied_rules]
    assert "R001" in applied_ids
    assert "R002" in applied_ids
    assert len(result.missing_prerequisites) == 0


def test_backward_chaining_unknown_prerequisite_is_not_false(kb):
    """Test that a goal lacking evidence remains UNRESOLVED_UNKNOWN rather than FALSE."""
    engine = BackwardChainingEngine(kb)
    facts = {
        "fever_present": Fact(id="fever_present", value=TruthValue.TRUE),
        "cough_present": Fact(id="cough_present", value=TruthValue.TRUE),
        # fatigue_present and body_aches_present are missing!
    }
    result = engine.run("influenza_like_illness_supported", facts)
    assert result.status == GoalStatus.UNRESOLVED_UNKNOWN
    assert "fatigue_present" in result.missing_prerequisites or "body_aches_present" in result.missing_prerequisites


def test_backward_chaining_explicit_contradiction(kb):
    """Test that when a required symptom is explicitly established as FALSE, goal fails/contradicts."""
    engine = BackwardChainingEngine(kb)
    # Target: acute_gastroenteritis_pattern_supported (requires watery_diarrhea + nausea)
    facts = {
        "watery_diarrhea_present": Fact(id="watery_diarrhea_present", value=TruthValue.FALSE), # explicitly absent!
        "nausea_present": Fact(id="nausea_present", value=TruthValue.TRUE),
        "vomiting_present": Fact(id="vomiting_present", value=TruthValue.FALSE),
        "abdominal_cramps_present": Fact(id="abdominal_cramps_present", value=TruthValue.FALSE),
        "fever_present": Fact(id="fever_present", value=TruthValue.FALSE),
    }
    result = engine.run("acute_gastroenteritis_pattern_supported", facts)
    assert result.status == GoalStatus.CONTRADICTED_OR_FAILED


def test_backward_chaining_or_branch_alternative_success(kb):
    """Test that when candidate rule R009 has an OR condition (itchy_eyes OR itchy_palate),
    having one of them allows successful proof of the goal."""
    engine = BackwardChainingEngine(kb)
    facts = {
        "sneezing_present": Fact(id="sneezing_present", value=TruthValue.TRUE),
        "clear_rhinorrhea_present": Fact(id="clear_rhinorrhea_present", value=TruthValue.TRUE),
        "itchy_eyes_present": Fact(id="itchy_eyes_present", value=TruthValue.TRUE),
        # itchy_nose_or_palate is UNKNOWN
    }
    result = engine.run("allergic_rhinitis_pattern_supported", facts)
    assert result.status == GoalStatus.SUPPORTED
    applied_ids = [r.id for r in result.applied_rules]
    assert "R008" in applied_ids
    assert "R009" in applied_ids


def test_backward_chaining_cycle_detection():
    """Verify that circular rule dependencies are detected and halted safely."""
    cyclic_kb = KnowledgeBase()
    # G1 -> G2 -> G1
    cyclic_kb.rules = [
        Rule(
            id="CR1",
            name="Cycle 1",
            category="Test",
            readable_text="IF G2 THEN G1",
            antecedent={"fact": "G2", "value": "TRUE"},
            consequent={"fact": "G1", "value": "TRUE"},
            explanation="",
            source="",
        ),
        Rule(
            id="CR2",
            name="Cycle 2",
            category="Test",
            readable_text="IF G1 THEN G2",
            antecedent={"fact": "G1", "value": "TRUE"},
            consequent={"fact": "G2", "value": "TRUE"},
            explanation="",
            source="",
        ),
    ]
    cyclic_kb.rules_by_consequent = {
        "G1": [cyclic_kb.rules[0]],
        "G2": [cyclic_kb.rules[1]],
    }

    engine = BackwardChainingEngine(cyclic_kb, max_depth=10)
    result = engine.run("G1", {})
    # Should catch circular dependency and not enter infinite recursion
    assert result.status in (GoalStatus.CYCLE_DETECTED, GoalStatus.CONTRADICTED_OR_FAILED, GoalStatus.UNRESOLVED_UNKNOWN)
    trace_actions = [t.action for t in result.trace]
    assert "CYCLE_DETECTED" in trace_actions


def test_backward_chaining_depth_limit():
    """Verify that deep recursive chains stop cleanly when exceeding max_depth."""
    deep_kb = KnowledgeBase()
    rules = []
    for i in range(10):
        rules.append(
            Rule(
                id=f"D{i}",
                name=f"Deep {i}",
                category="Test",
                readable_text=f"IF F{i+1} THEN F{i}",
                antecedent={"fact": f"F{i+1}", "value": "TRUE"},
                consequent={"fact": f"F{i}", "value": "TRUE"},
                explanation="",
                source="",
            )
        )
    deep_kb.rules = rules
    deep_kb.rules_by_consequent = {f"F{i}": [rules[i]] for i in range(10)}

    engine = BackwardChainingEngine(deep_kb, max_depth=4)
    result = engine.run("F0", {})
    trace_actions = [t.action for t in result.trace]
    assert "DEPTH_LIMIT_EXCEEDED" in trace_actions
