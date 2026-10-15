"""Tests for Independent Safety Layer and Emergency Protocols."""

import pytest
from engine.knowledge_base import Fact, TruthValue
from engine.safety import SafetyEngine


def test_safety_clean_when_no_red_flags():
    safety = SafetyEngine()
    facts = {
        "cough_present": Fact(id="cough_present", value=TruthValue.TRUE),
        "fever_present": Fact(id="fever_present", value=TruthValue.TRUE),
    }
    report = safety.check_safety(facts)
    assert not report.has_emergency
    assert len(report.alerts) == 0


def test_safety_chest_pain_triggers_emergency():
    safety = SafetyEngine()
    facts = {
        "chest_pain_present": Fact(id="chest_pain_present", value=TruthValue.TRUE),
        "cough_present": Fact(id="cough_present", value=TruthValue.TRUE),
    }
    report = safety.check_safety(facts)
    assert report.has_emergency
    assert any(a.symptom_id == "chest_pain_present" for a in report.alerts)


def test_safety_multiple_emergencies():
    safety = SafetyEngine()
    facts = {
        "chest_pain_present": Fact(id="chest_pain_present", value=TruthValue.TRUE),
        "severe_shortness_of_breath_present": Fact(id="severe_shortness_of_breath_present", value=TruthValue.TRUE),
        "stiff_neck_with_high_fever_present": Fact(id="stiff_neck_with_high_fever_present", value=TruthValue.TRUE),
    }
    report = safety.check_safety(facts)
    assert report.has_emergency
    assert len(report.alerts) == 3


def test_safety_false_or_unknown_does_not_alert():
    safety = SafetyEngine()
    facts = {
        "chest_pain_present": Fact(id="chest_pain_present", value=TruthValue.FALSE), # explicitly absent
        "severe_shortness_of_breath_present": Fact(id="severe_shortness_of_breath_present", value=TruthValue.UNKNOWN),
    }
    report = safety.check_safety(facts)
    assert not report.has_emergency
    assert len(report.alerts) == 0
