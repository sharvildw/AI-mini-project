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


def test_expanded_kb_scale(system_components):
    """Verify that the knowledge base has been substantially expanded."""
    kb, fc, bc, expl, safety = system_components
    assert len(kb.symptoms) >= 50, f"Expected at least 50 symptoms, got {len(kb.symptoms)}"
    assert len(kb.conditions) >= 15, f"Expected at least 15 conditions, got {len(kb.conditions)}"
    assert len(kb.rules) >= 40, f"Expected at least 40 rules, got {len(kb.rules)}"
    assert len(kb.references) >= 15, f"Expected at least 15 references, got {len(kb.references)}"


def test_covid_deduction(system_components):
    """Verify forward deduction for COVID-19 via sensory loss and fever."""
    kb, fc, bc, expl, safety = system_components
    input_facts = {
        "fever_present": Fact(id="fever_present", value=TruthValue.TRUE),
        "loss_of_taste_or_smell_present": Fact(id="loss_of_taste_or_smell_present", value=TruthValue.TRUE),
    }
    fc_res = fc.run(input_facts)
    supported_ids = [h["condition_id"] for h in fc_res.supported_hypotheses]
    assert "covid_19_pattern_supported" in supported_ids


def test_strep_throat_deduction(system_components):
    """Verify forward deduction for Streptococcal Pharyngitis via Centor criteria."""
    kb, fc, bc, expl, safety = system_components
    input_facts = {
        "sore_throat_present": Fact(id="sore_throat_present", value=TruthValue.TRUE),
        "fever_present": Fact(id="fever_present", value=TruthValue.TRUE),
        "tonsillar_exudate_present": Fact(id="tonsillar_exudate_present", value=TruthValue.TRUE),
    }
    fc_res = fc.run(input_facts)
    supported_ids = [h["condition_id"] for h in fc_res.supported_hypotheses]
    assert "strep_throat_pattern_supported" in supported_ids


def test_candidate_differential_hypotheses(system_components):
    """Verify that partial symptom matches return valid differential candidates with missing symptoms."""
    kb, fc, bc, expl, safety = system_components
    # Patient only has sore throat and fever (missing tonsillar exudate or lymph nodes for strep throat)
    input_facts = {
        "sore_throat_present": Fact(id="sore_throat_present", value=TruthValue.TRUE),
        "fever_present": Fact(id="fever_present", value=TruthValue.TRUE),
    }
    fc_res = fc.run(input_facts)
    supported_ids = {h["condition_id"] for h in fc_res.supported_hypotheses}
    candidates = expl.find_candidate_and_differential_hypotheses(fc_res.working_memory, supported_ids)

    cand_ids = [c["condition_id"] for c in candidates]
    assert "strep_throat_pattern_supported" in cand_ids
    strep_cand = next(c for c in candidates if c["condition_id"] == "strep_throat_pattern_supported")
    assert strep_cand["match_score"] >= 50
    assert len(strep_cand["missing_symptoms"]) > 0


def test_new_emergency_red_flags(system_components):
    """Verify that new high-acuity red flags trigger immediate emergency warnings."""
    kb, fc, bc, expl, safety = system_components
    input_facts = {
        "radiating_chest_pain_present": Fact(id="radiating_chest_pain_present", value=TruthValue.TRUE),
        "bloody_stool_present": Fact(id="bloody_stool_present", value=TruthValue.TRUE),
    }
    safe_rep = safety.check_safety(input_facts)
    assert safe_rep.has_emergency
    alert_syms = [a.symptom_id for a in safe_rep.alerts]
    assert "radiating_chest_pain_present" in alert_syms
    assert "bloody_stool_present" in alert_syms

