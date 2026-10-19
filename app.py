"""MediLogic: Medical Diagnosis Rule-Based Expert System.

A simplified, beginner-friendly Streamlit user interface demonstrating
Propositional Logic Formalisms, Modus Ponens, Kleene 3-Valued Calculus,
Forward Chaining, and Backward Chaining inference engines.
"""

from __future__ import annotations
from typing import Dict, List, Any
import streamlit as st

from engine.backward_chaining import BackwardChainingEngine, GoalStatus
from engine.explanation import ExplanationEngine
from engine.forward_chaining import ForwardChainingEngine
from engine.knowledge_base import Fact, FactSource, KnowledgeBase, TruthValue
from engine.safety import SafetyEngine
from ui.components import (
    PRESET_CASES,
    SIMPLE_CATEGORY_MAPPING,
    SIMPLE_SYMPTOM_DETAILS,
    get_goal_status_badge_html,
    get_truth_badge_html,
    initialize_session_state,
    render_disclaimer,
    render_emergency_banner,
    render_home_hero,
    reset_assessment,
)
from ui.styles import get_custom_css

# Page Configuration
st.set_page_config(
    page_title="MediLogic - Medical Expert System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Clean Styles
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize Engine Components
@st.cache_resource
def load_system() -> tuple[KnowledgeBase, ForwardChainingEngine, BackwardChainingEngine, ExplanationEngine, SafetyEngine]:
    kb = KnowledgeBase()
    fc = ForwardChainingEngine(kb)
    bc = BackwardChainingEngine(kb)
    expl = ExplanationEngine(kb)
    safety = SafetyEngine(kb)
    return kb, fc, bc, expl, safety

kb, fc_engine, bc_engine, expl_engine, safety_engine = load_system()
initialize_session_state(kb)

# Helper function for safe button-driven page navigation
def navigate_to(page_name: str) -> None:
    """Safely transitions navigation to target page and triggers rerun."""
    st.session_state["_target_nav"] = page_name
    st.session_state.current_nav = page_name
    st.rerun()


# Convert session state user facts to Fact objects
def get_current_fact_store() -> Dict[str, Fact]:
    store: Dict[str, Fact] = {}
    for sid, val in st.session_state.user_facts.items():
        if val != TruthValue.UNKNOWN:
            store[sid] = Fact(id=sid, value=val, source=FactSource.USER)
    return store

# Active Facts & Safety Monitor
active_facts = get_current_fact_store()
safety_report = safety_engine.check_safety(active_facts)

# Sidebar Navigation
st.sidebar.markdown(
    """
    <div style="padding: 0.2rem 0 1rem 0;">
        <h2 style="color: #0F766E; margin: 0; font-size: 1.5rem; font-weight: 800;">🩺 MediLogic</h2>
        <p style="font-size: 0.85rem; color: #64748B; margin: 0;">Educational Rule-Based Medical Checker</p>
    </div>
    """,
    unsafe_allow_html=True,
)

nav_options = [
    "🏠 Home",
    "🩺 Check Symptoms",
    "📋 My Results",
    "💡 Learn How It Works",
    "🔬 AI Lab",
]

# Apply programmatic navigation requests (from buttons) before rendering the radio widget
if "_target_nav" in st.session_state:
    target = st.session_state.pop("_target_nav")
    st.session_state.current_nav = target
    for opt in nav_options:
        if target in opt:
            st.session_state["nav_radio"] = opt
            break

# Ensure nav_radio is initialized to match current_nav
if "nav_radio" not in st.session_state:
    for opt in nav_options:
        if st.session_state.current_nav in opt:
            st.session_state["nav_radio"] = opt
            break

selected_page = st.sidebar.radio(
    "Menu",
    nav_options,
    key="nav_radio",
    label_visibility="collapsed",
)

# Update session state if user clicks directly in sidebar
for opt in nav_options:
    if opt == selected_page:
        clean_name = opt.split(" ", 1)[1]
        st.session_state.current_nav = clean_name

st.sidebar.markdown("---")

# Quick Status in Sidebar
yes_count = sum(1 for v in st.session_state.user_facts.values() if v == TruthValue.TRUE)
no_count = sum(1 for v in st.session_state.user_facts.values() if v == TruthValue.FALSE)

st.sidebar.markdown(f"**Your Selections:**")
st.sidebar.markdown(f"• **Present:** {yes_count} symptom(s)")
st.sidebar.markdown(f"• **Absent:** {no_count} symptom(s)")

if safety_report.has_emergency:
    st.sidebar.markdown(
        """
        <div style="background:#FEF2F2; border:1px solid #FCA5A5; border-radius:8px; padding:0.6rem; margin-top:0.6rem;">
            <strong style="color:#DC2626; font-size:0.85rem;">🚨 Emergency Warning</strong>
            <p style="font-size:0.78rem; color:#991B1B; margin:0.2rem 0 0 0;">An urgent symptom was marked present.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if st.sidebar.button("Start Again (Reset)", use_container_width=True):
    reset_assessment(kb)
    navigate_to("Check Symptoms")

st.sidebar.caption("MediLogic • Educational AI Demonstration")


# ==============================================================================
# 1. HOME PAGE
# ==============================================================================
if st.session_state.current_nav == "Home":
    render_home_hero()
    render_disclaimer()
    if safety_report.has_emergency:
        render_emergency_banner(safety_report.alerts)

    st.markdown("### How It Works in 3 Simple Steps")

    st.markdown(
        """
        <div class="steps-container">
            <div class="step-card">
                <div class="step-num">1</div>
                <h3>Choose your symptoms</h3>
                <p>Select what you are experiencing using simple, plain-English categories like General, Nose, or Stomach.</p>
            </div>
            <div class="step-card">
                <div class="step-num">2</div>
                <h3>Check the available rules</h3>
                <p>The system evaluates transparent IF–THEN medical rules without using any confusing black-box AI.</p>
            </div>
            <div class="step-card">
                <div class="step-num">3</div>
                <h3>Understand the result</h3>
                <p>See which educational health patterns match your answers, and learn exactly why each rule fired.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Prominent Action Buttons
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("👉 Start Symptom Check", type="primary", use_container_width=True):
            navigate_to("Check Symptoms")
    with col_btn2:
        if st.button("💡 Learn How It Works", type="secondary", use_container_width=True):
            navigate_to("Learn How It Works")

    st.markdown("---")

    # Optional Quick Example Selector for Easy Testing
    st.markdown("#### Want to try a quick example?")
    st.write("You can load an example case with one click to see how the system works:")

    ex_cols = st.columns(3)
    preset_names = list(PRESET_CASES.keys())

    for idx, p_name in enumerate(preset_names[:3]):
        with ex_cols[idx]:
            p_info = PRESET_CASES[p_name]
            st.markdown(f"**{p_name}**")
            st.caption(p_info["description"])
            if st.button(f"Load Example #{idx+1}", key=f"home_pre_{idx}", use_container_width=True):
                reset_assessment(kb)
                for f_k, f_v in p_info["facts"].items():
                    st.session_state.user_facts[f_k] = f_v
                # Run forward chaining immediately
                store = get_current_fact_store()
                st.session_state.forward_result = fc_engine.run(store)
                navigate_to("My Results")

    with st.expander("📚 Explore More Clinical Cases (COVID-19, Strep Throat, Sinusitis, GERD, Asthma, etc.)"):
        more_cols = st.columns(2)
        for idx, p_name in enumerate(preset_names[3:]):
            col_target = more_cols[idx % 2]
            with col_target:
                p_info = PRESET_CASES[p_name]
                st.markdown(f"**{p_name}**")
                st.caption(p_info["description"])
                if st.button(f"Load '{p_name}'", key=f"more_pre_{idx}", use_container_width=True):
                    reset_assessment(kb)
                    for f_k, f_v in p_info["facts"].items():
                        st.session_state.user_facts[f_k] = f_v
                    store = get_current_fact_store()
                    st.session_state.forward_result = fc_engine.run(store)
                    navigate_to("My Results")


# ==============================================================================
# 2. CHECK SYMPTOMS PAGE
# ==============================================================================
elif st.session_state.current_nav == "Check Symptoms":
    st.markdown("## 🩺 Check Your Symptoms")
    st.write("Select the symptoms you are experiencing. If you are unsure about any symptom, choose **Not sure**.")
    render_disclaimer()
    if safety_report.has_emergency:
        render_emergency_banner(safety_report.alerts)

    # Search filter
    search_term = st.text_input("🔍 Quick search symptom (e.g., 'fever', 'headache', 'cough'):", "").strip().lower()

    # Iterate through simplified categories
    for cat_name, sym_keys in SIMPLE_CATEGORY_MAPPING.items():
        # Filter if search term given
        matching_keys = []
        for sk in sym_keys:
            info = SIMPLE_SYMPTOM_DETAILS.get(sk, {})
            title = info.get("title", sk).lower()
            desc = info.get("desc", "").lower()
            if not search_term or search_term in title or search_term in desc:
                matching_keys.append(sk)

        if not matching_keys:
            continue

        cat_icon = "🚨" if "Emergency" in cat_name else "📁"
        with st.expander(f"{cat_icon} {cat_name} ({len(matching_keys)})", expanded=True):
            for sk in matching_keys:
                info = SIMPLE_SYMPTOM_DETAILS.get(sk, {
                    "title": kb.symptoms.get(sk, {}).get("name", sk),
                    "desc": kb.symptoms.get(sk, {}).get("description", ""),
                    "icon": "•",
                })
                current_state = st.session_state.user_facts.get(sk, TruthValue.UNKNOWN)

                c_text, c_choice = st.columns([3, 2])
                with c_text:
                    emerg_label = " <span style='color:#DC2626; font-weight:700;'>[Emergency Sign]</span>" if sk in SIMPLE_CATEGORY_MAPPING["Emergency Warning Signs"] else ""
                    st.markdown(f"**{info.get('icon', '•')} {info['title']}**{emerg_label}", unsafe_allow_html=True)
                    st.caption(info["desc"])

                with c_choice:
                    state_idx = 0 if current_state == TruthValue.UNKNOWN else (1 if current_state == TruthValue.TRUE else 2)
                    cur_ver = st.session_state.get("assessment_version", 0)
                    new_val_str = st.radio(
                        f"Choice for {sk}",
                        ["Not sure", "Yes, I have this", "No, I do not"],
                        index=state_idx,
                        key=f"check_sym_{cur_ver}_{sk}",
                        horizontal=True,
                        label_visibility="collapsed",
                    )
                    if new_val_str == "Yes, I have this":
                        st.session_state.user_facts[sk] = TruthValue.TRUE
                    elif new_val_str == "No, I do not":
                        st.session_state.user_facts[sk] = TruthValue.FALSE
                    else:
                        st.session_state.user_facts[sk] = TruthValue.UNKNOWN

    st.markdown("---")

    # Clear Action Buttons
    action_col1, action_col2 = st.columns([2, 1])
    with action_col1:
        if st.button("👉 Check My Answers", type="primary", use_container_width=True):
            # Run inference on current facts
            fact_store = get_current_fact_store()
            st.session_state.forward_result = fc_engine.run(fact_store)
            navigate_to("My Results")

    with action_col2:
        if st.button("Start Again", type="secondary", use_container_width=True):
            reset_assessment(kb)
            st.rerun()


# ==============================================================================
# 3. MY RESULTS PAGE
# ==============================================================================
elif st.session_state.current_nav == "My Results":
    st.markdown("## 📋 Your Assessment Results")
    render_disclaimer()
    if safety_report.has_emergency:
        render_emergency_banner(safety_report.alerts)

    # Ensure inference has been run
    fact_store = get_current_fact_store()
    if st.session_state.forward_result is None:
        st.session_state.forward_result = fc_engine.run(fact_store)

    result = st.session_state.forward_result

    # User-Friendly Summary Message
    if safety_report.has_emergency:
        st.error("⚠️ **Important:** One or more emergency warning signs were noted above. Please seek urgent professional care.")

    if not fact_store:
        st.info("You haven't selected any symptoms yet. Please start by checking your symptoms.")
        if st.button("👉 Select Symptoms Now", type="primary"):
            navigate_to("Check Symptoms")
    else:
        supported_ids = {h["condition_id"] for h in result.supported_hypotheses}
        candidate_hypotheses = expl_engine.find_candidate_and_differential_hypotheses(result.working_memory, supported_ids)

        # 1. Definitively Confirmed Hypotheses (Modus Ponens)
        if result.supported_hypotheses:
            st.markdown(
                """
                <div class="simple-card" style="border-left: 6px solid #0D9488;">
                    <h3 style="color:#0F766E; margin-top:0;">✅ Confirmed Patterns (100% Rule Deduction)</h3>
                    <p style="color:#334155; margin-bottom:0;">
                        Based on verified clinical guidelines, your reported symptoms satisfy all antecedent requirements for the following condition(s):
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            for hypo in result.supported_hypotheses:
                cond_id = hypo["condition_id"]
                cond_name = hypo["condition_name"]
                desc = hypo["description"]
                features = hypo.get("clinical_features", [])
                rule_id = hypo.get("derivation_rule", "")

                st.markdown(
                    f"""
                    <div class="result-card result-card-supported">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                            <h3 style="margin:0;">{cond_name}</h3>
                            <span class="badge-match">Pattern Matched</span>
                        </div>
                        <p style="color:#475569; font-size:0.98rem; margin-bottom:0.8rem;">{desc}</p>
                        <div style="font-size:0.9rem; color:#0F172A; margin-bottom:0.4rem;">
                            <strong>Key Clinical Features:</strong>
                        </div>
                        <ul style="margin-top:0.2rem; color:#334155; font-size:0.9rem;">
                            {"".join(f"<li>{f}</li>" for f in features[:4])}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Plain-Language "Why am I seeing this?"
                with st.expander(f"❓ Why am I seeing '{cond_name}'?"):
                    st.write(
                        f"MediLogic verified the production rules for **{cond_name}**. The symptoms you marked as present satisfied "
                        f"all necessary antecedents defined in authoritative medical practice guidelines."
                    )
                    st.write("**Differential considerations to keep in mind:**")
                    st.write(f"- {', '.join(hypo.get('differential_considerations', [])[:4])}")
                    st.caption(f"Educational reference: {hypo.get('primary_reference', 'Clinical Practice Guideline')}")

                # Expandable Technical Explanation
                with st.expander(f"🔬 How did MediLogic deduce this? (Rule Audit)"):
                    st.markdown(f"**Triggered Production Rule:** `{rule_id}`")
                    rule_obj = kb.rules_by_id.get(rule_id)
                    if rule_obj:
                        st.markdown(f"<div class='tech-box'>{rule_obj.readable_text}</div>", unsafe_allow_html=True)
                        st.markdown(f"**Clinical rationale:** {rule_obj.explanation}")
                    st.write("**Inference engine verification:** Modus Ponens verified that all antecedent conditions evaluated to TRUE in working memory.")

        # 2. Potential Differential Candidates (Near-Matches & Partial Criteria)
        if candidate_hypotheses:
            header_text = "🟡 Other Differential Patterns Under Consideration" if result.supported_hypotheses else "🟡 Potential Health Patterns (Criteria Partially Met)"
            st.markdown(f"### {header_text}")
            st.caption("These conditions share several of your symptoms, but some key criteria are currently unconfirmed or missing:")

            for cand in candidate_hypotheses[:4]:
                c_name = cand["condition_name"]
                c_desc = cand["description"]
                c_score = cand["match_score"]
                matching = cand["matching_symptoms"]
                missing = cand["missing_symptoms"]

                matching_str = ", ".join(matching) if matching else "None"
                missing_str = ", ".join(missing[:3]) if missing else "None"

                st.markdown(
                    f"""
                    <div class="simple-card" style="border-left: 5px solid #F59E0B; margin-bottom: 0.8rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
                            <h4 style="margin:0; color:#0F172A;">{c_name}</h4>
                            <span style="background:#FEF3C7; color:#92400E; padding:0.2rem 0.5rem; border-radius:6px; font-size:0.8rem; font-weight:700;">
                                {c_score}% Diagnostic Alignment
                            </span>
                        </div>
                        <p style="font-size:0.9rem; color:#475569; margin-bottom:0.5rem;">{c_desc}</p>
                        <div style="font-size:0.85rem; color:#1E293B;">
                            <strong>✅ Symptoms you marked present:</strong> {matching_str}
                        </div>
                        <div style="font-size:0.85rem; color:#B45309; margin-top:0.3rem;">
                            <strong>❓ Key symptoms currently 'Not sure' or needed to confirm:</strong> {missing_str}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        elif not result.supported_hypotheses:
            st.markdown(
                """
                <div class="simple-card" style="border-left: 6px solid #64748B;">
                    <h3 style="color:#1E293B; margin-top:0;">No Specific Health Pattern Confirmed</h3>
                    <p style="color:#475569; margin-bottom:0;">
                        The symptoms you entered are either mild, non-specific, or do not form a recognized syndromic cluster in our expert system rules.
                        Try checking additional symptoms or clarifying any symptoms currently marked as "Not sure".
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Bottom Actions
    col_nav1, col_nav2 = st.columns([1, 1])
    with col_nav1:
        if st.button("✏️ Change My Symptoms", use_container_width=True):
            navigate_to("Check Symptoms")
    with col_nav2:
        if st.button("🔬 Explore in AI Lab", use_container_width=True):
            navigate_to("AI Lab")


# ==============================================================================
# 4. LEARN HOW IT WORKS PAGE
# ==============================================================================
elif st.session_state.current_nav == "Learn How It Works":
    st.markdown("## 💡 How MediLogic Works")
    st.write("A simple, non-technical explanation of how rule-based expert systems think.")
    render_disclaimer()

    st.markdown(
        """
        <div class="simple-card">
            <h3>1. What is an Expert System?</h3>
            <p>
                An <strong>expert system</strong> is a computer program that solves problems by applying human-like rules.
                Unlike complex modern neural networks that guess based on patterns in huge datasets, an expert system
                works like a clear, transparent medical guidebook written with <strong>IF–THEN</strong> rules.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="simple-card">
            <h3>2. Two Ways of Thinking</h3>
            <div style="display:flex; gap:1.2rem; flex-wrap:wrap; margin-top:0.8rem;">
                <div style="flex:1; min-width:240px; background:#F8FAFC; border:1px solid #E2E8F0; padding:1.2rem; border-radius:10px;">
                    <h4 style="color:#0F766E; margin-top:0;">⏩ Forward Chaining</h4>
                    <p style="font-size:0.95rem; color:#334155; margin:0;">
                        <strong>"Start with known facts and discover what follows."</strong><br>
                        You enter your symptoms (e.g. fever + cough + body aches). The system scans its rules and derives that this matches a flu-like pattern.
                    </p>
                </div>
                <div style="flex:1; min-width:240px; background:#F8FAFC; border:1px solid #E2E8F0; padding:1.2rem; border-radius:10px;">
                    <h4 style="color:#0F766E; margin-top:0;">⏪ Backward Chaining</h4>
                    <p style="font-size:0.95rem; color:#334155; margin:0;">
                        <strong>"Start with a question and check whether known facts support it."</strong><br>
                        You ask: <em>"Does this look like a migraine?"</em> The system works backward to verify if you have throbbing pain and light sensitivity.
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="simple-card">
            <h3>3. Why "Not sure" Matters (Three-Valued Logic)</h3>
            <p>
                In a regular computer program, anything not marked as "Yes" is often treated as "No".
                In healthcare, this is dangerous: just because a patient hasn't taken their temperature doesn't mean they don't have a fever!
            </p>
            <p style="margin-bottom:0;">
                MediLogic uses <strong>three-valued logic</strong>:
                <br>• <strong>Yes (Present)</strong>
                <br>• <strong>No (Absent)</strong>
                <br>• <strong>Not sure (Unknown)</strong>
                <br>This ensures the system never jumps to conclusions when information is missing.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("👉 Try Checking Symptoms Now", type="primary"):
        navigate_to("Check Symptoms")


# ==============================================================================
# 5. AI LAB (ADVANCED ACADEMIC FEATURES)
# ==============================================================================
elif st.session_state.current_nav == "AI Lab":
    st.markdown("## 🔬 AI Lab (Advanced Academic Features)")
    st.write("Detailed inspection tools for professors, evaluators, and AI students.")
    render_disclaimer()
    if safety_report.has_emergency:
        render_emergency_banner(safety_report.alerts)

    lab_tabs = st.tabs([
        "⏩ Forward Chaining Demo",
        "⏪ Backward Chaining Demo",
        "⚖️ Compare Both Methods",
        "📚 Explore Knowledge Base",
        "🎓 Syllabus & Viva Notes",
    ])

    # 1. Forward Chaining Demo Tab
    with lab_tabs[0]:
        st.markdown("### Forward Chaining Engine")
        st.caption("Data-Driven Modus Ponens: Starts from active facts in working memory and fires rules in rounds.")

        if st.button("⚡ Run Forward Chaining", type="primary"):
            store = get_current_fact_store()
            st.session_state.forward_result = fc_engine.run(store)

        store = get_current_fact_store()
        fc_res = fc_engine.run(store)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Initial Facts", len(fc_res.initial_facts))
        c2.metric("Derived Facts", len(fc_res.derived_facts))
        c3.metric("Rules Fired", len(fc_res.fired_rules))
        c4.metric("Iterations", fc_res.iterations_run)

        st.info(f"Termination: {fc_res.termination_reason}")

        st.markdown("#### Fired Rules & Step Trace:")
        for step in fc_res.trace:
            if step.fired:
                st.markdown(
                    f"- **Step {step.step_number} [Iteration {step.iteration}]:** Rule `{step.rule_id}` fired &rarr; Added `{step.consequent_fact}`."
                )

        with st.expander("Inspect All Rule Evaluations (Complete Audit)"):
            all_trace_data = []
            for s in fc_res.trace:
                all_trace_data.append({
                    "Step": s.step_number,
                    "Rule": s.rule_id,
                    "Fired": "Yes" if s.fired else "No",
                    "Evaluation": s.evaluation_value.value,
                    "Explanation": s.explanation,
                })
            st.dataframe(all_trace_data, use_container_width=True)

    # 2. Backward Chaining Demo Tab
    with lab_tabs[1]:
        st.markdown("### Backward Chaining Engine")
        st.caption("Goal-Directed Recursive Proof: Starts from a target hypothesis and checks subgoals depth-first.")

        target_options = list(kb.conditions.keys())
        selected_goal = st.selectbox(
            "Select Hypothesis to Prove:",
            target_options,
            format_func=lambda x: f"{kb.conditions[x]['name']} ({x})",
            key="ai_lab_target_goal",
        )

        store = get_current_fact_store()
        bc_res = bc_engine.run(selected_goal, store)

        badge = get_goal_status_badge_html(bc_res.status)
        st.markdown(f"**Proof Outcome:** {badge}", unsafe_allow_html=True)
        st.write(bc_res.explanation_summary)

        if bc_res.missing_prerequisites:
            st.warning(f"Missing prerequisites to confirm this goal: {', '.join(bc_res.missing_prerequisites)}")

        st.markdown("#### Goal Proof Tree:")
        tree_items = expl_engine.format_backward_proof_tree(bc_res.proof_tree)
        tree_text = "\n".join([item["text"] for item in tree_items])
        st.markdown(f"<div class='tech-box'>{tree_text}</div>", unsafe_allow_html=True)

    # 3. Compare Both Methods Tab
    with lab_tabs[2]:
        st.markdown("### Side-by-Side Algorithm Comparison")
        st.caption("Compare how Forward Chaining and Backward Chaining process the exact same facts.")

        store = get_current_fact_store()
        fc_res = fc_engine.run(store)
        bc_res = bc_engine.run(selected_goal, store)
        comp = expl_engine.compare_engines(fc_res, bc_res)

        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown(
                f"""
                <div class="simple-card">
                    <h4>Forward Chaining</h4>
                    <p><strong>Direction:</strong> Data-driven (Bottom-Up)</p>
                    <p><strong>Supported:</strong> {len(comp['forward_supported_all'])} hypotheses</p>
                    <p><strong>Rules Fired:</strong> {len(comp['forward_rules_fired'])}</p>
                    <p><strong>Total Steps:</strong> {comp['forward_steps_count']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_right:
            st.markdown(
                f"""
                <div class="simple-card">
                    <h4>Backward Chaining</h4>
                    <p><strong>Direction:</strong> Goal-directed (Top-Down)</p>
                    <p><strong>Target Goal:</strong> {selected_goal}</p>
                    <p><strong>Status:</strong> {bc_res.status.value}</p>
                    <p><strong>Steps Explored:</strong> {comp['backward_steps_count']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(f"> **Engine Agreement:** Both algorithms agree on target `{selected_goal}`: **{comp['agreement']}**.")

    # 4. Explore Knowledge Base Tab
    with lab_tabs[3]:
        st.markdown("### Knowledge Base Explorer")
        st.caption("Browse all 21 production rules, 34 symptoms, 8 condition hypotheses, and 7 citations.")

        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["Production Rules", "Symptoms", "Medical References"])
        with sub_tab1:
            for r in kb.rules:
                with st.expander(f"{r.id}: {r.name}"):
                    st.markdown(f"<div class='tech-box'>{r.readable_text}</div>", unsafe_allow_html=True)
                    st.write(f"**Explanation:** {r.explanation}")
                    st.write(f"**Source Citation:** `{r.source}`")
        with sub_tab2:
            s_data = [{"ID": s["id"], "Name": s["name"], "Category": s["category"], "Emergency": s["is_emergency"]} for s in kb.symptoms.values()]
            st.dataframe(s_data, use_container_width=True)
        with sub_tab3:
            for rid, ref in kb.references.items():
                st.markdown(f"**{ref['title']} ({ref['year']})** — _{ref['organization']}_")
                st.caption(ref["description"])

    # 5. Syllabus & Viva Notes Tab
    with lab_tabs[4]:
        st.markdown("### Academic Syllabus Alignment (Unit IV)")
        st.markdown(
            """
            - **Propositional Logic & WFFs:** Implemented via validated expression trees (`engine/rule_evaluator.py`).
            - **Modus Ponens:** Implemented as rule detachment in `engine/forward_chaining.py`.
            - **Kleene 3-Valued Logic:** Preserves explicit `TRUE`, `FALSE`, and `UNKNOWN` states.
            - **Cycle Detection:** Implemented via active call-stack guard in `engine/backward_chaining.py`.
            - **MYCIN Architectural Principles:** Separation of declarative knowledge base from inference engine; transparent explanation trace.
            """
        )
        st.info("For full academic documentation and all 40 viva questions, see `docs/VIVA_QUESTIONS.md`.")
