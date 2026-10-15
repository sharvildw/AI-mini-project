"""Reusable UI Components and Renderers for Streamlit MediLogic App.

Provides simplified, beginner-friendly UI presentation components while preserving
underlying fact structures and clinical safety monitors.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
import streamlit as st

from engine.backward_chaining import GoalStatus
from engine.knowledge_base import Fact, FactSource, KnowledgeBase, TruthValue
from engine.safety import EmergencyAlert


# Friendly category mapping for non-technical users
SIMPLE_CATEGORY_MAPPING = {
    "General": [
        "fever_present",
        "high_fever_present",
        "body_aches_present",
        "fatigue_present",
        "chills_present",
        "rapid_onset_present",
    ],
    "Nose and Breathing": [
        "cough_present",
        "sore_throat_present",
        "nasal_congestion_present",
        "clear_rhinorrhea_present",
        "sneezing_present",
    ],
    "Head": [
        "headache_present",
        "unilateral_throbbing_headache_present",
        "photophobia_present",
        "phonophobia_present",
        "visual_aura_present",
        "worsened_by_routine_activity_present",
    ],
    "Stomach": [
        "nausea_present",
        "vomiting_present",
        "watery_diarrhea_present",
        "abdominal_cramps_present",
    ],
    "Other": [
        "itchy_eyes_present",
        "itchy_nose_or_palate_present",
        "allergen_exposure_trigger_present",
        "dysuria_present",
        "urinary_frequency_present",
        "urinary_urgency_present",
        "suprapubic_tenderness_present",
        "flank_pain_present",
    ],
    "Emergency Warning Signs": [
        "chest_pain_present",
        "severe_shortness_of_breath_present",
        "sudden_neurological_deficit_present",
        "stiff_neck_with_high_fever_present",
        "severe_unrelenting_abdominal_pain_present",
    ],
}

# Simplified human-friendly names and plain descriptions
SIMPLE_SYMPTOM_DETAILS = {
    "fever_present": {
        "title": "Fever",
        "desc": "Elevated body temperature (38°C / 100.4°F or higher)",
        "icon": "🌡️",
    },
    "high_fever_present": {
        "title": "High Fever",
        "desc": "Very high temperature (39°C / 102.2°F or higher)",
        "icon": "🔥",
    },
    "body_aches_present": {
        "title": "Body Aches",
        "desc": "Generalized muscle soreness and body discomfort",
        "icon": "💪",
    },
    "fatigue_present": {
        "title": "Feeling Tired / Weak",
        "desc": "Low energy, weakness, or general sluggishness",
        "icon": "😴",
    },
    "chills_present": {
        "title": "Chills or Shivering",
        "desc": "Feeling cold with involuntary shivering",
        "icon": "🥶",
    },
    "rapid_onset_present": {
        "title": "Sudden Onset",
        "desc": "Symptoms started quickly over a few hours rather than days",
        "icon": "⚡",
    },
    "cough_present": {
        "title": "Cough",
        "desc": "Frequent or dry/wet coughing",
        "icon": "🗣️",
    },
    "sore_throat_present": {
        "title": "Sore Throat",
        "desc": "Scratchy, painful, or irritated throat when swallowing",
        "icon": "🧣",
    },
    "nasal_congestion_present": {
        "title": "Stuffy Nose",
        "desc": "Blocked or congested nasal passages",
        "icon": "👃",
    },
    "clear_rhinorrhea_present": {
        "title": "Runny Nose (Clear)",
        "desc": "Thin, watery, clear liquid running from the nose",
        "icon": "💧",
    },
    "sneezing_present": {
        "title": "Frequent Sneezing",
        "desc": "Bouts of repeated sneezing",
        "icon": "🤧",
    },
    "headache_present": {
        "title": "Headache",
        "desc": "General pain or aching in the head",
        "icon": "🤕",
    },
    "unilateral_throbbing_headache_present": {
        "title": "Throbbing Headache on One Side",
        "desc": "Pulsating pain mostly on the left or right side of your head",
        "icon": "💥",
    },
    "photophobia_present": {
        "title": "Sensitive to Light",
        "desc": "Normal indoor light or sunlight hurts your eyes",
        "icon": "☀️",
    },
    "phonophobia_present": {
        "title": "Sensitive to Sound",
        "desc": "Ordinary sounds feel uncomfortably loud or painful",
        "icon": "🔊",
    },
    "visual_aura_present": {
        "title": "Vision Changes (Aura)",
        "desc": "Flashes of light, zigzag patterns, or blind spots before pain",
        "icon": "✨",
    },
    "worsened_by_routine_activity_present": {
        "title": "Headache Worse with Movement",
        "desc": "Walking, climbing stairs, or head movement worsens pain",
        "icon": "🚶",
    },
    "nausea_present": {
        "title": "Nausea",
        "desc": "Feeling sick to your stomach or inclined to vomit",
        "icon": "🤢",
    },
    "vomiting_present": {
        "title": "Vomiting",
        "desc": "Episodes of throwing up",
        "icon": "🤮",
    },
    "watery_diarrhea_present": {
        "title": "Watery Diarrhea",
        "desc": "Loose, watery stools 3 or more times in a day",
        "icon": "🚽",
    },
    "abdominal_cramps_present": {
        "title": "Stomach Discomfort / Cramps",
        "desc": "Mild to moderate cramping or tummy pain",
        "icon": "🩺",
    },
    "itchy_eyes_present": {
        "title": "Itchy or Watery Eyes",
        "desc": "Red, itchy, or watery eyes (allergic feeling)",
        "icon": "👁️",
    },
    "itchy_nose_or_palate_present": {
        "title": "Itchy Nose or Mouth Roof",
        "desc": "Itching inside the nose or on the roof of the mouth",
        "icon": "🌾",
    },
    "allergen_exposure_trigger_present": {
        "title": "Allergy Trigger",
        "desc": "Symptoms flared up around pollen, dust, animals, or season changes",
        "icon": "🌸",
    },
    "dysuria_present": {
        "title": "Urinary Discomfort",
        "desc": "Painful, burning sensation when passing urine",
        "icon": "⚠️",
    },
    "urinary_frequency_present": {
        "title": "Urinating Very Often",
        "desc": "Needing to urinate much more frequently than normal",
        "icon": "⏱️",
    },
    "urinary_urgency_present": {
        "title": "Urgent Need to Urinate",
        "desc": "Sudden, pressing urge that is difficult to hold",
        "icon": "🚨",
    },
    "suprapubic_tenderness_present": {
        "title": "Lower Pelvic Pressure",
        "desc": "Discomfort or heaviness in the lower central tummy area",
        "icon": "📍",
    },
    "flank_pain_present": {
        "title": "Lower Back or Side Pain",
        "desc": "Pain in the back or side area between the ribs and hips",
        "icon": "🩺",
    },
    "chest_pain_present": {
        "title": "Chest Pain or Pressure",
        "desc": "Severe pressure, tightness, squeezing, or chest pain",
        "icon": "💔",
    },
    "severe_shortness_of_breath_present": {
        "title": "Severe Shortness of Breath",
        "desc": "Gasping for air, unable to finish full sentences",
        "icon": "🫁",
    },
    "sudden_neurological_deficit_present": {
        "title": "Sudden Weakness or Speech Trouble",
        "desc": "Face drooping, sudden arm/leg weakness, or slurred speech",
        "icon": "🧠",
    },
    "stiff_neck_with_high_fever_present": {
        "title": "Stiff Neck with High Fever",
        "desc": "Inability to touch chin to chest accompanied by severe fever",
        "icon": "🔴",
    },
    "severe_unrelenting_abdominal_pain_present": {
        "title": "Severe Unrelenting Stomach Pain",
        "desc": "Agonizing, sudden, rigid, or unbearable stomach pain",
        "icon": "🚨",
    },
}


def render_home_hero() -> None:
    """Renders the simplified home hero banner."""
    st.markdown(
        """
        <div class="simple-hero">
            <h1>MediLogic</h1>
            <p>An easy way to explore how symptoms match educational medical rules.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Alias for backward compatibility
render_header = render_home_hero


def render_disclaimer() -> None:
    """Renders clean, friendly educational disclaimer."""
    st.markdown(
        """
        <div class="simple-disclaimer">
            <strong>ℹ️ Educational Demonstration:</strong> MediLogic is an academic computer science project demonstrating
            symbolic rule-based AI. It is <strong>not a medical diagnosis</strong>. Please consult a qualified doctor for any actual health concerns.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_emergency_banner(alerts: List[EmergencyAlert]) -> None:
    """Renders prominent emergency alert box if red flags are detected."""
    if not alerts:
        return

    items_html = "".join(
        f"<li><strong>{a.symptom_name}:</strong> {a.action_directive}</li>"
        for a in alerts
    )

    st.markdown(
        f"""
        <div class="simple-emergency-banner">
            <h3>🚨 Immediate Medical Attention Recommended</h3>
            <p style="margin: 0 0 0.4rem 0;">You selected one or more emergency warning signs that require urgent clinical evaluation:</p>
            <ul>{items_html}</ul>
            <div class="callout-tel">
                📞 Call your local emergency number (e.g. 911 / 112 / 999) or visit the nearest emergency room immediately.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_truth_badge_html(val: TruthValue) -> str:
    """Returns HTML badge for fact truth states."""
    if val == TruthValue.TRUE:
        return '<span class="tag-pill tag-pill-active">Yes (Present)</span>'
    elif val == TruthValue.FALSE:
        return '<span class="tag-pill" style="color:#991B1B;">No (Absent)</span>'
    else:
        return '<span class="tag-pill">Not Sure</span>'


def get_goal_status_badge_html(status: GoalStatus) -> str:
    """Returns HTML badge for backward chaining goal statuses."""
    if status == GoalStatus.SUPPORTED:
        return '<span class="result-card .badge-match" style="background:#ECFDF5; color:#065F46; padding:0.2rem 0.5rem; border-radius:6px; font-weight:700;">PROVEN (MATCHED)</span>'
    elif status == GoalStatus.CONTRADICTED_OR_FAILED:
        return '<span style="background:#FEF2F2; color:#991B1B; padding:0.2rem 0.5rem; border-radius:6px; font-weight:700;">NOT SUPPORTED</span>'
    elif status == GoalStatus.UNRESOLVED_UNKNOWN:
        return '<span style="background:#FFFBEB; color:#92400E; padding:0.2rem 0.5rem; border-radius:6px; font-weight:700;">MORE INFO NEEDED</span>'
    else:
        return '<span style="background:#F1F5F9; color:#475569; padding:0.2rem 0.5rem; border-radius:6px; font-weight:700;">CYCLE / LIMIT</span>'


# Presets kept for easy testing and quick demonstration
PRESET_CASES: Dict[str, Dict[str, Any]] = {
    "Flu-like Illness Example": {
        "description": "Fever, cough, body aches, and feeling tired.",
        "facts": {
            "fever_present": TruthValue.TRUE,
            "cough_present": TruthValue.TRUE,
            "fatigue_present": TruthValue.TRUE,
            "body_aches_present": TruthValue.TRUE,
            "rapid_onset_present": TruthValue.TRUE,
            "chest_pain_present": TruthValue.FALSE,
            "severe_shortness_of_breath_present": TruthValue.FALSE,
        },
        "expected_goal": "influenza_like_illness_supported",
    },
    "Common Cold Example": {
        "description": "Stuffy nose, sore throat, sneezing, and mild tiredness.",
        "facts": {
            "nasal_congestion_present": TruthValue.TRUE,
            "sore_throat_present": TruthValue.TRUE,
            "sneezing_present": TruthValue.TRUE,
            "fatigue_present": TruthValue.TRUE,
            "high_fever_present": TruthValue.FALSE,
            "chest_pain_present": TruthValue.FALSE,
        },
        "expected_goal": "common_cold_like_illness_supported",
    },
    "Allergies Example": {
        "description": "Frequent sneezing, clear runny nose, and itchy eyes.",
        "facts": {
            "sneezing_present": TruthValue.TRUE,
            "clear_rhinorrhea_present": TruthValue.TRUE,
            "itchy_eyes_present": TruthValue.TRUE,
            "allergen_exposure_trigger_present": TruthValue.TRUE,
            "fever_present": TruthValue.FALSE,
        },
        "expected_goal": "allergic_rhinitis_pattern_supported",
    },
    "Migraine Headache Example": {
        "description": "Throbbing headache on one side with light sensitivity and nausea.",
        "facts": {
            "headache_present": TruthValue.TRUE,
            "unilateral_throbbing_headache_present": TruthValue.TRUE,
            "photophobia_present": TruthValue.TRUE,
            "nausea_present": TruthValue.TRUE,
            "worsened_by_routine_activity_present": TruthValue.TRUE,
        },
        "expected_goal": "migraine_like_headache_pattern_supported",
    },
    "Stomach Bug Example": {
        "description": "Watery diarrhea, nausea, vomiting, and stomach cramps.",
        "facts": {
            "watery_diarrhea_present": TruthValue.TRUE,
            "nausea_present": TruthValue.TRUE,
            "vomiting_present": TruthValue.TRUE,
            "abdominal_cramps_present": TruthValue.TRUE,
            "severe_unrelenting_abdominal_pain_present": TruthValue.FALSE,
        },
        "expected_goal": "acute_gastroenteritis_pattern_supported",
    },
    "Urinary Discomfort Example": {
        "description": "Pain or burning when urinating, needing to urinate often.",
        "facts": {
            "dysuria_present": TruthValue.TRUE,
            "urinary_frequency_present": TruthValue.TRUE,
            "urinary_urgency_present": TruthValue.TRUE,
            "flank_pain_present": TruthValue.FALSE,
            "fever_present": TruthValue.FALSE,
        },
        "expected_goal": "lower_urinary_tract_infection_pattern_supported",
    },
    "Emergency Warning Example": {
        "description": "Chest pain with severe shortness of breath.",
        "facts": {
            "chest_pain_present": TruthValue.TRUE,
            "severe_shortness_of_breath_present": TruthValue.TRUE,
        },
        "expected_goal": "influenza_like_illness_supported",
    },
}


def initialize_session_state(kb: KnowledgeBase) -> None:
    """Ensures all session state variables exist with proper defaults."""
    if "kb" not in st.session_state:
        st.session_state.kb = kb

    if "user_facts" not in st.session_state:
        st.session_state.user_facts = {sid: TruthValue.UNKNOWN for sid in kb.symptoms.keys()}

    if "forward_result" not in st.session_state:
        st.session_state.forward_result = None

    if "backward_result" not in st.session_state:
        st.session_state.backward_result = None

    if "target_hypothesis" not in st.session_state:
        st.session_state.target_hypothesis = "influenza_like_illness_supported"

    if "current_nav" not in st.session_state:
        st.session_state.current_nav = "Home"


def reset_assessment(kb: KnowledgeBase) -> None:
    """Clears all entered facts and cached results."""
    st.session_state.user_facts = {sid: TruthValue.UNKNOWN for sid in kb.symptoms.keys()}
    st.session_state.forward_result = None
    st.session_state.backward_result = None
