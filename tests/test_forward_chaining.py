"""Tests for Forward Chaining Inference Engine."""

import pytest
from engine.knowledge_base import Fact, FactSource, KnowledgeBase, Rule, TruthValue
from engine.forward_chaining import ForwardChainingEngine


@pytest.fixture
def kb():
    return KnowledgeBase()


def test_forward_chaining_direct_single_step(kb):
    """Test direct firing of a single rule (e.g. R005)."""
    engine = ForwardChainingEngine(kb)
    facts = {
        "nasal_congestion_present": Fact(id="nasal_congestion_present", value=TruthValue.TRUE),
        "sore_throat_present": Fact(id="sore_throat_present", value=TruthValue.TRUE),
    }
    result = engine.run(facts)
    assert "nasopharyngeal_catarrh_supported" in result.derived_facts
    assert result.derived_facts["nasopharyngeal_catarrh_supported"].value == TruthValue.TRUE
    assert any(r.id == "R005" for r in result.fired_rules)


def test_forward_chaining_missing_evidence_does_not_fire(kb):
    """Rule R001 requires fever, cough, fatigue. If fatigue is missing, rule must not fire."""
    engine = ForwardChainingEngine(kb)
    facts = {
        "fever_present": Fact(id="fever_present", value=TruthValue.TRUE),
        "cough_present": Fact(id="cough_present", value=TruthValue.TRUE),
        # fatigue_present is missing (UNKNOWN)
    }
    result = engine.run(facts)
    assert "acute_febrile_respiratory_syndrome_supported" not in result.derived_facts
    assert not any(r.id == "R001" for r in result.fired_rules)


def test_forward_chaining_multi_step_deduction(kb):
    """Test 3-tier multi-step chaining:
    Step 1: fever + cough + fatigue -> acute_febrile_respiratory_syndrome (R001)
    Step 2: acute_febrile_respiratory_syndrome + body_aches -> influenza_like_illness (R002)
    Step 3: influenza_like_illness + high_fever + chills -> severe_influenza_like (R003)
    """
    engine = ForwardChainingEngine(kb)
    facts = {
        "fever_present": Fact(id="fever_present", value=TruthValue.TRUE),
        "cough_present": Fact(id="cough_present", value=TruthValue.TRUE),
        "fatigue_present": Fact(id="fatigue_present", value=TruthValue.TRUE),
        "body_aches_present": Fact(id="body_aches_present", value=TruthValue.TRUE),
        "high_fever_present": Fact(id="high_fever_present", value=TruthValue.TRUE),
        "chills_present": Fact(id="chills_present", value=TruthValue.TRUE),
    }
    result = engine.run(facts)

    assert "acute_febrile_respiratory_syndrome_supported" in result.derived_facts
    assert "influenza_like_illness_supported" in result.derived_facts
    assert "severe_influenza_like_pattern_supported" in result.derived_facts

    fired_ids = [r.id for r in result.fired_rules]
    assert "R001" in fired_ids
    assert "R002" in fired_ids
    assert "R003" in fired_ids

    # Supported condition hypotheses should include both ILI and Severe ILI
    hypo_ids = [h["condition_id"] for h in result.supported_hypotheses]
    assert "influenza_like_illness_supported" in hypo_ids
    assert "severe_influenza_like_pattern_supported" in hypo_ids


def test_forward_chaining_or_expression(kb):
    """Test rule with OR condition (R006: catarrh AND (cough OR sneezing))."""
    engine = ForwardChainingEngine(kb)
    # Give catarrh and sneezing (cough absent)
    facts = {
        "nasal_congestion_present": Fact(id="nasal_congestion_present", value=TruthValue.TRUE),
        "sore_throat_present": Fact(id="sore_throat_present", value=TruthValue.TRUE),
        "sneezing_present": Fact(id="sneezing_present", value=TruthValue.TRUE),
    }
    result = engine.run(facts)
    assert "nasopharyngeal_catarrh_supported" in result.derived_facts
    assert "common_cold_like_illness_supported" in result.derived_facts


def test_forward_chaining_duplicate_fact_prevention(kb):
    """Verify that multiple rules deriving the same fact do not duplicate working memory entries."""
    engine = ForwardChainingEngine(kb)
    # Both R008 and R010 can relate to allergic rhinitis
    facts = {
        "sneezing_present": Fact(id="sneezing_present", value=TruthValue.TRUE),
        "clear_rhinorrhea_present": Fact(id="clear_rhinorrhea_present", value=TruthValue.TRUE),
        "itchy_eyes_present": Fact(id="itchy_eyes_present", value=TruthValue.TRUE),
        "allergen_exposure_trigger_present": Fact(id="allergen_exposure_trigger_present", value=TruthValue.TRUE),
    }
    result = engine.run(facts)
    assert "allergic_rhinitis_pattern_supported" in result.derived_facts
    # Fact store has exactly 1 entry for the condition
    assert list(result.working_memory.keys()).count("allergic_rhinitis_pattern_supported") == 1


def test_forward_chaining_multiple_supported_hypotheses(kb):
    """Test overlapping symptoms supporting multiple non-conflicting educational hypotheses."""
    engine = ForwardChainingEngine(kb)
    # Present symptoms for Migraine AND Gastroenteritis
    facts = {
        "headache_present": Fact(id="headache_present", value=TruthValue.TRUE),
        "unilateral_throbbing_headache_present": Fact(id="unilateral_throbbing_headache_present", value=TruthValue.TRUE),
        "photophobia_present": Fact(id="photophobia_present", value=TruthValue.TRUE),
        "watery_diarrhea_present": Fact(id="watery_diarrhea_present", value=TruthValue.TRUE),
        "nausea_present": Fact(id="nausea_present", value=TruthValue.TRUE),
        "vomiting_present": Fact(id="vomiting_present", value=TruthValue.TRUE),
    }
    result = engine.run(facts)
    hypo_ids = [h["condition_id"] for h in result.supported_hypotheses]
    assert "migraine_like_headache_pattern_supported" in hypo_ids
    assert "acute_gastroenteritis_pattern_supported" in hypo_ids


def test_forward_chaining_cyclic_rule_termination():
    """Verify that a synthetic cyclic knowledge base terminates safely via fixed-point or limit."""
    cyclic_kb = KnowledgeBase()
    # Artificially inject cyclic rules A -> B and B -> A
    cyclic_rule1 = Rule(
        id="CYC1",
        name="Cycle Rule 1",
        category="Test",
        readable_text="IF fact_a THEN fact_b",
        antecedent={"fact": "fact_a", "value": "TRUE"},
        consequent={"fact": "fact_b", "value": "TRUE"},
        explanation="",
        source="",
    )
    cyclic_rule2 = Rule(
        id="CYC2",
        name="Cycle Rule 2",
        category="Test",
        readable_text="IF fact_b THEN fact_a",
        antecedent={"fact": "fact_b", "value": "TRUE"},
        consequent={"fact": "fact_a", "value": "TRUE"},
        explanation="",
        source="",
    )
    cyclic_kb.rules = [cyclic_rule1, cyclic_rule2]

    engine = ForwardChainingEngine(cyclic_kb, max_iterations=10)
    facts = {"fact_a": Fact(id="fact_a", value=TruthValue.TRUE)}
    result = engine.run(facts)

    # Must terminate without infinite loop
    assert result.iterations_run <= 3  # Terminates as soon as fact_b and fact_a are both in memory!
    assert "fact_b" in result.derived_facts
