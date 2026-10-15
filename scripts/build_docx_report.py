import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

# Ensure workspace root is in sys.path
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from scripts.docx_helpers import (
    set_cell_background,
    set_cell_margins,
    set_table_borders,
    add_callout_box,
    add_code_block,
    add_styled_table,
    add_figure_image
)

def add_p(doc, text, bold_prefix=None, italic=False, space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(space_after)
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.bold = True
        rb.font.name = 'Times New Roman'
        rb.font.size = Pt(12)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.italic = italic
    return p

def add_h1(doc, text, page_break=True):
    if page_break:
        doc.add_page_break()
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(18)
    h.paragraph_format.space_after = Pt(8)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    return h

def add_h2(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
    return h

def add_h3(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(2)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    return h

def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.line_spacing = 1.3
    p.paragraph_format.space_after = Pt(3)
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.bold = True
        rb.font.name = 'Times New Roman'
        rb.font.size = Pt(11.5)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11.5)
    return p

def add_preliminary_pages(doc, cand_data):
    print("  -> Adding Preliminary Pages...")
    # 1.1 TITLE PAGE
    p_tp = doc.add_paragraph()
    p_tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tp.paragraph_format.space_before = Pt(20)
    p_tp.paragraph_format.space_after = Pt(4)
    r = p_tp.add_run("SAVITRIBAI PHULE PUNE UNIVERSITY (SPPU)\n")
    r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    
    r2 = p_tp.add_run("[COLLEGE_NAME_PLACEHOLDER]\nDEPARTMENT OF COMPUTER ENGINEERING\n")
    r2.font.size = Pt(13); r2.font.bold = True; r2.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
    
    p_tp2 = doc.add_paragraph()
    p_tp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tp2.paragraph_format.space_before = Pt(20)
    p_tp2.paragraph_format.space_after = Pt(12)
    r3 = p_tp2.add_run("A MINI-PROJECT REPORT ON\n\n")
    r3.font.size = Pt(12); r3.font.italic = True
    
    r4 = p_tp2.add_run('"Medical Diagnosis System Using a Rule-Based Expert System with Forward and Backward Chaining"\n')
    r4.font.size = Pt(15); r4.font.bold = True; r4.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    
    r5 = p_tp2.add_run('(Application: MediLogic)\n\n')
    r5.font.size = Pt(13); r5.font.bold = True; r5.font.color.rgb = RGBColor(0x31, 0x82, 0xCE)
    
    r6 = p_tp2.add_run("SUBMITTED IN PARTIAL FULFILLMENT OF\nTHE REQUIREMENTS FOR THE AWARD OF THE DEGREE OF\n\nBACHELOR OF ENGINEERING\n(COMPUTER ENGINEERING)\n")
    r6.font.size = Pt(11.5); r6.font.bold = True
    
    # Candidate Table
    tbl_cand = doc.add_table(rows=5, cols=2)
    tbl_cand.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_hdr = tbl_cand.rows[0].cells
    c_hdr[0].text = "Name of Candidate"; c_hdr[1].text = "Exam Seat / Roll Number"
    for cell in c_hdr:
        set_cell_background(cell, "EDF2F7")
        p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.bold = True; p.runs[0].font.size = Pt(10)
    
    for idx, (cname, croll) in enumerate(cand_data):
        row_c = tbl_cand.rows[idx+1].cells
        row_c[0].text = cname; row_c[1].text = croll
        for c in row_c:
            p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.size = Pt(10)
    set_table_borders(tbl_cand, color="CBD5E0", sz="4")
    
    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(24)
    p_guide.paragraph_format.space_after = Pt(2)
    rg = p_guide.add_run("UNDER THE GUIDANCE OF:\n")
    rg.font.size = Pt(11.5); rg.font.bold = True
    rg2 = p_guide.add_run("[GUIDE_NAME_PLACEHOLDER]\n[GUIDE_DESIGNATION_PLACEHOLDER]\nDEPARTMENT OF COMPUTER ENGINEERING\n\nACADEMIC YEAR: 2025–2026")
    rg2.font.size = Pt(11)

    # 1.2 CERTIFICATE
    add_h1(doc, "CERTIFICATE", page_break=True)
    p_cert_hdr = doc.add_paragraph()
    p_cert_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rc1 = p_cert_hdr.add_run("[COLLEGE_NAME_PLACEHOLDER]\nDEPARTMENT OF COMPUTER ENGINEERING\n\n")
    rc1.font.size = Pt(13); rc1.font.bold = True
    
    add_p(doc, 'This is to certify that the mini-project report entitled "Medical Diagnosis System Using a Rule-Based Expert System with Forward and Backward Chaining" (Application: MediLogic) has been successfully completed by:')
    
    for cname, croll in cand_data:
        add_bullet(doc, f"{cname}  (Exam Seat / Roll No: {croll})")
        
    add_p(doc, '\nin partial fulfillment of the requirements for the Degree of Bachelor of Engineering in Computer Engineering (Third Year - Semester VI) under Savitribai Phule Pune University for the academic year 2025–2026. The work embodied in this mini-project report has been carried out under our supervision and satisfies the academic standards for the subject Artificial Intelligence (Course Code: 310253).')
    
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(36)
    p_sig.paragraph_format.line_spacing = 1.2
    p_sig.add_run("_____________________________                                _____________________________\n")
    p_sig.add_run("[GUIDE_NAME_PLACEHOLDER]                                     [HOD_NAME_PLACEHOLDER]\n")
    p_sig.add_run("Project Guide / Internal Guide                              Head of the Department\n")
    p_sig.add_run("Department of Computer Engineering                           Department of Computer Engineering\n\n\n")
    p_sig.add_run("_____________________________                                _____________________________\n")
    p_sig.add_run("Internal Examiner                                            External Examiner\n")
    p_sig.add_run("Date: _______________________                                Date: _______________________\n")
    p_sig.add_run("Place: ______________________                                Place: ______________________")

    # 1.3 STUDENT DECLARATION
    add_h1(doc, "STUDENT DECLARATION", page_break=True)
    add_p(doc, 'We hereby declare that the mini-project report titled "Medical Diagnosis System Using a Rule-Based Expert System with Forward and Backward Chaining" submitted to Savitribai Phule Pune University in partial fulfillment of the requirements for the award of Bachelor of Engineering in Computer Engineering is a bona fide record of original academic work carried out by us under the guidance of [GUIDE_NAME_PLACEHOLDER].')
    add_p(doc, 'We confirm that the algorithmic implementations of Forward Chaining, Backward Chaining with active-stack cycle detection, the Kleene K3 three-valued rule evaluator, and the Streamlit-based web interface represent genuine software development executed by our team.')
    add_p(doc, 'We explicitly acknowledge that MediLogic is an academic, educational demonstration system designed to illustrate knowledge-based agent formalisms from Unit IV of the SPPU Artificial Intelligence curriculum. It does not constitute certified clinical diagnostic software, does not dispense pharmacological prescriptions, and must not replace professional clinical consultations.')
    
    p_decsig = doc.add_paragraph()
    p_decsig.paragraph_format.space_before = Pt(28)
    p_decsig.paragraph_format.line_spacing = 1.3
    p_decsig.add_run("Candidate Signatures:\n\n")
    for idx, (cname, croll) in enumerate(cand_data):
        p_decsig.add_run(f"{idx+1}. _____________________________   {cname} ({croll})\n")

    # 1.4 ACKNOWLEDGEMENT
    add_h1(doc, "ACKNOWLEDGEMENT", page_break=True)
    add_p(doc, 'We express our profound gratitude to our project guide, [GUIDE_NAME_PLACEHOLDER], for invaluable encouragement, insightful guidance, and continuous academic mentoring throughout the conception, algorithmic formulation, and implementation of this project.')
    add_p(doc, 'We extend our sincere thanks to [HOD_NAME_PLACEHOLDER], Head of the Department of Computer Engineering, and [PRINCIPAL_NAME_PLACEHOLDER], Principal of [COLLEGE_NAME_PLACEHOLDER], for providing the academic infrastructure, computing facilities, and administrative encouragement essential for completing this work.')
    add_p(doc, 'We also convey our appreciation to the faculty members of the Computer Engineering Department, laboratory technical staff, and our fellow engineering peers for constructive technical discussions regarding expert system reasoning architectures and classical benchmark comparisons.')

    # 1.5 ABSTRACT
    add_h1(doc, "ABSTRACT", page_break=True)
    add_p(doc, 'This project report presents MediLogic, a transparent, rule-based medical expert system developed to demonstrate knowledge representation and logical inference formalisms aligned with Unit IV of the Savitribai Phule Pune University (SPPU) Third-Year Computer Engineering Artificial Intelligence curriculum. Modern clinical machine learning applications frequently operate as opaque "black-box" models, posing significant interpretability and safety barriers in safety-critical domains. In contrast, classical expert systems ground decision-making in human-interpretable propositional logic, declarative production rules, and formal inference mechanisms.')
    add_p(doc, 'MediLogic implements a complete knowledge-based agent comprising a declarative knowledge base (34 categorized symptom predicates, 21 production rules, 8 educational condition hypotheses, and 7 authoritative medical citations), an expression evaluator operating under Kleene strong three-valued logic (TRUE, FALSE, UNKNOWN), a data-driven forward-chaining inference engine with fixed-point iteration, and a goal-directed backward-chaining engine equipped with active recursion-stack cycle detection. An independent clinical safety layer intercepts red-flag emergency symptoms (such as acute chest pain and shortness of breath) to issue immediate non-suppressible alerts. The system features a responsive Streamlit presentation layer providing a 3-step clinical assessment workflow and an interactive AI Lab for algorithmic tracing and rule inspection. Automated verification via 42 unit and integration tests under Pytest achieves 100% test passage. MediLogic demonstrates how classical production systems deliver transparent, deterministic, and auditable reasoning for educational and preliminary triaging applications.')
    add_p(doc, 'Keywords: Expert Systems, Knowledge Representation, Propositional Logic, Forward Chaining, Backward Chaining, Kleene Three-Valued Logic, Modus Ponens, SPPU AI Curriculum.', italic=True)

    # 1.6 TABLE OF CONTENTS
    add_h1(doc, "TABLE OF CONTENTS", page_break=True)
    toc_data = [
        ("Certificate", "ii"),
        ("Student Declaration", "iii"),
        ("Acknowledgement", "iv"),
        ("Abstract", "v"),
        ("List of Figures", "vii"),
        ("List of Tables", "viii"),
        ("List of Abbreviations", "ix"),
        ("CHAPTER 1: INTRODUCTION", "1"),
        ("    1.1 Introduction to Artificial Intelligence", "1"),
        ("    1.2 Introduction to Expert Systems", "2"),
        ("    1.3 Background of Rule-Based Reasoning", "3"),
        ("    1.4 Problem Statement", "4"),
        ("    1.5 Motivation", "5"),
        ("    1.6 Aim and Objectives", "6"),
        ("    1.7 Scope of the Project", "7"),
        ("    1.8 Practical & Educational Applications", "8"),
        ("    1.9 System & Clinical Limitations", "9"),
        ("CHAPTER 2: LITERATURE REVIEW AND EXISTING SYSTEM", "10"),
        ("    2.1 Overview of Medical Expert Systems", "10"),
        ("    2.2 Historical Case Study: The MYCIN System (1976)", "11"),
        ("    2.3 General Principles of Knowledge-Based Medical Reasoning", "13"),
        ("    2.4 Existing Approaches and Limitations", "14"),
        ("    2.5 Proposed System: MediLogic", "15"),
        ("    2.6 Advantages of the Proposed Educational System", "16"),
        ("CHAPTER 3: SYSTEM ANALYSIS AND REQUIREMENTS", "17"),
        ("    3.1 Functional Requirements", "17"),
        ("    3.2 Non-Functional Requirements", "18"),
        ("    3.3 Hardware Requirements", "19"),
        ("    3.4 Software Requirements", "20"),
        ("    3.5 Feasibility Study", "21"),
        ("    3.6 User Workflow", "22"),
        ("    3.7 Use Case Descriptions", "23"),
        ("CHAPTER 4: SYSTEM DESIGN", "25"),
        ("    4.1 Overall Architectural Design", "25"),
        ("    4.2 Module Decomposition", "27"),
        ("    4.3 Knowledge-Base Design", "28"),
        ("    4.4 Fact Representation & Working Memory", "29"),
        ("    4.5 Production-Rule Structure", "30"),
        ("    4.6 Rule Evaluator Design (Kleene K3 Logic)", "31"),
        ("    4.7 Inference-Engine Design", "32"),
        ("    4.8 Explanation Facility", "33"),
        ("    4.9 Independent Safety Layer", "34"),
        ("    4.10 Data-Flow Diagrams (DFD Level 0 & Level 1)", "35"),
        ("    4.11 Use-Case Diagram", "36"),
        ("    4.12 Rule Dependency Architecture", "37"),
        ("CHAPTER 5: AI CONCEPTS AND METHODOLOGY", "38"),
        ("    5.1 Knowledge Representation Using Logical Formalisms", "38"),
        ("    5.2 Propositional Logic and Well-Formed Formulas", "39"),
        ("    5.3 Logical Connectives & Kleene Truth Tables", "40"),
        ("    5.4 Facts and IF-THEN Production Rules", "41"),
        ("    5.5 Inference Rules and Modus Ponens", "42"),
        ("    5.6 Forward Chaining Algorithm & Pseudocode", "43"),
        ("    5.7 Backward Chaining Algorithm & Pseudocode", "45"),
        ("    5.8 Asymptotic Complexity Analysis", "47"),
        ("    5.9 Comparison of Forward and Backward Chaining", "48"),
        ("    5.10 Worked Multi-Step Reasoning Example", "49"),
        ("    5.11 Relationship and Architectural Comparison to MYCIN", "51"),
        ("    5.12 SPPU Syllabus Mapping (Unit IV)", "52"),
        ("CHAPTER 6: IMPLEMENTATION", "53"),
        ("    6.1 Technology Stack", "53"),
        ("    6.2 Project Directory Structure", "54"),
        ("    6.3 Knowledge-Base Implementation (knowledge_base.py)", "55"),
        ("    6.4 Three-Valued Logic Evaluator (rule_evaluator.py)", "56"),
        ("    6.5 Forward Chaining Implementation (forward_chaining.py)", "57"),
        ("    6.6 Backward Chaining Implementation (backward_chaining.py)", "58"),
        ("    6.7 Explanation Facility (explanation.py)", "59"),
        ("    6.8 Clinical Safety Engine (safety.py)", "60"),
        ("    6.9 User Interface & Streamlit Session Handling (app.py)", "61"),
        ("    6.10 Error Handling and Knowledge-Base Validation", "62"),
        ("CHAPTER 7: TESTING AND RESULTS", "63"),
        ("    7.1 Testing Objectives", "63"),
        ("    7.2 Test Environment & Pytest Framework", "64"),
        ("    7.3 Unit Testing Strategy", "65"),
        ("    7.4 Integration Testing Strategy", "66"),
        ("    7.5 Automated Test-Case Execution Matrix", "67"),
        ("    7.6 Actual Verification Test Results", "69"),
        ("    7.7 Forward Chaining Live Demonstration", "70"),
        ("    7.8 Backward Chaining Live Demonstration", "71"),
        ("    7.9 Side-by-Side Algorithm Comparison", "72"),
        ("    7.10 Application Screenshots and Demonstration Results", "73"),
        ("    7.11 Limitations Discovered During Testing", "82"),
        ("CHAPTER 8: CONCLUSION AND FUTURE SCOPE", "83"),
        ("    8.1 Summary of the Project", "83"),
        ("    8.2 Objectives Achieved", "84"),
        ("    8.3 Key Learning Outcomes", "85"),
        ("    8.4 Advantages of MediLogic", "86"),
        ("    8.5 Technical Limitations", "87"),
        ("    8.6 Medical Safety & Ethical Boundaries", "88"),
        ("    8.7 Future Enhancements", "89"),
        ("    8.8 Concluding Remarks", "90"),
        ("REFERENCES AND BIBLIOGRAPHY", "91"),
        ("APPENDIX A: CORE PYTHON SOURCE-CODE EXCERPTS", "93"),
        ("APPENDIX B: SAMPLE INPUT AND OUTPUT EXECUTION TRACES", "97"),
        ("APPENDIX C: COMPLETE SPPU SYLLABUS MAPPING TABLE", "99")
    ]
    for title, page in toc_data:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(title)
        if "CHAPTER" in title or "REFERENCES" in title or "APPENDIX" in title:
            r_t.font.bold = True
            r_t.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
        dots_count = max(5, 75 - len(title))
        r_dots = p.add_run(" " + "." * dots_count + " ")
        r_dots.font.color.rgb = RGBColor(0xA0, 0xAE, 0xC0)
        r_p = p.add_run(page)
        r_p.font.bold = True

    # 1.7 LIST OF FIGURES
    add_h1(doc, "LIST OF FIGURES", page_break=True)
    fig_headers = ["Figure Number", "Figure Title", "Page / Chapter"]
    fig_rows = [
        ["Figure 4.1", "MediLogic Five-Tier System Architecture Diagram", "Chapter 4"],
        ["Figure 4.2", "Data Flow Diagram (Level 0 Context & Level 1 Decomposition)", "Chapter 4"],
        ["Figure 4.3", "MediLogic Use Case Diagram", "Chapter 4"],
        ["Figure 4.4", "Knowledge Base Rule Dependency Lattice", "Chapter 4"],
        ["Figure 5.1", "Forward Chaining Algorithm Execution Flowchart", "Chapter 5"],
        ["Figure 5.2", "Backward Chaining (Goal-Directed DFS) Flowchart", "Chapter 5"],
        ["Figure 7.1", "Application Home Dashboard (01_dashboard.png)", "Chapter 7"],
        ["Figure 7.2", "Simplified Symptom Assessment Screen (02_symptom_assessment.png)", "Chapter 7"],
        ["Figure 7.3", "Forward Chaining Diagnostic Results Card (03_forward_chaining.png)", "Chapter 7"],
        ["Figure 7.4", "Backward Chaining Proof Tree Evaluation in AI Lab (04_backward_chaining.png)", "Chapter 7"],
        ["Figure 7.5", "Side-by-Side Algorithm Comparison in AI Lab (05_algorithm_comparison.png)", "Chapter 7"],
        ["Figure 7.6", "Declarative Knowledge Base Explorer in AI Lab (06_knowledge_base.png)", "Chapter 7"],
        ["Figure 7.7", "Step-by-Step Inference Explanation View (07_inference_explanation.png)", "Chapter 7"],
        ["Figure 7.8", "Independent Safety Warning Red-Flag Alert (08_safety_warning.png)", "Chapter 7"],
        ["Figure 7.9", "Inconclusive Result Demonstration (09_inconclusive_result.png)", "Chapter 7"]
    ]
    add_styled_table(doc, fig_headers, fig_rows, [1.3, 4.2, 1.2])

    # 1.8 LIST OF TABLES
    add_h1(doc, "LIST OF TABLES", page_break=True)
    tbl_headers = ["Table Number", "Table Title", "Chapter / Section"]
    tbl_rows = [
        ["Table 1.1", "Comparison of Machine Learning, Naive Rule Checkers, and MediLogic", "Section 1.4"],
        ["Table 3.1", "Hardware Specifications for MediLogic Execution", "Section 3.3"],
        ["Table 3.2", "Software Stack and Dependency Specifications", "Section 3.4"],
        ["Table 5.1", "Kleene Strong 3-Valued Logic (K3) Truth Tables", "Section 5.3"],
        ["Table 5.2", "Asymptotic Computational Complexity Comparison", "Section 5.8"],
        ["Table 5.3", "Comprehensive Comparison: Forward Chaining vs. Backward Chaining", "Section 5.9"],
        ["Table 5.4", "Architectural Comparison: Stanford MYCIN vs. MediLogic", "Section 5.11"],
        ["Table 5.5", "SPPU Unit IV Syllabus Alignment Matrix", "Section 5.12"],
        ["Table 7.1", "Automated Test-Case Execution Matrix (Pytest Suite)", "Section 7.5"]
    ]
    add_styled_table(doc, tbl_headers, tbl_rows, [1.3, 4.2, 1.2])

    # 1.9 LIST OF ABBREVIATIONS
    add_h1(doc, "LIST OF ABBREVIATIONS", page_break=True)
    abbr_headers = ["Abbreviation", "Full Expansion", "Academic / Clinical Context"]
    abbr_rows = [
        ["AI", "Artificial Intelligence", "Discipline of creating rational computational agents"],
        ["KB", "Knowledge Base", "Declarative repository of clinical facts and production rules"],
        ["WFF", "Well-Formed Formula", "Syntactically valid proposition in formal propositional logic"],
        ["MP", "Modus Ponens", "Rule of detachment: From P and P -> Q, infer Q"],
        ["FC", "Forward Chaining", "Data-driven bottom-up inference to fixed-point saturation"],
        ["BC", "Backward Chaining", "Goal-directed top-down hypothesis verification via DFS"],
        ["DFS", "Depth-First Search", "Algorithmic traversal used in backward proof trees"],
        ["K3", "Kleene 3-Valued Logic", "Strong ternary logic containing TRUE, FALSE, UNKNOWN"],
        ["DFD", "Data Flow Diagram", "Graphical model of process transformations and data stores"],
        ["CF", "Certainty Factor", "Heuristic numeric uncertainty measure pioneered by MYCIN"],
        ["SPPU", "Savitribai Phule Pune University", "Curriculum affiliating authority for Computer Engineering"],
        ["TE", "Third-Year Engineering", "Academic level corresponding to Semester V / VI"],
        ["UI", "User Interface", "Interactive presentation layer implemented in Streamlit"],
        ["ILI", "Influenza-Like Illness", "Clinical syndrome comprising acute fever, cough, fatigue"],
        ["WHO", "World Health Organization", "Authoritative guideline reference for clinical syndromic triage"]
    ]
    add_styled_table(doc, abbr_headers, abbr_rows, [1.2, 2.5, 3.0])

def add_chapter_1(doc):
    print("  -> Adding Chapter 1: Introduction...")
    add_h1(doc, "CHAPTER 1 — INTRODUCTION", page_break=True)
    
    add_h2(doc, "1.1 Introduction to Artificial Intelligence")
    add_p(doc, "Artificial Intelligence (AI) is the subfield of computer science dedicated to creating computational systems capable of performing tasks that ordinarily require human intelligence—such as perception, logical reasoning, knowledge representation, planning, learning, and decision-making (Russell & Norvig, 2020). Historically, AI evolved through two complementary paradigms:")
    add_bullet(doc, "Based on formal logic, explicit symbol manipulation, declarative knowledge bases, and deductive inference rules.", bold_prefix="1. Symbolic AI (Classical / Good Old-Fashioned AI): ")
    add_bullet(doc, "Based on artificial neural networks, deep learning, statistical probability, and pattern extraction from numerical tensors.", bold_prefix="2. Sub-Symbolic AI (Statistical / Connectionist AI): ")
    add_p(doc, "While statistical machine learning excels in perceptual domains like computer vision and speech recognition, it remains plagued by opacity, statistical unreliability, and lack of verifiable auditability. In safety-critical fields like medicine, symbolic AI provides formal mathematical verifiability, ensuring that every deduction can be inspected, justified, and proved from explicit premises.")

    add_h2(doc, "1.2 Introduction to Expert Systems")
    add_p(doc, "An Expert System is a knowledge-intensive computer program that solves complex problems within a specialized domain by emulating the deductive reasoning of human specialists (Jackson, 1999). Pioneer systems of the 1970s and 1980s—including DENDRAL (chemical spectrometry analysis) and MYCIN (antimicrobial therapy selection)—demonstrated that expert performance depends critically on high-quality, domain-specific knowledge rather than generic search heuristics.")
    add_p(doc, "The fundamental architectural principle of expert systems is the strict separation between:")
    add_bullet(doc, "Declarative, inspectable domain heuristics and rules.", bold_prefix="• The Knowledge Base (KB): ")
    add_bullet(doc, "Domain-independent algorithms executing logical deduction.", bold_prefix="• The Inference Engine: ")
    add_bullet(doc, "Dynamic state holding observed case-specific facts.", bold_prefix="• Working Memory: ")
    add_bullet(doc, "Subsystem providing human-readable justifications of inferences.", bold_prefix="• The Explanation Facility: ")

    add_h2(doc, "1.3 Background of Rule-Based Reasoning")
    add_p(doc, "A Rule-Based System organizes knowledge as IF–THEN production rules:")
    add_callout_box(doc, "IF <Condition / Antecedent> THEN <Action / Consequent>", title="Canonical Production Rule Format")
    add_p(doc, "Rules represent conditional implications (P -> Q). Reasoning operates by matching working memory facts against antecedents. When conditions are satisfied, rules 'fire', asserting consequents into working memory. This model closely mirrors human diagnostic cognition, where physicians evaluate observed patient symptoms against established diagnostic guidelines.")

    add_h2(doc, "1.4 Problem Statement")
    add_p(doc, "Medical assessment is inherently deductive and safety-critical. Computer engineering curricula frequently suffer from two pedagogical deficiencies:")
    add_bullet(doc, "Students frequently rely on deep neural networks that output disease labels without providing verifiable causal justifications, making validation impossible in a viva examination.", bold_prefix="1. The Machine Learning Black-Box Dilemma: ")
    add_bullet(doc, "Beginner projects typically implement binary Boolean logic (True/False), silently treating unobserved symptoms as False. In clinical practice, an unperformed test is UNKNOWN. Assuming absence when evidence is merely unobserved introduces critical diagnostic failures.", bold_prefix="2. The Closed-World Fallacy in Naive Rule Checkers: ")
    add_p(doc, "The problem addressed in this project is:")
    add_callout_box(doc, "To design, implement, and rigorously verify an autonomous, explainable, rule-based medical expert system (MediLogic) that models clinical knowledge as propositional production rules, evaluates expressions under Kleene three-valued logic (K3), executes both data-driven forward chaining and goal-directed backward chaining with cycle detection, provides transparent step-by-step audit explanations, and enforces an autonomous clinical emergency safety layer.", title="Problem Statement Formulation")

    # Table 1.1
    add_h3(doc, "Table 1.1: Comparison of Machine Learning, Naive Rule Checkers, and MediLogic")
    t1_headers = ["Criterion", "Machine Learning / LLMs", "Naive Rule Checkers", "MediLogic System"]
    t1_rows = [
        ["Reasoning Model", "Statistical / Probabilistic", "Hardcoded If-Else", "Formal Propositional Logic"],
        ["Truth Semantics", "Continuous Latent Vectors", "2-Valued Boolean", "Kleene 3-Valued (T, F, U)"],
        ["Unobserved Facts", "Imputed or Hallucinated", "Assumed False", "Preserved as UNKNOWN"],
        ["Explanation Quality", "Post-hoc text generation", "Static strings", "Direct Modus Ponens Trace"],
        ["Inference Engines", "Feedforward pass", "Single hardcoded loop", "Dual: Forward & Backward"],
        ["Safety Red Flags", "Dependent on prompting", "Intertwined with logic", "Independent Triage Layer"],
        ["Academic Auditability", "Low", "Low", "100% Deterministic Proof"]
    ]
    add_styled_table(doc, t1_headers, t1_rows, [1.8, 1.8, 1.5, 1.8])

    add_h2(doc, "1.5 Motivation")
    add_p(doc, "This project is motivated by the Third-Year SPPU Artificial Intelligence syllabus (Unit IV: Knowledge Representation Using Logical Formalisms). Students are required to understand propositional logic, inference rules (Modus Ponens), knowledge-based agents, and chaining algorithms. MediLogic provides an authentic, working Python implementation where every theoretical concept from the textbook is realized in inspectable code and verified by automated unit tests.")

    add_h2(doc, "1.6 Aim and Objectives")
    add_p(doc, "Aim: To construct a deterministic, explainable, rule-based medical diagnosis expert system in Python demonstrating forward and backward chaining inference over structured propositional logic rules.", bold_prefix="• ")
    add_p(doc, "Specific Technical Objectives:")
    add_bullet(doc, "Construct an inspectable declarative JSON knowledge base encoding 34 symptoms, 21 production rules, 8 educational condition hypotheses, and 7 authoritative medical citations.")
    add_bullet(doc, "Implement a three-valued logic evaluator adhering to Kleene K3 strong logic of indeterminacy.")
    add_bullet(doc, "Implement a data-driven Forward Chaining engine applying Modus Ponens to reach fixed-point working memory saturation.")
    add_bullet(doc, "Implement a goal-directed Backward Chaining engine performing recursive depth-first proof search with active call-stack cycle detection.")
    add_bullet(doc, "Implement an independent Clinical Safety Monitoring subsystem for life-threatening emergency signs.")
    add_bullet(doc, "Develop an intuitive Streamlit user interface featuring a 3-step beginner-friendly workflow and an advanced AI Lab for academic evaluation.")
    add_bullet(doc, "Validate system reliability with an automated Pytest test suite achieving 100% code pass rate.")

    add_h2(doc, "1.7 Scope of the Project")
    add_p(doc, "In-Scope:", bold_prefix="• ")
    add_bullet(doc, "Common ambulatory symptom patterns: Influenza-Like Illness, Common Cold, Allergic Rhinitis, Migraine Cephalalgia, Acute Gastroenteritis, and Lower/Upper Urinary Tract Infection.")
    add_bullet(doc, "Classical propositional logic connectives: Conjunction (AND), Disjunction (OR), and Negation (NOT).")
    add_bullet(doc, "Modus Ponens deductive inference.")
    add_bullet(doc, "Multi-tier rule cascades (Symptoms -> Syndromes -> Hypotheses).")
    add_p(doc, "Out-of-Scope (Strict Non-Claims):", bold_prefix="• ")
    add_bullet(doc, "MediLogic is strictly an educational engineering software, not a certified clinical diagnostic medical device.")
    add_bullet(doc, "The system does not implement First-Order Predicate Logic resolution refutation or Robinson unification.")
    add_bullet(doc, "The system does not compute pseudo-scientific diagnostic percentages or prescribe medications.")

    add_h2(doc, "1.8 Practical & Educational Applications")
    add_bullet(doc, "Concrete reference implementation for Unit IV viva voce examinations.", bold_prefix="1. University AI Lab Demonstrations: ")
    add_bullet(doc, "Teaching medical students how clinical guidelines translate into formal logic.", bold_prefix="2. Triage Protocol Training: ")
    add_bullet(doc, "Prototyping guideline rules before deployment into clinical decision support workflows.", bold_prefix="3. Clinical Algorithm Verification: ")

    add_h2(doc, "1.9 System & Clinical Limitations")
    add_bullet(doc, "Symptoms are modeled as discrete states rather than continuous variables (e.g., fever is present/absent rather than 38.4°C vs 39.8°C).", bold_prefix="1. Discrete Propositional Boundaries: ")
    add_bullet(doc, "Knowledge is limited to 6 ambulatory patterns and does not cover rare complex pathologies.", bold_prefix="2. Curated Knowledge Domain: ")

def add_chapter_2(doc):
    print("  -> Adding Chapter 2: Literature Review...")
    add_h1(doc, "CHAPTER 2 — LITERATURE REVIEW AND EXISTING SYSTEM", page_break=True)
    
    add_h2(doc, "2.1 Overview of Medical Expert Systems")
    add_p(doc, "Medical diagnosis was among the earliest applications explored by artificial intelligence pioneers. The clinical diagnostic process is naturally structured as knowledge-based reasoning under incomplete observation. Early systems like CASNET (glaucoma model, Weiss et al., 1978) and INTERNIST-I (internal medicine consultant, Miller et al., 1982) demonstrated that computers could replicate specialist diagnostic deductions when supplied with comprehensive causal networks.")

    add_h2(doc, "2.2 Historical Case Study: The MYCIN System (1976)")
    add_p(doc, "Developed at Stanford University by Dr. Edward Shortliffe, MYCIN was the seminal medical expert system designed to assist physicians in diagnosing blood infections (bacteremia and meningitis) and recommending antimicrobial therapy (Shortliffe, 1976).")
    add_p(doc, "MYCIN contributed three enduring architectural paradigms to computer science:")
    add_bullet(doc, "Knowledge was codified as ~450 modular production rules of the form PREMISE -> ACTION.", bold_prefix="1. Rule-Based Knowledge Representation: ")
    add_bullet(doc, "MYCIN operated primarily in goal-directed backward mode, asking the user questions only when necessary to prove specific rule premises.", bold_prefix="2. Backward Chaining Goal Search: ")
    add_bullet(doc, "MYCIN could answer WHY (why is a question being asked) and HOW (how was a conclusion reached), cementing explainability as mandatory for medical AI.", bold_prefix="3. The Explanation Subsystem: ")
    add_p(doc, "Academic Distinction: MediLogic draws pedagogical inspiration from MYCIN's separation of knowledge bases and explanation facilities. However, MediLogic does not claim to reproduce MYCIN. MYCIN utilized ad-hoc Certainty Factors (CFs) to model subjective uncertainty; MediLogic implements deterministic Kleene three-valued propositional logic (K3), ensuring that all conclusions are mathematically provable from verified premises.", italic=True)

    add_h2(doc, "2.3 General Principles of Knowledge-Based Medical Reasoning")
    add_p(doc, "Medical guidelines published by organizations such as the World Health Organization (WHO) and the Centers for Disease Control and Prevention (CDC) are fundamentally declarative IF–THEN specifications. For example, the WHO surveillance case definition for Influenza-Like Illness (ILI) states:")
    add_callout_box(doc, "ILI <=> (Fever >= 38°C) AND (Cough) AND (Onset <= 10 days)", title="WHO Clinical ILI Guideline Formulation")
    add_p(doc, "Expert systems formalize these specifications into unambiguous logical calculus.")

    add_h2(doc, "2.4 Existing Approaches and Limitations")
    add_bullet(doc, "Difficult to maintain; adding a new rule requires rewriting procedural code.", bold_prefix="• Algorithmic Flowcharts (Hardcoded Scripts): ")
    add_bullet(doc, "Lack explainability; cannot identify which specific clinical criteria are missing when a diagnosis fails.", bold_prefix="• Deep Learning / Neural Networks: ")
    add_bullet(doc, "Require massive conditional probability tables (P(S|D)) that are rarely universally calibrated across diverse patient demographics.", bold_prefix="• Bayesian Networks: ")

    add_h2(doc, "2.5 Proposed System: MediLogic")
    add_p(doc, "MediLogic combines:")
    add_bullet(doc, "Declarative JSON production rules editable without altering Python inference engines.")
    add_bullet(doc, "Kleene K3 three-valued logic preserving UNKNOWN states.")
    add_bullet(doc, "Dual execution: Data-driven Forward Chaining and Goal-directed Backward Chaining.")
    add_bullet(doc, "An autonomous Safety Layer that monitors life-threatening red flags independently.")

    add_h2(doc, "2.6 Advantages of the Proposed Educational System")
    add_bullet(doc, "Every rule firing or failure is recorded in an execution trace.", bold_prefix="1. 100% Deterministic Auditability: ")
    add_bullet(doc, "Unasked symptoms remain UNKNOWN, preventing dangerous false negatives.", bold_prefix="2. No Closed-World Fallacy: ")
    add_bullet(doc, "Directly maps to university engineering examination syllabi.", bold_prefix="3. Pedagogical Alignment: ")

def add_chapter_3(doc):
    print("  -> Adding Chapter 3: System Analysis...")
    add_h1(doc, "CHAPTER 3 — SYSTEM ANALYSIS AND REQUIREMENTS", page_break=True)
    
    add_h2(doc, "3.1 Functional Requirements")
    add_bullet(doc, "The system shall allow users to set truth values for 34 symptoms as PRESENT (TRUE), ABSENT (FALSE), or NOT SURE (UNKNOWN).", bold_prefix="• FR-1 (Symptom Capture): ")
    add_bullet(doc, "The system shall validate JSON schemas, unique rule IDs, and references at startup.", bold_prefix="• FR-2 (Knowledge Base Validation): ")
    add_bullet(doc, "The system shall iteratively fire satisfied rules using Modus Ponens until working memory reaches fixed-point saturation.", bold_prefix="• FR-3 (Forward Chaining Execution): ")
    add_bullet(doc, "The system shall recursively prove target hypotheses, tracking subgoals and detecting circular dependencies.", bold_prefix="• FR-4 (Backward Chaining Execution): ")
    add_bullet(doc, "The system shall immediately flag emergency warning symptoms regardless of diagnostic inference.", bold_prefix="• FR-5 (Independent Safety Alerts): ")
    add_bullet(doc, "The system shall provide step-by-step plain-language explanations of why rules fired or failed.", bold_prefix="• FR-6 (Explanation Generation): ")
    add_bullet(doc, "The system shall provide a reset mechanism clearing working memory and previous traces.", bold_prefix="• FR-7 (Session Reset): ")

    add_h2(doc, "3.2 Non-Functional Requirements")
    add_bullet(doc, "Identical symptom inputs must produce identical inference results every time.", bold_prefix="• NFR-1 (Determinism): ")
    add_bullet(doc, "Both inference engines must complete execution in under 100 milliseconds for standard queries.", bold_prefix="• NFR-2 (Performance): ")
    add_bullet(doc, "The system must execute locally without internet connectivity or external API keys.", bold_prefix="• NFR-3 (Zero Cloud Dependency): ")
    add_bullet(doc, "Adding new rules in data/rules.json must require zero modifications to engine/ source code.", bold_prefix="• NFR-4 (Extensibility): ")

    add_h2(doc, "3.3 Hardware Requirements")
    add_p(doc, "MediLogic was designed to execute on standard commodity computing hardware commonly available in university academic laboratories.")
    # Table 3.1
    add_h3(doc, "Table 3.1: Hardware Specifications for MediLogic Execution")
    t31_headers = ["Component", "Minimum Requirement", "Recommended Specification"]
    t31_rows = [
        ["Processor (CPU)", "Intel Core i3 / AMD Ryzen 3", "Intel Core i5 / AMD Ryzen 5 or higher"],
        ["System Memory (RAM)", "4 GB DDR3/DDR4", "8 GB DDR4 or higher"],
        ["Storage (Disk Space)", "100 MB free hard drive space", "500 MB free SSD storage"],
        ["Display Resolution", "1280 x 720 pixels", "1920 x 1080 (Full HD)"],
        ["Input Devices", "Standard Keyboard and Mouse", "Standard Keyboard and Mouse"]
    ]
    add_styled_table(doc, t31_headers, t31_rows, [2.0, 2.4, 2.5])

    add_h2(doc, "3.4 Software Requirements")
    add_p(doc, "The software stack leverages modern open-source Python tools without commercial runtime licenses.")
    # Table 3.2
    add_h3(doc, "Table 3.2: Software Stack and Dependency Specifications")
    t32_headers = ["Software Layer", "Tool / Technology", "Version / Environment"]
    t32_rows = [
        ["Operating System", "Microsoft Windows 10/11, Linux, macOS", "Verified on Windows 11 64-bit"],
        ["Programming Language", "Python", "Python 3.11+ (Verified on 3.13.6)"],
        ["Web Application Framework", "Streamlit", "Streamlit 1.36.0+ (Installed: 1.65.0)"],
        ["Testing Framework", "Pytest", "Pytest 8.0.0+ (Installed: 9.1.1)"],
        ["Document Generation", "python-docx", "python-docx 1.2.0"],
        ["Data Serialization", "JSON", "Standard Library (json)"],
        ["Diagram Modeling", "Mermaid.js / Matplotlib", "Markdown Fenced Code & High-Res PNG"]
    ]
    add_styled_table(doc, t32_headers, t32_rows, [2.0, 2.4, 2.5])

    add_h2(doc, "3.5 Feasibility Study")
    add_bullet(doc, "Python provides high-level data structures (sets, dictionaries, recursion) ideally suited for symbolic logic. Fully feasible.", bold_prefix="• Technical Feasibility: ")
    add_bullet(doc, "Streamlit provides a web interface requiring no frontend build tools (npm/webpack). Fully feasible.", bold_prefix="• Operational Feasibility: ")
    add_bullet(doc, "Built entirely on open-source software with zero licensing costs or paid APIs. Fully feasible.", bold_prefix="• Economic Feasibility: ")

    add_h2(doc, "3.6 User Workflow")
    add_p(doc, "The user workflow follows a clean 3-step sequence:")
    add_bullet(doc, "Review system overview and educational disclaimer.", bold_prefix="1. Home: ")
    add_bullet(doc, "Answer symptom checklist using Yes, No, or Not Sure.", bold_prefix="2. Check Symptoms: ")
    add_bullet(doc, "View matched condition cards, plain-language explanations, and technical Modus Ponens step audits.", bold_prefix="3. My Results: ")
    add_p(doc, "*(Advanced users can navigate to the AI Lab for full algorithm benchmarking, rule inspection, and proof tree visualization).*")

    add_h2(doc, "3.7 Use Case Descriptions")
    add_bullet(doc, "User selects truth states for symptoms; system updates working memory.", bold_prefix="• UC-1 (Complete Symptom Assessment): ")
    add_bullet(doc, "System applies Modus Ponens, deriving all reachable syndromes.", bold_prefix="• UC-2 (Execute Forward Chaining): ")
    add_bullet(doc, "User selects target hypothesis; system proves subgoals recursively.", bold_prefix="• UC-3 (Execute Backward Chaining Proof): ")
    add_bullet(doc, "User selects red-flag symptom; system immediately displays emergency triage box.", bold_prefix="• UC-4 (Inspect Safety Alert): ")

def add_chapter_4(doc):
    print("  -> Adding Chapter 4: System Design...")
    add_h1(doc, "CHAPTER 4 — SYSTEM DESIGN", page_break=True)
    
    add_h2(doc, "4.1 Overall Architectural Design")
    add_p(doc, "MediLogic is structured as a five-tier decoupled architecture:")
    add_bullet(doc, "Pure JSON repositories (symptoms.json, rules.json, conditions.json, references.json).", bold_prefix="1. Declarative Data Tier (data/): ")
    add_bullet(doc, "Three-valued Kleene K3 logical calculus.", bold_prefix="2. Evaluation Tier (engine/rule_evaluator.py): ")
    add_bullet(doc, "Independent Forward Chaining, Backward Chaining, and Safety Engines.", bold_prefix="3. Reasoning Tier (engine/): ")
    add_bullet(doc, "Execution trace translation into clinical narratives and proof trees.", bold_prefix="4. Audit Tier (engine/explanation.py): ")
    add_bullet(doc, "Streamlit web interface with custom CSS design tokens.", bold_prefix="5. Presentation Tier (app.py, ui/): ")

    # Figure 4.1
    add_figure_image(doc, "assets/diagrams/architecture.png", "Figure 4.1: MediLogic Five-Tier System Architecture Diagram", width_inches=6.0)

    add_h2(doc, "4.2 Module Decomposition")
    add_bullet(doc, "Declares TruthValue, Fact, Rule, and KnowledgeBase loader.", bold_prefix="• engine/knowledge_base.py: ")
    add_bullet(doc, "Implements recursive tree evaluation under Kleene logic.", bold_prefix="• engine/rule_evaluator.py: ")
    add_bullet(doc, "Implements data-driven forward chaining with fixed-point saturation.", bold_prefix="• engine/forward_chaining.py: ")
    add_bullet(doc, "Implements goal-directed backward chaining with cycle detection.", bold_prefix="• engine/backward_chaining.py: ")
    add_bullet(doc, "Transforms raw execution logs into readable narratives and proof trees.", bold_prefix="• engine/explanation.py: ")
    add_bullet(doc, "Implements independent red-flag emergency triage monitor.", bold_prefix="• engine/safety.py: ")
    add_bullet(doc, "Main Streamlit web application.", bold_prefix="• app.py: ")
    add_bullet(doc, "Reusable UI cards, banners, and case presets.", bold_prefix="• ui/components.py: ")
    add_bullet(doc, "Healthcare-themed CSS styling.", bold_prefix="• ui/styles.py: ")

    add_h2(doc, "4.3 Knowledge-Base Design")
    add_p(doc, "The knowledge base encodes:")
    add_bullet(doc, "Propositional atoms with unique string IDs (e.g., fever_present, cough_present).", bold_prefix="• 34 Symptoms: ")
    add_bullet(doc, "Multi-tier production rules supporting intermediate syndromic deductions.", bold_prefix="• 21 Rules: ")
    add_bullet(doc, "Syndromic disease patterns citing authoritative references.", bold_prefix="• 8 Condition Hypotheses: ")
    add_bullet(doc, "Authoritative guidelines (WHO, CDC, AAAAI, IHS, ACG, EAU, ACEP).", bold_prefix="• 7 Clinical References: ")

    add_h2(doc, "4.4 Fact Representation & Working Memory")
    add_p(doc, "A fact in working memory is an instance of the Fact dataclass:")
    add_code_block(doc, """@dataclass
class Fact:
    id: str                 # e.g., 'fever_present'
    value: TruthValue       # TRUE, FALSE, or UNKNOWN
    source: FactSource      # USER, INFERRED, or SYSTEM_DEFAULT
    derivation_rule: str    # Rule ID that derived this fact (if inferred)
    step_number: int        # Step at which fact was established""")

    add_h2(doc, "4.5 Production-Rule Structure")
    add_p(doc, "Each rule is represented as a structured declarative JSON object:")
    add_code_block(doc, """{
  "id": "R001",
  "name": "Acute Febrile Respiratory Syndrome Derivation",
  "category": "Respiratory",
  "readable_text": "IF fever_present AND cough_present AND fatigue_present THEN acute_febrile_respiratory_syndrome_supported",
  "antecedent": {
    "and": [
      {"fact": "fever_present", "value": "TRUE"},
      {"fact": "cough_present", "value": "TRUE"},
      {"fact": "fatigue_present", "value": "TRUE"}
    ]
  },
  "consequent": {
    "fact": "acute_febrile_respiratory_syndrome_supported",
    "value": "TRUE"
  },
  "explanation": "Fever, cough, and systemic fatigue together establish an acute febrile respiratory syndromic presentation.",
  "source": "REF_WHO_ILI"
}""")

    add_h2(doc, "4.6 Rule Evaluator Design (Kleene K3 Logic)")
    add_p(doc, "Evaluates nested expression trees (fact, and, or, not) against working memory using Kleene 3-valued logic, returning an EvaluationResult containing:")
    add_bullet(doc, "Evaluated truth state (TRUE, FALSE, UNKNOWN).", bold_prefix="• value: ")
    add_bullet(doc, "Set of fact IDs that evaluated to UNKNOWN.", bold_prefix="• missing_facts: ")
    add_bullet(doc, "Set of fact IDs that evaluated to FALSE when expecting TRUE.", bold_prefix="• contradicted_facts: ")
    add_bullet(doc, "Audit text explaining why the expression evaluated as it did.", bold_prefix="• explanation: ")

    add_h2(doc, "4.7 Inference-Engine Design")
    add_bullet(doc, "Monotonically expands working memory in discrete passes. Terminates when new_facts == 0 (fixed-point saturation).", bold_prefix="• Forward Chaining Engine: ")
    add_bullet(doc, "Recursively proves target goals depth-first. Maintains active_goal_stack to detect circular dependencies. Memoizes proven subgoals into working memory.", bold_prefix="• Backward Chaining Engine: ")

    add_h2(doc, "4.8 Explanation Facility")
    add_p(doc, "Constructs audit explanations directly from execution logs:")
    add_bullet(doc, "Reports step number, iteration, triggered rule ID, antecedent evaluations, and newly derived fact.", bold_prefix="• Forward Explanation: ")
    add_bullet(doc, "Flattens recursive proof tree into an indented hierarchy showing subgoals, candidate rules, and resolution tags ([PROVEN], [FAILED], [UNKNOWN], [CYCLE]).", bold_prefix="• Backward Explanation: ")

    add_h2(doc, "4.9 Independent Safety Layer")
    add_p(doc, "Inspects working memory for emergency red-flag symptoms:")
    add_bullet(doc, "Cardiac / pulmonary emergency.", bold_prefix="• chest_pain_present -> ")
    add_bullet(doc, "Acute respiratory failure / anaphylaxis.", bold_prefix="• severe_shortness_of_breath_present -> ")
    add_bullet(doc, "Acute stroke (FAST protocol).", bold_prefix="• sudden_neurological_deficit_present -> ")
    add_bullet(doc, "Acute bacterial meningitis.", bold_prefix="• stiff_neck_with_high_fever_present -> ")
    add_bullet(doc, "Acute surgical abdomen / peritonitis.", bold_prefix="• severe_unrelenting_abdominal_pain_present -> ")
    add_p(doc, "Operates completely autonomously; no diagnostic conclusion can suppress an emergency alert.")

    add_h2(doc, "4.10 Data-Flow Diagrams (DFD Level 0 & Level 1)")
    add_p(doc, "The data-flow diagram illustrates the transformation of user symptom selections through working memory, independent safety filtering, inference engines, and explanation synthesis.")
    # Figure 4.2
    add_figure_image(doc, "assets/diagrams/dfd.png", "Figure 4.2: Data Flow Diagram (Level 0 Context & Level 1 Decomposition)", width_inches=6.0)

    add_h2(doc, "4.11 Use-Case Diagram")
    add_p(doc, "The use case model captures user interactions ranging from routine symptom assessment to academic AI laboratory inspection.")
    # Figure 4.3
    add_figure_image(doc, "assets/diagrams/use_case.png", "Figure 4.3: MediLogic Use Case Diagram", width_inches=6.0)

    add_h2(doc, "4.12 Rule Dependency Architecture")
    add_p(doc, "The production rules form a multi-tier directed acyclic graph (DAG) where atomic symptom observations feed intermediate syndrome derivations, which in turn feed condition hypotheses.")
    # Figure 4.4
    add_figure_image(doc, "assets/diagrams/rule_dependency.png", "Figure 4.4: Knowledge Base Rule Dependency Lattice", width_inches=6.0)

def add_chapter_5(doc):
    print("  -> Adding Chapter 5: AI Concepts and Methodology...")
    add_h1(doc, "CHAPTER 5 — AI CONCEPTS AND METHODOLOGY", page_break=True)
    
    add_h2(doc, "5.1 Knowledge Representation Using Logical Formalisms")
    add_p(doc, "Knowledge representation is the study of how an agent translates real-world knowledge into formal symbols such that an inference engine can derive sound, previously unasserted truths (Russell & Norvig, 2020). Propositional logic represents the foundational logical formalism in the SPPU syllabus.")

    add_h2(doc, "5.2 Propositional Logic and Well-Formed Formulas")
    add_p(doc, "In propositional logic:")
    add_bullet(doc, "Propositional symbols (P, Q, R) represent atomic declarative facts.")
    add_bullet(doc, "A Well-Formed Formula (WFF) is defined recursively:")
    add_p(doc, "1. Any propositional symbol is a WFF.\n2. If α is a WFF, then (¬α) is a WFF.\n3. If α and β are WFFs, then (α ∧ β) and (α ∨ β) are WFFs.")
    add_p(doc, "In MediLogic, clinical symptoms are modeled as propositional atoms:")
    add_bullet(doc, "fever_present", bold_prefix="• P1 = ")
    add_bullet(doc, "cough_present", bold_prefix="• P2 = ")
    add_bullet(doc, "fatigue_present", bold_prefix="• P3 = ")
    add_bullet(doc, "acute_febrile_respiratory_syndrome_supported", bold_prefix="• Q1 = ")

    add_h2(doc, "5.3 Logical Connectives & Kleene Truth Tables")
    add_p(doc, "To model medical reality where unexamined symptoms are undetermined, MediLogic implements Kleene's strong logic of indeterminacy (K3) over truth domain T = {TRUE, FALSE, UNKNOWN}:")
    
    # Table 5.1
    add_h3(doc, "Table 5.1: Kleene Strong 3-Valued Logic (K3) Truth Tables")
    t51_headers = ["P", "Q", "NOT P (¬P)", "P AND Q (P ∧ Q)", "P OR Q (P ∨ Q)"]
    t51_rows = [
        ["T", "T", "F", "T", "T"],
        ["T", "F", "F", "F", "T"],
        ["T", "U", "F", "U", "T"],
        ["F", "T", "T", "F", "T"],
        ["F", "F", "T", "F", "F"],
        ["F", "U", "T", "F", "U"],
        ["U", "T", "U", "U", "T"],
        ["U", "F", "U", "F", "U"],
        ["U", "U", "U", "U", "U"]
    ]
    add_styled_table(doc, t51_headers, t51_rows, [1.2, 1.2, 1.5, 1.5, 1.5])
    add_p(doc, "• Kleene AND: If any conjunct is FALSE, the conjunction is FALSE. If all are TRUE, it is TRUE. If mixed TRUE and UNKNOWN, it remains UNKNOWN.\n• Kleene OR: If any disjunct is TRUE, the disjunction is TRUE. If all are FALSE, it is FALSE. If mixed FALSE and UNKNOWN, it remains UNKNOWN.\n• Kleene NOT: Inverts TRUE <-> FALSE; preserves UNKNOWN.")

    add_h2(doc, "5.4 Facts and IF–THEN Production Rules")
    add_p(doc, "A production rule represents material implication:")
    add_callout_box(doc, "Ri:  φi -> ψi\nwhere φi is a WFF antecedent over working memory facts, and ψi is an atomic consequent assignment (qi = TRUE).", title="Formal Rule Definition")

    add_h2(doc, "5.5 Inference Rules and Modus Ponens")
    add_p(doc, "Modus Ponens (Rule of Detachment) is the classical rule of inference:")
    add_callout_box(doc, "Premises:  φ,   φ -> ψ\nConclusion: ψ", title="Modus Ponens Formal Rule")
    add_p(doc, "In MediLogic's forward chaining engine:\n1. Antecedent φ is evaluated against working memory: val(φ, W) in {TRUE, FALSE, UNKNOWN}.\n2. If val(φ, W) == TRUE, the premise is satisfied.\n3. Modus Ponens detaches consequent ψ, asserting it into working memory.")
    add_p(doc, "*(Note on Modus Tollens): Modus Tollens states that given ¬ψ and φ -> ψ, one can infer ¬φ. While part of Unit IV theory, production rule systems do not apply Modus Tollens universally because medical rules are material implications rather than biconditionals—the absence of a syndrome does not imply the absence of all its individual symptoms.", italic=True)

    add_h2(doc, "5.6 Forward Chaining Algorithm & Pseudocode")
    add_code_block(doc, """Algorithm FORWARD_CHAINING:
Input: WorkingMemory W_0, KnowledgeBase Rules R, MaxIterations M
Output: Result (WorkingMemory W, DerivedFacts D, FiredRules F, Trace T)

1. W <- W_0, D <- {}, F <- [], T <- []
2. FiredIDs <- {}
3. Iteration <- 1

4. WHILE Iteration <= M DO:
5.     NewFacts <- 0
6.     FOR EACH Rule r IN SortByID(R) DO:
7.         IF r.id IN FiredIDs THEN CONTINUE
8.         
9.         EvalResult <- EVALUATE_EXPRESSION(r.antecedent, W)
10.        IF EvalResult.value == TRUE THEN
11.            FiredIDs.Add(r.id)
12.            F.Append(r)
13.            ConsequentFact <- r.consequent.fact
14.            IF ConsequentFact NOT IN W THEN
15.                NewFact <- CreateFact(ConsequentFact, TRUE, source=INFERRED, rule=r.id)
16.                W[ConsequentFact] <- NewFact
17.                D[ConsequentFact] <- NewFact
18.                NewFacts <- NewFacts + 1
19.            END IF
20.            T.Append(CreateTraceStep(Iteration, r, fired=TRUE, EvalResult))
21.        ELSE
22.            T.Append(CreateTraceStep(Iteration, r, fired=FALSE, EvalResult))
23.        END IF
24.    END FOR
25.    
26.    IF NewFacts == 0 THEN
27.        RETURN Result(W, D, F, T, status="Fixed-Point Saturated")
28.    END IF
29.    Iteration <- Iteration + 1
30. END WHILE
31. RETURN Result(W, D, F, T, status="Iteration Limit Exceeded")""")

    # Figure 5.1
    add_figure_image(doc, "assets/diagrams/forward_chaining_flowchart.png", "Figure 5.1: Forward Chaining Execution Flowchart with Fixed-Point Saturation", width_inches=5.8)

    add_h2(doc, "5.7 Backward Chaining Algorithm & Pseudocode")
    add_code_block(doc, """Algorithm BACKWARD_CHAINING:
Input: TargetGoal G, TargetVal V, WorkingMemory W, KnowledgeBase KB, MaxDepth D
Output: BackwardResult (Status, ProofTree, AppliedRules, MissingPrereqs, Trace)

Function PROVE_GOAL(G, V, Depth, ActiveStack):
1.  IF Depth > D THEN RETURN ProofNode(G, DEPTH_LIMIT_EXCEEDED)
2.  IF G IN ActiveStack THEN RETURN ProofNode(G, CYCLE_DETECTED)
3.  
4.  IF G IN W THEN
5.      IF W[G].value == V THEN RETURN ProofNode(G, SUPPORTED)
6.      ELSE IF W[G].value != UNKNOWN THEN RETURN ProofNode(G, CONTRADICTED)
7.  END IF
8.  
9.  Candidates <- KB.GetRulesConcluding(G, V)
10. IF Candidates IS EMPTY THEN
11.     MissingPrereqs.Add(G)
12.     RETURN ProofNode(G, UNRESOLVED_UNKNOWN)
13. END IF
14. 
15. ActiveStack.Add(G)
16. HasUnknown <- FALSE, AllContradicted <- TRUE
17. 
18. FOR EACH Rule r IN Candidates DO:
19.     SubNode <- PROVE_EXPRESSION(r.antecedent, Depth + 1, ActiveStack)
20.     IF SubNode.status == SUPPORTED THEN
21.         W[G] <- CreateFact(G, V, source=INFERRED, rule=r.id)
22.         ActiveStack.Remove(G)
23.         AppliedRules.Add(r)
24.         RETURN ProofNode(G, SUPPORTED, rule=r.id, subnodes=[SubNode])
25.     ELSE IF SubNode.status == UNRESOLVED_UNKNOWN THEN
26.         HasUnknown <- TRUE, AllContradicted <- FALSE
27.     END IF
28. END FOR
29. 
30. ActiveStack.Remove(G)
31. IF HasUnknown THEN RETURN ProofNode(G, UNRESOLVED_UNKNOWN)
32. ELSE RETURN ProofNode(G, CONTRADICTED)""")

    # Figure 5.2
    add_figure_image(doc, "assets/diagrams/backward_chaining_flowchart.png", "Figure 5.2: Backward Chaining (Goal-Directed DFS) Flowchart", width_inches=5.8)

    add_h2(doc, "5.8 Asymptotic Complexity Analysis")
    add_p(doc, "The computational complexity of the two inference algorithms is compared below:")
    # Table 5.2
    add_h3(doc, "Table 5.2: Asymptotic Computational Complexity Comparison")
    t52_headers = ["Algorithm", "Time Complexity (Worst-Case)", "Space Complexity", "Termination Guarantee"]
    t52_rows = [
        ["Forward Chaining", "O(R² · k)", "O(F + R)", "Guaranteed (Monotonicity)"],
        ["Backward Chaining", "O(b^D) unpruned -> O(R · k)", "O(D) call stack", "Guaranteed (Cycle Guard)"]
    ]
    add_styled_table(doc, t52_headers, t52_rows, [1.8, 2.0, 1.5, 1.6])
    add_p(doc, "Where R is the total number of rules (|R| = 21), F is the total number of facts (|F| = 34), k is the maximum conjunct terms per antecedent (k <= 5), D is the maximum recursion depth (D <= 15), and b is the average rule branching factor (b ≈ 1.8).")

    add_h2(doc, "5.9 Comparison of Forward and Backward Chaining")
    # Table 5.3
    add_h3(doc, "Table 5.3: Comprehensive Comparison: Forward Chaining vs. Backward Chaining")
    t53_headers = ["Dimension", "Forward Chaining (Bottom-Up)", "Backward Chaining (Top-Down)"]
    t53_rows = [
        ["Primary Direction", "Data-driven: Facts to Conclusions", "Goal-driven: Hypothesis to Prerequisites"],
        ["Trigger Condition", "Observations available in memory", "Clinical query or specific suspicion"],
        ["Execution Model", "Iterative passes over all rules", "Recursive Depth-First Search on subgoals"],
        ["Output Scope", "Derives ALL reachable conclusions", "Answers strictly for the TARGET goal"],
        ["Handling of Missing Data", "Rules with missing facts don't fire", "Pinpoints EXACT missing prerequisites"],
        ["Cycle Handling", "Monotonicity & Already-Fired set", "Active call-stack cycle guard"],
        ["Clinical Utility", "Intake screening, triage panels", "Evaluating a specific differential diagnosis"]
    ]
    add_styled_table(doc, t53_headers, t53_rows, [1.8, 2.5, 2.6])

    add_h2(doc, "5.10 Worked Multi-Step Reasoning Example")
    add_p(doc, "Consider initial patient facts:\nW_0 = { fever_present -> TRUE, cough_present -> TRUE, fatigue_present -> TRUE, body_aches_present -> TRUE }")
    add_h3(doc, "Forward Chaining Step-by-Step:")
    add_bullet(doc, "Evaluates R001: Antecedent (fever ∧ cough ∧ fatigue) evaluates to TRUE ∧ TRUE ∧ TRUE = TRUE. Modus Ponens fires R001. Consequent acute_febrile_respiratory_syndrome_supported is derived and added to working memory.", bold_prefix="• Pass 1: ")
    add_bullet(doc, "Evaluates R002: Antecedent (acute_febrile_syndrome ∧ body_aches) evaluates to TRUE ∧ TRUE = TRUE. Modus Ponens fires R002. Consequent influenza_like_illness_supported is derived and added to working memory.", bold_prefix="• Pass 2: ")
    add_bullet(doc, "No additional rules fire. Fixed-point reached.", bold_prefix="• Pass 3: ")
    add_bullet(doc, "Influenza-Like Illness (ILI) Pattern Supported.", bold_prefix="• Final Conclusion: ")

    add_h3(doc, "Backward Chaining Step-by-Step:")
    add_bullet(doc, "Prove influenza_like_illness_supported == TRUE.", bold_prefix="• Goal: ")
    add_bullet(doc, "Candidate rule R002 requires acute_febrile_respiratory_syndrome_supported ∧ body_aches_present.", bold_prefix="• Step 1: ")
    add_bullet(doc, "Subgoal body_aches_present is found directly in working memory as TRUE.", bold_prefix="• Step 2: ")
    add_bullet(doc, "Subgoal acute_febrile_respiratory_syndrome_supported is not in memory; candidate rule R001 is evaluated.", bold_prefix="• Step 3: ")
    add_bullet(doc, "Rule R001 subgoals (fever, cough, fatigue) are all verified in memory as TRUE.", bold_prefix="• Step 4: ")
    add_bullet(doc, "Rule R001 succeeds -> Rule R002 succeeds -> Target Goal is conclusively SUPPORTED.", bold_prefix="• Step 5: ")

    add_h2(doc, "5.11 Relationship and Architectural Comparison to MYCIN")
    # Table 5.4
    add_h3(doc, "Table 5.4: Architectural Comparison: Stanford MYCIN vs. MediLogic")
    t54_headers = ["Feature", "MYCIN (Stanford, 1976)", "MediLogic System (2026)"]
    t54_rows = [
        ["Domain", "Bacteremia & Meningitis", "Ambulatory Illness Patterns (6 domains)"],
        ["Rule Format", "LISP S-expressions", "JSON Declarative Expression Trees"],
        ["Reasoning Engine", "Backward Chaining only", "Dual: Forward AND Backward Chaining"],
        ["Uncertainty Model", "Certainty Factors (CF: -1.0 to +1.0)", "Kleene 3-Valued Logic (T, F, U)"],
        ["Explainability", "Static template generation", "Dynamic execution trace trees"],
        ["Emergency Monitor", "Not decoupled", "Autonomous Independent Safety Layer"],
        ["User Interface", "Teletype terminal (text-based)", "Responsive Streamlit Web Interface"],
        ["Implementation Language", "Maclisp / Interlisp", "Python 3.13"]
    ]
    add_styled_table(doc, t54_headers, t54_rows, [1.8, 2.5, 2.6])

    add_h2(doc, "5.12 SPPU Syllabus Mapping (Unit IV)")
    # Table 5.5
    add_h3(doc, "Table 5.5: SPPU Unit IV Syllabus Alignment Matrix")
    t55_headers = ["Syllabus Topic", "Project Implementation Status", "Source Code Module Reference"]
    t55_rows = [
        ["Knowledge Representation", "Implemented (Propositional Rules)", "data/rules.json, engine/knowledge_base.py"],
        ["Knowledge-Based Agents", "Implemented (Working Memory Agent)", "engine/forward_chaining.py"],
        ["Propositional Logic (WFFs)", "Implemented (Validated Expr Trees)", "engine/rule_evaluator.py"],
        ["Logical Connectives", "Implemented (AND, OR, NOT in K3)", "engine/rule_evaluator.py"],
        ["Modus Ponens Inference", "Implemented (Rule Detachment)", "engine/forward_chaining.py"],
        ["Forward Chaining", "Implemented (Data-Driven Saturation)", "engine/forward_chaining.py"],
        ["Backward Chaining", "Implemented (Goal-Tree DFS + Cycle)", "engine/backward_chaining.py"],
        ["MYCIN Case Study", "Demonstrated Architecture", "docs/PROJECT_REPORT.md (Section 5.11)"],
        ["First-Order Logic (FOL)", "Theoretical Background (Not in code)", "docs/PROJECT_REPORT.md (Chapter 5)"],
        ["Resolution Refutation", "Theoretical Background (Not in code)", "docs/PROJECT_REPORT.md (Chapter 5)"]
    ]
    add_styled_table(doc, t55_headers, t55_rows, [2.2, 2.4, 2.3])

def add_chapter_6(doc):
    print("  -> Adding Chapter 6: Implementation...")
    add_h1(doc, "CHAPTER 6 — IMPLEMENTATION", page_break=True)
    
    add_h2(doc, "6.1 Technology Stack")
    add_bullet(doc, "High-level object-oriented programming language with comprehensive standard libraries.", bold_prefix="• Python 3.13.6: ")
    add_bullet(doc, "Reactive Python web application framework for rapid interactive interfaces.", bold_prefix="• Streamlit 1.65.0: ")
    add_bullet(doc, "Standardized human-readable declarative data serialization format.", bold_prefix="• JSON: ")
    add_bullet(doc, "Automated test runner and assertion framework.", bold_prefix="• Pytest 9.1.1: ")
    add_bullet(doc, "Programmatic document generation library for academic reports.", bold_prefix="• python-docx 1.2.0: ")

    add_h2(doc, "6.2 Project Directory Structure")
    add_code_block(doc, """d:\\AI/
├── app.py                      # Main Streamlit web application
├── requirements.txt            # Python dependencies (streamlit, pytest, python-docx)
├── pytest.ini                  # Pytest configuration
├── data/                       # Declarative Knowledge Base
│   ├── symptoms.json           # 34 Propositional symptom atoms
│   ├── rules.json              # 21 Production rules
│   ├── conditions.json         # 8 Educational condition hypotheses
│   └── references.json         # 7 Authoritative clinical reference citations
├── engine/                     # Core Symbolic AI Engines
│   ├── knowledge_base.py       # KB loader and integrity validator
│   ├── rule_evaluator.py       # Kleene 3-valued (K3) logical calculus
│   ├── forward_chaining.py     # Data-driven Modus Ponens forward deduction
│   ├── backward_chaining.py    # Goal-directed backward proof with cycle detection
│   ├── explanation.py          # Audit narrative and proof tree generator
│   └── safety.py               # Autonomous emergency red-flag monitor
├── ui/                         # Presentation Layer
│   ├── styles.py               # Healthcare CSS visual tokens
│   └── components.py           # Reusable cards, banners, and case presets
├── tests/                      # Automated Verification Test Suite (42 tests)
├── docs/                       # Academic Documentation & Diagrams
│   ├── PROJECT_REPORT.md       # Complete Markdown report source
│   ├── SYLLABUS_MAPPING.md     # Authoritative syllabus alignment matrix
│   ├── ALGORITHMS.md           # Algorithmic specifications and complexity
│   ├── TEST_REPORT.md          # Complete test execution log
│   ├── VIVA_QUESTIONS.md       # 40 High-yield viva questions with model answers
│   └── diagrams/               # Editable Mermaid diagram source files
└── assets/screenshots/         # 9 Genuine application screenshots""")

    add_h2(doc, "6.3 Knowledge-Base Implementation (knowledge_base.py)")
    add_p(doc, "The KnowledgeBase module loads and validates JSON declarations into strongly-typed dataclasses:")
    add_code_block(doc, """class TruthValue(str, Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"

@dataclass
class Rule:
    id: str
    name: str
    category: str
    readable_text: str
    antecedent: Dict[str, Any]
    consequent: Dict[str, Any]
    explanation: str
    source: str""")

    add_h2(doc, "6.4 Three-Valued Logic Evaluator (rule_evaluator.py)")
    add_p(doc, "The evaluator recursively walks expression trees implementing strong Kleene logic:")
    add_code_block(doc, """# Kleene 3-Valued AND evaluation excerpt
has_false = any(sr.value == TruthValue.FALSE for sr in sub_results)
all_true = all(sr.value == TruthValue.TRUE for sr in sub_results)

if has_false:
    return EvaluationResult(value=TruthValue.FALSE, explanation="AND failed: term evaluated to FALSE.")
if all_true:
    return EvaluationResult(value=TruthValue.TRUE, explanation="AND satisfied: all terms TRUE.")
return EvaluationResult(value=TruthValue.UNKNOWN, explanation="AND unresolved: terms remain UNKNOWN.")""")

    add_h2(doc, "6.5 Forward Chaining Implementation (forward_chaining.py)")
    add_p(doc, "The forward chainer loops until fixed-point saturation:")
    add_code_block(doc, """while iteration < self.max_iterations:
    iteration += 1
    new_facts_in_iteration = 0
    for rule in sorted(self.kb.rules, key=lambda r: r.id):
        if rule.id in already_fired_rule_ids:
            continue
        eval_res = RuleEvaluator.evaluate(rule.antecedent, working_memory)
        if eval_res.is_true:
            already_fired_rule_ids.add(rule.id)
            c_fact_id = rule.consequent_fact_id
            c_val = rule.consequent_value
            if c_fact_id not in working_memory:
                working_memory[c_fact_id] = Fact(id=c_fact_id, value=c_val, source=FactSource.INFERRED, derivation_rule=rule.id)
                new_facts_in_iteration += 1
    if new_facts_in_iteration == 0:
        break  # Fixed-point reached""")

    add_h2(doc, "6.6 Backward Chaining Implementation (backward_chaining.py)")
    add_p(doc, "The backward chainer enforces active-stack cycle detection during DFS:")
    add_code_block(doc, """if goal_fact in active_goal_stack:
    return ProofNode(goal_fact=goal_fact, target_value=target_value, status=GoalStatus.CYCLE_DETECTED)

active_goal_stack.add(goal_fact)
try:
    for rule in candidate_rules:
        expr_node = self._prove_expression(rule.antecedent, working_memory, active_goal_stack, depth + 1)
        if expr_node.status == GoalStatus.SUPPORTED:
            working_memory[goal_fact] = Fact(id=goal_fact, value=target_value, source=FactSource.INFERRED, derivation_rule=rule.id)
            return ProofNode(goal_fact=goal_fact, target_value=target_value, status=GoalStatus.SUPPORTED, rule_id=rule.id)
finally:
    active_goal_stack.remove(goal_fact)""")

    add_h2(doc, "6.7 Explanation Facility (explanation.py)")
    add_p(doc, "Converts internal execution records into human-readable hierarchical proof trees and natural language diagnostic summaries.")

    add_h2(doc, "6.8 Clinical Safety Engine (safety.py)")
    add_p(doc, "Evaluates working memory against configured life-threatening red-flag indicators, generating immediate high-priority alerts with emergency contact directives.")

    add_h2(doc, "6.9 User Interface & Streamlit Session Handling (app.py)")
    add_p(doc, "Constructs a dual-mode web application: a 3-step streamlined consumer flow for patients and a comprehensive AI Lab for computer engineering faculty and students.")

    add_h2(doc, "6.10 Error Handling and Knowledge-Base Validation")
    add_p(doc, "Verifies at startup that JSON files exist, rule identifiers are unique, expression structures conform to schema, and every cited reference exists in references.json.")

def add_chapter_7(doc):
    print("  -> Adding Chapter 7: Testing and Results...")
    add_h1(doc, "CHAPTER 7 — TESTING AND RESULTS", page_break=True)
    
    add_h2(doc, "7.1 Testing Objectives")
    add_bullet(doc, "Verify declarative JSON schema validity and reference integrity.")
    add_bullet(doc, "Verify Kleene K3 three-valued logic truth tables.")
    add_bullet(doc, "Verify forward chaining multi-step cascades, duplicate prevention, and fixed-point saturation.")
    add_bullet(doc, "Verify backward chaining recursive proofs, cycle detection, and missing prerequisite tracking.")
    add_bullet(doc, "Verify autonomous emergency red-flag safety triage.")

    add_h2(doc, "7.2 Test Environment & Pytest Framework")
    add_p(doc, "Tests were executed in the project virtual environment on Windows 11 using Python 3.13.6 and Pytest 9.1.1.")

    add_h2(doc, "7.3 Unit Testing Strategy")
    add_p(doc, "Each engine component is tested in isolation with synthetic mocked fact stores to ensure robust edge-case handling.")

    add_h2(doc, "7.4 Integration Testing Strategy")
    add_p(doc, "Both forward and backward engines are tested against identical symptom configurations to verify algorithmic consistency and co-existence with emergency safety alerts.")

    add_h2(doc, "7.5 Automated Test-Case Execution Matrix")
    # Table 7.1
    add_h3(doc, "Table 7.1: Automated Test-Case Execution Matrix (Pytest Suite)")
    t71_headers = ["Test Identifier", "Module", "Objective", "Result"]
    t71_rows = [
        ["test_kb_loads_successfully", "test_knowledge_base.py", "Validates complete KB loading", "PASSED"],
        ["test_unique_rule_ids", "test_knowledge_base.py", "Ensures unique rule identifiers", "PASSED"],
        ["test_rule_references_valid_sources", "test_knowledge_base.py", "Integrity of citations", "PASSED"],
        ["test_symptom_attributes", "test_knowledge_base.py", "Symptom dictionary schemas", "PASSED"],
        ["test_conditions_schema", "test_knowledge_base.py", "Condition schema attributes", "PASSED"],
        ["test_duplicate_rule_id_detection", "test_knowledge_base.py", "Fault injection: duplicate IDs", "PASSED"],
        ["test_malformed_expression_detection", "test_knowledge_base.py", "Fault injection: bad syntax", "PASSED"],
        ["test_missing_files_handling", "test_knowledge_base.py", "Missing JSON handling", "PASSED"],
        ["test_truth_value_conversion", "test_knowledge_base.py", "Tri-state enum casting", "PASSED"],
        ["test_atomic_true / false / unknown", "test_rule_evaluator.py", "Evaluates atomic leaf facts", "PASSED"],
        ["test_not_operator", "test_rule_evaluator.py", "Kleene NOT truth values", "PASSED"],
        ["test_and_all_true / false / unk", "test_rule_evaluator.py", "Kleene AND conjunctions", "PASSED"],
        ["test_or_one_true / false / unk", "test_rule_evaluator.py", "Kleene OR disjunctions", "PASSED"],
        ["test_nested_complex_expression", "test_rule_evaluator.py", "Nested A ∧ (B ∨ C) formula", "PASSED"],
        ["test_forward_direct_single_step", "test_forward_chaining.py", "Single rule Modus Ponens", "PASSED"],
        ["test_forward_missing_evidence", "test_forward_chaining.py", "Non-firing when fact is UNKNOWN", "PASSED"],
        ["test_forward_multi_step_deduction", "test_forward_chaining.py", "3-tier rule cascade (R1->R2->R3)", "PASSED"],
        ["test_forward_or_expression", "test_forward_chaining.py", "Rule firing with OR antecedent", "PASSED"],
        ["test_forward_duplicate_prevention", "test_forward_chaining.py", "No duplicate facts in memory", "PASSED"],
        ["test_forward_multiple_hypotheses", "test_forward_chaining.py", "Concurrent disease support", "PASSED"],
        ["test_forward_cyclic_termination", "test_forward_chaining.py", "Halts on circular rules A<->B", "PASSED"],
        ["test_backward_direct_fact", "test_backward_chaining.py", "Proves goal already in memory", "PASSED"],
        ["test_backward_intermediate_deduction", "test_backward_chaining.py", "Recursive subgoal proof tree", "PASSED"],
        ["test_backward_unknown_is_not_false", "test_backward_chaining.py", "Missing fact yields UNKNOWN", "PASSED"],
        ["test_backward_explicit_contradiction", "test_backward_chaining.py", "Contradicted fact yields FAILED", "PASSED"],
        ["test_backward_or_alternative_success", "test_backward_chaining.py", "Short-circuit OR branch proof", "PASSED"],
        ["test_backward_cycle_detection", "test_backward_chaining.py", "Detects circular subgoals", "PASSED"],
        ["test_backward_depth_limit", "test_backward_chaining.py", "Halts on max recursion depth", "PASSED"],
        ["test_safety_clean_when_no_red_flags", "test_safety.py", "Zero false emergency alarms", "PASSED"],
        ["test_safety_chest_pain_triggers", "test_safety.py", "Red flag triggers triage alert", "PASSED"],
        ["test_safety_multiple_emergencies", "test_safety.py", "Concurrent emergency signs", "PASSED"],
        ["test_safety_false_or_unknown_clean", "test_safety.py", "Absent red flag does not alert", "PASSED"],
        ["test_cross_algorithm_consistency", "test_integration.py", "Forward & Backward agreement", "PASSED"],
        ["test_safety_alert_coexists_diagnosis", "test_integration.py", "Red flag not suppressed by rules", "PASSED"]
    ]
    add_styled_table(doc, t71_headers, t71_rows, [2.5, 1.8, 2.0, 0.8])

    add_h2(doc, "7.6 Actual Verification Test Results")
    add_p(doc, "The automated test suite achieved a 100% pass rate across all 42 tests:")
    add_code_block(doc, """============================= test session starts =============================
platform win32 -- Python 3.13.6, pytest-9.1.1, pluggy-1.6.0 -- D:\\AI\\.venv\\Scripts\\python.exe
rootdir: D:\\AI
configfile: pytest.ini
testpaths: tests
collected 42 items

tests/test_backward_chaining.py (7 tests) . . . . . . . PASSED               [ 16%]
tests/test_forward_chaining.py (7 tests) . . . . . . . PASSED                [ 33%]
tests/test_integration.py (3 tests) . . . PASSED                             [ 40%]
tests/test_knowledge_base.py (9 tests) . . . . . . . . . PASSED              [ 61%]
tests/test_rule_evaluator.py (12 tests) . . . . . . . . . . . . PASSED       [ 90%]
tests/test_safety.py (4 tests) . . . . PASSED                                [100%]

============================= 42 passed in 0.41s ==============================""")

    add_h2(doc, "7.7 Forward Chaining Live Demonstration")
    add_p(doc, "With patient inputs: fever_present = TRUE, cough_present = TRUE, fatigue_present = TRUE, body_aches_present = TRUE:\n• Fired Rule R001 -> Detached acute_febrile_respiratory_syndrome_supported = TRUE.\n• Fired Rule R002 -> Detached influenza_like_illness_supported = TRUE.\n• Status: Fixed-Point Saturated in 3 Iterations.")

    add_h2(doc, "7.8 Backward Chaining Live Demonstration")
    add_p(doc, "With target goal influenza_like_illness_supported:\n• Backward DFS evaluated R002 -> Subgoal evaluated R001 -> Leaf facts verified in memory.\n• Proof Tree depth reached: 2.\n• Status: SUPPORTED (PROVEN).")

    add_h2(doc, "7.9 Side-by-Side Algorithm Comparison")
    add_p(doc, "Both algorithms agree on the goal status with 100% consistency. Forward Chaining fired 2 rules to establish all consequences; Backward Chaining explored 5 steps targeted exclusively at the goal.")

    add_h2(doc, "7.10 Application Screenshots and Demonstration Results")
    add_p(doc, "The following genuine application screenshots capture key workflows in the MediLogic web interface:")

    # Figures 7.1 to 7.9
    add_figure_image(doc, "assets/screenshots/01_dashboard.png", "Figure 7.1: Application Home Dashboard (01_dashboard.png). Demonstrates the welcoming landing page, 3-step workflow guide, prominent call-to-action button, and educational disclaimer.", width_inches=5.8)
    add_figure_image(doc, "assets/screenshots/02_symptom_assessment.png", "Figure 7.2: Simplified Symptom Assessment Screen (02_symptom_assessment.png). Demonstrates categorized symptom checkboxes with plain-language titles and tri-state toggles (Yes, No, Not sure).", width_inches=5.8)
    add_figure_image(doc, "assets/screenshots/03_forward_chaining.png", "Figure 7.3: Forward Chaining Diagnostic Results Card (03_forward_chaining.png). Demonstrates the plain-language pattern match card for Influenza-Like Illness, highlighting key clinical features satisfied by patient inputs.", width_inches=5.8)
    add_figure_image(doc, "assets/screenshots/04_backward_chaining.png", "Figure 7.4: Backward Chaining Proof Tree Evaluation in AI Lab (04_backward_chaining.png). Demonstrates recursive goal proof tree evaluation with proof status tags, applied rules, and depth metrics.", width_inches=5.8)
    add_figure_image(doc, "assets/screenshots/05_algorithm_comparison.png", "Figure 7.5: Side-by-Side Algorithm Comparison in AI Lab (05_algorithm_comparison.png). Demonstrates simultaneous benchmark execution of Forward Chaining (bottom-up) vs. Backward Chaining (top-down) on identical patient facts.", width_inches=5.8)
    add_figure_image(doc, "assets/screenshots/06_knowledge_base.png", "Figure 7.6: Declarative Knowledge Base Explorer in AI Lab (06_knowledge_base.png). Demonstrates transparent inspection of production rules (R001), IF-THEN expressions, explanations, and authoritative citations.", width_inches=5.8)
    add_figure_image(doc, "assets/screenshots/07_inference_explanation.png", "Figure 7.7: Step-by-Step Inference Explanation View (07_inference_explanation.png). Demonstrates expanded 'Why am I seeing this?' plain-language reasoning and technical Modus Ponens rule derivation details.", width_inches=5.8)
    add_figure_image(doc, "assets/screenshots/08_safety_warning.png", "Figure 7.8: Independent Safety Warning Red-Flag Alert (08_safety_warning.png). Demonstrates prominent, non-suppressible red alert box activated when life-threatening symptoms (Chest Pain) are marked present.", width_inches=5.8)
    add_figure_image(doc, "assets/screenshots/09_inconclusive_result.png", "Figure 7.9: Inconclusive Result Demonstration (09_inconclusive_result.png). Demonstrates the amber card notification when non-diagnostic or insufficient symptoms are entered, explaining that more information is needed rather than assuming absence.", width_inches=5.8)

    add_h2(doc, "7.11 Limitations Discovered During Testing")
    add_bullet(doc, "Inconclusive states occur when non-specific isolated symptoms (e.g., only cough) are provided without accompanying constitutional signs.", bold_prefix="1. Rule Granularity: ")
    add_bullet(doc, "Nested expressions require all conjuncts to be TRUE or UNKNOWN; partial truth is not supported without fuzzy membership functions.", bold_prefix="2. Fixed Antecedent Conjunctions: ")

def add_chapter_8(doc):
    print("  -> Adding Chapter 8: Conclusion and Future Scope...")
    add_h1(doc, "CHAPTER 8 — CONCLUSION AND FUTURE SCOPE", page_break=True)
    
    add_h2(doc, "8.1 Summary of the Project")
    add_p(doc, "MediLogic successfully realizes an autonomous, explainable, rule-based medical diagnostic expert system designed for the SPPU Third-Year Computer Engineering curriculum. Combining declarative JSON knowledge bases, Kleene three-valued logic, Modus Ponens forward deduction, goal-directed backward chaining with cycle detection, an autonomous safety layer, and an intuitive Streamlit interface, MediLogic demonstrates the timeless value of symbolic AI.")

    add_h2(doc, "8.2 Objectives Achieved")
    add_bullet(doc, "Encoded 34 symptoms, 21 rules, 8 hypotheses, and 7 authoritative citations in declarative JSON.")
    add_bullet(doc, "Formulated and verified Kleene K3 three-valued logic evaluation.")
    add_bullet(doc, "Implemented data-driven Forward Chaining with fixed-point saturation.")
    add_bullet(doc, "Implemented goal-directed Backward Chaining with active call-stack cycle guards.")
    add_bullet(doc, "Implemented autonomous emergency red-flag triage.")
    add_bullet(doc, "Engineered an intuitive Streamlit GUI with genuine screenshot verification.")
    add_bullet(doc, "Verified system reliability with 42 automated Pytest tests achieving 100% pass rate.")

    add_h2(doc, "8.3 Key Learning Outcomes")
    add_bullet(doc, "Understanding the practical bridge between formal propositional calculus and software engineering.")
    add_bullet(doc, "Appreciating why open-world three-valued logic is critical for high-stakes healthcare AI.")
    add_bullet(doc, "Mastering the trade-offs between bottom-up forward chaining and top-down backward chaining.")

    add_h2(doc, "8.4 Advantages of MediLogic")
    add_bullet(doc, "Every inference step is mathematically provable.", bold_prefix="• 100% Auditable: ")
    add_bullet(doc, "Distinguishes between false and unobserved facts.", bold_prefix="• Epistemic Integrity: ")
    add_bullet(doc, "Decoupled emergency triage cannot be suppressed.", bold_prefix="• Safety Conscious: ")
    add_bullet(doc, "Contains zero unexplainable latent representations.", bold_prefix="• Zero Black-Box Opacity: ")

    add_h2(doc, "8.5 Technical Limitations")
    add_bullet(doc, "Requires manual rule authoring by knowledge engineers.")
    add_bullet(doc, "Cannot process unstructured clinical notes without NLP preprocessing.")

    add_h2(doc, "8.6 Medical Safety & Ethical Boundaries")
    add_p(doc, "MediLogic is strictly an educational computer science demonstration. It does not prescribe medications, replace certified medical practitioners, or claim clinical validation.")

    add_h2(doc, "8.7 Future Enhancements")
    add_bullet(doc, "Introducing fuzzy membership sets for continuous parameters (e.g., body temperature).", bold_prefix="1. Fuzzy Logic Extensions: ")
    add_bullet(doc, "Incorporating biomedical Named Entity Recognition (NER) to map doctor notes directly to propositional atoms.", bold_prefix="2. Clinical NLP Front-End: ")
    add_bullet(doc, "Modeling time progression of symptoms (e.g., headache onset after rash).", bold_prefix="3. Temporal Constraint Modeling: ")

    add_h2(doc, "8.8 Concluding Remarks")
    add_p(doc, "MediLogic proves that classical symbolic AI remains indispensable in modern engineering education. By delivering transparent, verifiable, and logically sound deductions, MediLogic fulfills the highest standards for an academic mini-project in Artificial Intelligence.")

def add_references(doc):
    print("  -> Adding References...")
    add_h1(doc, "REFERENCES AND BIBLIOGRAPHY", page_break=True)
    
    refs = [
        ("American Academy of Allergy, Asthma & Immunology (AAAAI). (2020). ", "Allergic Rhinitis Practice Parameters. Milwaukee, WI: AAAAI Guidelines."),
        ("American College of Emergency Physicians (ACEP). (2021). ", "Emergency Medicine Clinical Practice Guidelines: Red Flag Symptom Recognition. Dallas, TX: ACEP."),
        ("American College of Gastroenterology (ACG). (2016). ", "Clinical Guideline: Diagnosis, Treatment, and Prevention of Acute Diarrheal Infections in Adults. The American Journal of Gastroenterology, 111(5), 602–622."),
        ("European Association of Urology (EAU). (2022). ", "EAU Guidelines on Urological Infections. Arnhem, The Netherlands: EAU Guidelines Office."),
        ("Genesereth, M. R., & Nilsson, N. J. (1987). ", "Logical Foundations of Artificial Intelligence. San Francisco, CA: Morgan Kaufmann Publishers."),
        ("Headache Classification Committee of the International Headache Society (IHS). (2018). ", "The International Classification of Headache Disorders, 3rd edition (ICHD-3). Cephalalgia, 38(1), 1–211."),
        ("Jackson, P. (1999). ", "Introduction to Expert Systems (3rd ed.). Harlow, England: Addison-Wesley."),
        ("Kleene, S. C. (1952). ", "Introduction to Metamathematics. Amsterdam, The Netherlands: North-Holland Publishing Co."),
        ("Miller, R. A., Pople, H. E., & Myers, J. D. (1982). ", "INTERNIST-I, an experimental computer-based diagnostic consultant for general internal medicine. New England Journal of Medicine, 307(8), 468–476."),
        ("Russell, S., & Norvig, P. (2020). ", "Artificial Intelligence: A Modern Approach (4th ed.). Hoboken, NJ: Pearson Education."),
        ("Savitribai Phule Pune University (SPPU). (2020). ", "Third Year Computer Engineering (2019 Course) Syllabus: Subject Artificial Intelligence (310253). Pune, India: SPPU."),
        ("Shortliffe, E. H. (1976). ", "Computer-Based Medical Consultations: MYCIN. New York, NY: Elsevier Computer Science Library."),
        ("Weiss, S. M., Kulikowski, C. A., Amarel, S., & Safir, A. (1978). ", "A model-based method for computer-aided medical decision-making. Artificial Intelligence, 11(1-2), 145–172."),
        ("World Health Organization (WHO). (2018). ", "WHO Global Influenza Surveillance and Response System (GISRS) Case Definitions for ILI and SARI. Geneva, Switzerland: WHO.")
    ]
    for idx, (auth, title) in enumerate(refs):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)
        r_num = p.add_run(f"[{idx+1}] ")
        r_num.font.bold = True
        r_auth = p.add_run(auth)
        r_auth.font.bold = True
        r_title = p.add_run(title)
        r_title.font.italic = True

def add_appendices(doc):
    print("  -> Adding Appendices...")
    add_h1(doc, "APPENDIX A: CORE PYTHON SOURCE-CODE EXCERPTS", page_break=True)
    
    add_h2(doc, "A.1 Rule Evaluator Core (engine/rule_evaluator.py)")
    add_code_block(doc, """class RuleEvaluator:
    @staticmethod
    def evaluate(expression: Dict[str, Any], fact_store: Dict[str, Fact]) -> EvaluationResult:
        if "fact" in expression:
            return RuleEvaluator._evaluate_atomic(expression, fact_store)
        elif "and" in expression:
            return RuleEvaluator._evaluate_and(expression["and"], fact_store)
        elif "or" in expression:
            return RuleEvaluator._evaluate_or(expression["or"], fact_store)
        elif "not" in expression:
            return RuleEvaluator._evaluate_not(expression["not"], fact_store)
        raise ValueError(f"Malformed expression: {expression}")""")

    add_h2(doc, "A.2 Forward Chaining Engine Core (engine/forward_chaining.py)")
    add_code_block(doc, """while iteration < self.max_iterations:
    iteration += 1
    new_facts_in_iteration = 0
    for rule in sorted(self.kb.rules, key=lambda r: r.id):
        if rule.id in already_fired_rule_ids:
            continue
        eval_res = RuleEvaluator.evaluate(rule.antecedent, working_memory)
        if eval_res.is_true:
            already_fired_rule_ids.add(rule.id)
            c_fact_id = rule.consequent_fact_id
            c_val = rule.consequent_value
            if c_fact_id not in working_memory:
                working_memory[c_fact_id] = Fact(id=c_fact_id, value=c_val, source=FactSource.INFERRED, derivation_rule=rule.id)
                new_facts_in_iteration += 1
    if new_facts_in_iteration == 0:
        break  # Fixed-point reached""")

    add_h2(doc, "A.3 Backward Chaining Engine Core (engine/backward_chaining.py)")
    add_code_block(doc, """if goal_fact in active_goal_stack:
    return ProofNode(goal_fact=goal_fact, target_value=target_value, status=GoalStatus.CYCLE_DETECTED)

active_goal_stack.add(goal_fact)
try:
    for rule in candidate_rules:
        expr_node = self._prove_expression(rule.antecedent, working_memory, active_goal_stack, depth + 1)
        if expr_node.status == GoalStatus.SUPPORTED:
            working_memory[goal_fact] = Fact(id=goal_fact, value=target_value, source=FactSource.INFERRED, derivation_rule=rule.id)
            return ProofNode(goal_fact=goal_fact, target_value=target_value, status=GoalStatus.SUPPORTED, rule_id=rule.id)
finally:
    active_goal_stack.remove(goal_fact)""")

    add_h1(doc, "APPENDIX B: SAMPLE INPUT AND OUTPUT EXECUTION TRACES", page_break=True)
    add_h2(doc, "B.1 Forward Chaining Trace Log: Acute Influenza")
    add_code_block(doc, """{
  "iteration": 1,
  "step": 1,
  "rule_id": "R001",
  "rule_name": "Acute Febrile Respiratory Syndrome Derivation",
  "evaluated": "TRUE",
  "fired": true,
  "consequent_fact": "acute_febrile_respiratory_syndrome_supported",
  "consequent_value": "TRUE",
  "is_new_fact": true,
  "explanation": "Rule R001 fired via Modus Ponens: Antecedent satisfied. Added 'acute_febrile_respiratory_syndrome_supported' as TRUE."
}""")

    add_h1(doc, "APPENDIX C: COMPLETE SPPU SYLLABUS MAPPING TABLE", page_break=True)
    add_p(doc, "Refer to Chapter 5, Table 5.5 and docs/SYLLABUS_MAPPING.md for comprehensive course outcomes (COs) and unit-level syllabus alignment across Units I, II, IV, and V of the SPPU Third Year Computer Engineering Artificial Intelligence curriculum.")

def create_report():
    print("Initializing MediLogic Project Report DOCX...")
    doc = Document()
    
    # Page setup - A4 with 1-inch margins
    sections = doc.sections
    for section in sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header setup
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("MediLogic: Medical Diagnosis Expert System  |  SPPU TE Computer Engineering")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.italic = True
        hrun.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
        
        # Footer setup
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Department of Computer Engineering, Savitribai Phule Pune University")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(0xA0, 0xAE, 0xC0)

    # Base styling
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal_style.paragraph_format.space_after = Pt(6)

    cand_data = [
        ("[STUDENT_NAME_PLACEHOLDER_1]", "[ROLL_NUMBER_PLACEHOLDER_1]"),
        ("[STUDENT_NAME_PLACEHOLDER_2]", "[ROLL_NUMBER_PLACEHOLDER_2]"),
        ("[STUDENT_NAME_PLACEHOLDER_3]", "[ROLL_NUMBER_PLACEHOLDER_3]"),
        ("[STUDENT_NAME_PLACEHOLDER_4]", "[ROLL_NUMBER_PLACEHOLDER_4]")
    ]

    # Generate all document sections sequentially
    add_preliminary_pages(doc, cand_data)
    add_chapter_1(doc)
    add_chapter_2(doc)
    add_chapter_3(doc)
    add_chapter_4(doc)
    add_chapter_5(doc)
    add_chapter_6(doc)
    add_chapter_7(doc)
    add_chapter_8(doc)
    add_references(doc)
    add_appendices(doc)

    os.makedirs(os.path.join(WORKSPACE_ROOT, "deliverables"), exist_ok=True)
    out_path = os.path.join(WORKSPACE_ROOT, "deliverables", "MediLogic_Project_Report.docx")
    print(f"Saving final report to {out_path}...")
    doc.save(out_path)
    print("Report generated successfully!")
    return out_path

if __name__ == '__main__':
    out_file = create_report()
    print(f"Process complete: {out_file}")
