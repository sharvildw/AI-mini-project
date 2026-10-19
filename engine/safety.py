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
        "radiating_chest_pain_present": {
            "name": "Radiating Chest Pain to Arm/Jaw/Back",
            "severity": "CRITICAL EMERGENCY",
            "rationale": "Chest discomfort radiating to the left arm, neck, jaw, or back is a hallmark presentation of Acute Coronary Syndrome (myocardial infarction).",
            "directive": "Call emergency services immediately (911 / 112 / 108). Keep calm, rest quietly, and chew an aspirin if non-allergic.",
        },
        "cold_sweats_diaphoresis_present": {
            "name": "Cold Sweats / Profuse Clamminess",
            "severity": "HIGH URGENCY",
            "rationale": "Sudden cold diaphoresis accompanying chest or abdominal distress indicates autonomic shock, acute cardiac ischemia, or severe sepsis.",
            "directive": "Seek immediate emergency clinical evaluation.",
        },
        "syncope_fainting_present": {
            "name": "Fainting / Sudden Loss of Consciousness",
            "severity": "TIME-CRITICAL EMERGENCY",
            "rationale": "Transient loss of consciousness can signify cardiac arrhythmia, acute pulmonary embolism, or critical intracranial hypotension.",
            "directive": "Lay the patient flat with legs elevated and call emergency medical services immediately.",
        },
        "hemoptysis_coughing_blood_present": {
            "name": "Coughing Up Blood (Hemoptysis)",
            "severity": "HIGH URGENCY",
            "rationale": "Expectoration of blood or blood-streaked sputum indicates pulmonary hemorrhage, pulmonary embolism, or severe lower respiratory tract pathology.",
            "directive": "Go to the nearest emergency department or urgent chest clinic immediately.",
        },
        "focal_right_lower_quadrant_pain_present": {
            "name": "Severe Right Lower Quadrant Abdominal Pain",
            "severity": "SURGICAL URGENCY",
            "rationale": "Persistent focal tenderness and guarding in the right lower abdomen is the cardinal sign of acute appendicitis.",
            "directive": "Proceed immediately to the emergency department for surgical evaluation. Do not take laxatives or pain relievers before examination.",
        },
        "bloody_stool_present": {
            "name": "Visible Blood in Stool / Black Tarry Stool",
            "severity": "HIGH URGENCY",
            "rationale": "Gastrointestinal bleeding or invasive enteric infection (dysentery) requires urgent medical diagnostic assessment.",
            "directive": "Seek prompt medical or emergency care for hydration and endoscopic/microbiological evaluation.",
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
