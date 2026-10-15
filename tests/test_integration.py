"""Integration Tests for MediLogic System."""

import pytest
from engine.knowledge_base import Fact, FactSource, KnowledgeBase, TruthValue
from engine.forward_chaining import ForwardChainingEngine
from engine.backward_chaining import BackwardChainingEngine, GoalStatus
from engine.explanation import ExplanationEngine
from engine.safety import SafetyEngine


@pytest.fixture
def system_components():
    kb = KnowledgeBase()
    fc = ForwardChainingEngine(kb)
    bc = BackwardChainingEngine(kb)
    expl = ExplanationEngine(kb)
    safety = SafetyEngine(kb)
    return kb, fc, bc, expl, safety


def test_cross_algorithm_consistency_on_influenza(system_components):
    """Verify that both Forward and Backward chaining reach harmonious conclusions
    given facts supporting Influenza-Like Illness."""
    kb, fc, bc, expl, safety = system_components

    input_facts = {
        "fever_present": Fact(id="fever_present", value=TruthValue.TRUE),
        "cough_present": Fact(id="cough_present", value=TruthValue.TRUE),
        "fatigue_present": Fact(id="fatigue_present", value=TruthValue.TRUE),
        "body_aches_present": Fact(id="body_aches_present", value=TruthValue.TRUE),
    }

    # 1. Forward chaining
    fc_res = fc.run(input_facts)
    supported_hypo_ids = [h["condition_id"] for h in fc_res.supported_hypotheses]
    assert "influenza_like_illness_supported" in supported_hypo_ids

    # 2. Backward chaining target ILI
    bc_res = bc.run("influenza_like_illness_supported", input_facts)
    assert bc_res.status == GoalStatus.SUPPORTED

    # 3. Explanation engine comparison
    comp = expl.compare_engines(fc_res, bc_res)
    assert comp["agreement"] is True
    assert comp["forward_target_supported"] is True
    assert comp["backward_target_supported"] is True

    # 4. Safety layer remains clean
    safe_rep = safety.check_safety(input_facts)
    assert not safe_rep.has_emergency


def test_cross_algorithm_consistency_on_insufficient_evidence(system_components):
    """Verify that both algorithms agree when evidence is insufficient."""
    kb, fc, bc, expl, safety = system_components

    input_facts = {
        "fever_present": Fact(id="fever_present", value=TruthValue.TRUE),
        # Missing cough, fatigue, body_aches
    }

    fc_res = fc.run(input_facts)
    supported_hypo_ids = [h["condition_id"] for h in fc_res.supported_hypotheses]
    assert "influenza_like_illness_supported" not in supported_hypo_ids

    bc_res = bc.run("influenza_like_illness_supported", input_facts)
    assert bc_res.status == GoalStatus.UNRESOLVED_UNKNOWN

    comp = expl.compare_engines(fc_res, bc_res)
    assert comp["agreement"] is True
    assert comp["forward_target_supported"] is False
    assert comp["backward_target_supported"] is False


def test_safety_alert_coexists_with_diagnosis(system_components):
    """Verify that an emergency red flag is triggered and NOT suppressed
    even if a standard educational condition rule fires simultaneously."""
    kb, fc, bc, expl, safety = system_components

    input_facts = {
        "nasal_congestion_present": Fact(id="nasal_congestion_present", value=TruthValue.TRUE),
        "sore_throat_present": Fact(id="sore_throat_present", value=TruthValue.TRUE),
        "cough_present": Fact(id="cough_present", value=TruthValue.TRUE),
        # Emergency red flag
        "chest_pain_present": Fact(id="chest_pain_present", value=TruthValue.TRUE),
    }

    # Diagnosis rule fires for common cold
    fc_res = fc.run(input_facts)
    assert "common_cold_like_illness_supported" in [h["condition_id"] for h in fc_res.supported_hypotheses]

    # Safety alert is independent and active
    safe_rep = safety.check_safety(input_facts)
    assert safe_rep.has_emergency
    assert any(a.symptom_id == "chest_pain_present" for a in safe_rep.alerts)
