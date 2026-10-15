"""Independent Clinical Safety Layer and Emergency Warning Monitor.

Operates autonomously from diagnostic inference engines to detect configured
life-threatening 'red flag' symptoms and surface mandatory emergency protocols.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from .knowledge_base import Fact, KnowledgeBase, TruthValue


@dataclass
class EmergencyAlert:
    """Represents a high-priority red flag medical emergency alert."""
    symptom_id: str
    symptom_name: str
    severity: str
    clinical_rationale: str
    action_directive: str
    reference_source: str = "REF_EMERGENCY_RED_FLAGS"


@dataclass
class SafetyCheckResult:
    """Comprehensive safety evaluation report."""
    has_emergency: bool
    alerts: List[EmergencyAlert] = field(default_factory=list)
    emergency_contacts: List[Dict[str, str]] = field(default_factory=list)
    disclaimer: str = (
        "EDUCATIONAL PURPOSES ONLY: MediLogic is an academic expert system for "
        "demonstrating symbolic artificial intelligence and rule-based inference. "
        "It is NOT a certified medical diagnostic device and does NOT replace licensed medical care."
    )


class SafetyEngine:
    """Evaluates working facts against independent red-flag emergency protocols."""

    RED_FLAG_DEFINITIONS: Dict[str, Dict[str, str]] = {
        "chest_pain_present": {
            "name": "Chest Pain / Pressure",
            "severity": "CRITICAL EMERGENCY",
            "rationale": "Unexplained chest pain, tightness, or pressure may indicate acute coronary syndrome, aortic dissection, or pulmonary embolism.",
            "directive": "Call emergency services immediately (911 / 112 / 108). Do not drive yourself to the hospital.",
        },
        "severe_shortness_of_breath_present": {
            "name": "Severe Shortness of Breath",
            "severity": "CRITICAL EMERGENCY",
            "rationale": "Acute severe dyspnea may indicate severe asthma exacerbation, anaphylaxis, pulmonary embolism, or respiratory failure.",
            "directive": "Seek immediate emergency medical care. Sit upright and call local emergency responders.",
        },
        "sudden_neurological_deficit_present": {
            "name": "Sudden Neurological Deficit",
            "severity": "TIME-CRITICAL EMERGENCY",
            "rationale": "Sudden unilateral weakness, facial droop, or speech impairment strongly indicates acute cerebral ischemia (stroke).",
            "directive": "Act FAST (Face, Arms, Speech, Time). Call emergency services immediately without delay.",
        },
        "stiff_neck_with_high_fever_present": {
            "name": "Stiff Neck with High Fever",
            "severity": "URGENT EMERGENCY",
            "rationale": "Nuchal rigidity accompanied by high fever and altered mental status represents classic signs of acute bacterial meningitis.",
            "directive": "Proceed immediately to the nearest Emergency Department for urgent physician evaluation.",
        },
        "severe_unrelenting_abdominal_pain_present": {
            "name": "Severe Unrelenting Abdominal Pain",
            "severity": "HIGH URGENCY",
            "rationale": "Rigid or excruciating abdominal pain may signal acute appendicitis, bowel perforation, or acute surgical abdomen.",
            "directive": "Seek urgent hospital emergency care. Do not eat or drink pending surgical evaluation.",
        },
    }

    EMERGENCY_NUMBERS: List[Dict[str, str]] = [
        {"region": "International / Europe / India", "number": "112", "service": "Unified Emergency Services"},
        {"region": "United States & Canada", "number": "911", "service": "Emergency Dispatch"},
        {"region": "United Kingdom", "number": "999 / 111", "service": "Emergency / NHS Urgent Helpline"},
        {"region": "India (Ambulance)", "number": "108 / 102", "service": "Emergency Ambulance Service"},
    ]

    def __init__(self, kb: Optional[KnowledgeBase] = None) -> None:
        self.kb = kb

    def check_safety(self, fact_store: Dict[str, Fact]) -> SafetyCheckResult:
        """Inspects fact store for active emergency red flags."""
        alerts: List[EmergencyAlert] = []

        for symptom_id, info in self.RED_FLAG_DEFINITIONS.items():
            fact = fact_store.get(symptom_id)
            if fact is not None and fact.value == TruthValue.TRUE:
                alerts.append(
                    EmergencyAlert(
                        symptom_id=symptom_id,
                        symptom_name=info["name"],
                        severity=info["severity"],
                        clinical_rationale=info["rationale"],
                        action_directive=info["directive"],
                    )
                )

        has_emerg = len(alerts) > 0
        return SafetyCheckResult(
            has_emergency=has_emerg,
            alerts=alerts,
            emergency_contacts=self.EMERGENCY_NUMBERS,
        )
