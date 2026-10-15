"""Tests for Three-Valued Logical Rule Evaluator."""

import pytest
from engine.knowledge_base import Fact, FactSource, TruthValue
from engine.rule_evaluator import RuleEvaluator


@pytest.fixture
def base_facts():
    return {
        "fever_present": Fact(id="fever_present", value=TruthValue.TRUE, source=FactSource.USER),
        "cough_present": Fact(id="cough_present", value=TruthValue.TRUE, source=FactSource.USER),
        "chest_pain_present": Fact(id="chest_pain_present", value=TruthValue.FALSE, source=FactSource.USER),
        "headache_present": Fact(id="headache_present", value=TruthValue.UNKNOWN, source=FactSource.USER),
    }


def test_atomic_true(base_facts):
    expr = {"fact": "fever_present", "value": "TRUE"}
    res = RuleEvaluator.evaluate(expr, base_facts)
    assert res.value == TruthValue.TRUE
    assert res.is_true


def test_atomic_false_contradiction(base_facts):
    expr = {"fact": "chest_pain_present", "value": "TRUE"}
    res = RuleEvaluator.evaluate(expr, base_facts)
    assert res.value == TruthValue.FALSE
    assert res.is_false
    assert "chest_pain_present" in res.contradicted_facts


def test_atomic_unknown_explicit(base_facts):
    expr = {"fact": "headache_present", "value": "TRUE"}
    res = RuleEvaluator.evaluate(expr, base_facts)
    assert res.value == TruthValue.UNKNOWN
    assert res.is_unknown
    assert "headache_present" in res.missing_facts


def test_atomic_unknown_unspecified(base_facts):
    expr = {"fact": "unlisted_symptom", "value": "TRUE"}
    res = RuleEvaluator.evaluate(expr, base_facts)
    assert res.value == TruthValue.UNKNOWN
    assert res.is_unknown
    assert "unlisted_symptom" in res.missing_facts


def test_not_operator(base_facts):
    # NOT (chest_pain == TRUE) where chest_pain is FALSE -> child is FALSE -> NOT is TRUE
    expr1 = {"not": {"fact": "chest_pain_present", "value": "TRUE"}}
    res1 = RuleEvaluator.evaluate(expr1, base_facts)
    assert res1.value == TruthValue.TRUE

    # NOT (fever == TRUE) where fever is TRUE -> child is TRUE -> NOT is FALSE
    expr2 = {"not": {"fact": "fever_present", "value": "TRUE"}}
    res2 = RuleEvaluator.evaluate(expr2, base_facts)
    assert res2.value == TruthValue.FALSE

    # NOT (headache == TRUE) where headache is UNKNOWN -> NOT is UNKNOWN
    expr3 = {"not": {"fact": "headache_present", "value": "TRUE"}}
    res3 = RuleEvaluator.evaluate(expr3, base_facts)
    assert res3.value == TruthValue.UNKNOWN


def test_and_all_true(base_facts):
    expr = {
        "and": [
            {"fact": "fever_present", "value": "TRUE"},
            {"fact": "cough_present", "value": "TRUE"},
        ]
    }
    res = RuleEvaluator.evaluate(expr, base_facts)
    assert res.value == TruthValue.TRUE


def test_and_one_false(base_facts):
    expr = {
        "and": [
            {"fact": "fever_present", "value": "TRUE"},
            {"fact": "chest_pain_present", "value": "TRUE"},  # FALSE
        ]
    }
    res = RuleEvaluator.evaluate(expr, base_facts)
    assert res.value == TruthValue.FALSE
    assert "chest_pain_present" in res.contradicted_facts


def test_and_one_unknown_no_false(base_facts):
    expr = {
        "and": [
            {"fact": "fever_present", "value": "TRUE"},
            {"fact": "headache_present", "value": "TRUE"},  # UNKNOWN
        ]
    }
    res = RuleEvaluator.evaluate(expr, base_facts)
    assert res.value == TruthValue.UNKNOWN
    assert "headache_present" in res.missing_facts


def test_or_one_true(base_facts):
    expr = {
        "or": [
            {"fact": "fever_present", "value": "TRUE"},      # TRUE
            {"fact": "chest_pain_present", "value": "TRUE"},  # FALSE
        ]
    }
    res = RuleEvaluator.evaluate(expr, base_facts)
    assert res.value == TruthValue.TRUE


def test_or_all_false(base_facts):
    expr = {
        "or": [
            {"fact": "chest_pain_present", "value": "TRUE"},   # FALSE
            {"fact": "fever_present", "value": "FALSE"},       # FALSE (since fever is TRUE)
        ]
    }
    res = RuleEvaluator.evaluate(expr, base_facts)
    assert res.value == TruthValue.FALSE


def test_or_mixed_false_and_unknown(base_facts):
    expr = {
        "or": [
            {"fact": "chest_pain_present", "value": "TRUE"},   # FALSE
            {"fact": "headache_present", "value": "TRUE"},     # UNKNOWN
        ]
    }
    res = RuleEvaluator.evaluate(expr, base_facts)
    assert res.value == TruthValue.UNKNOWN


def test_nested_complex_expression(base_facts):
    # fever AND (chest_pain OR cough) -> TRUE AND (FALSE OR TRUE) -> TRUE AND TRUE -> TRUE
    expr = {
        "and": [
            {"fact": "fever_present", "value": "TRUE"},
            {
                "or": [
                    {"fact": "chest_pain_present", "value": "TRUE"},
                    {"fact": "cough_present", "value": "TRUE"},
                ]
            },
        ]
    }
    res = RuleEvaluator.evaluate(expr, base_facts)
    assert res.value == TruthValue.TRUE
