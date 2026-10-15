# MediLogic: Annotated Bibliography & References

This document records the authoritative academic computer science literature and clinical diagnostic reference standards underpinning MediLogic.

---

## 1. Artificial Intelligence & Logical Formalisms Literature

1. **Russell, S., & Norvig, P. (2020).**  
   *Artificial Intelligence: A Modern Approach (4th ed.)*. Pearson.  
   - **Chapter 7:** Logical Agents (Knowledge-Based Agents, Propositional Logic, Syntax, Semantics, Modus Ponens, Resolution).  
   - **Chapter 9:** Inference in First-Order Logic (Forward Chaining, Backward Chaining, Fixed-Point Saturation).  
   - **Annotation:** Serves as the authoritative academic foundation for the syllabus alignment of Unit IV and Unit I.

2. **Shortliffe, E. H. (1976).**  
   *Computer-Based Medical Consultations: MYCIN*. New York: Elsevier Computer Science Library.  
   - **Annotation:** The landmark doctoral dissertation and book introducing rule-based expert systems to clinical medicine. Provided the blueprint for separating the declarative knowledge base from the inference engine and generating step-by-step audit explanations.

3. **Kleene, S. C. (1952).**  
   *Introduction to Metamathematics*. Amsterdam: North-Holland Publishing Co.  
   - **Section 64:** Strong 3-Valued Logic ($K_3$).  
   - **Annotation:** Defines the formal mathematical semantics of three-valued logic (True, False, Undetermined) implemented in `engine/rule_evaluator.py`.

4. **Genesereth, M. R., & Nilsson, N. J. (1987).**  
   *Logical Foundations of Artificial Intelligence*. Morgan Kaufmann Publishers.  
   - **Annotation:** Theoretical treatment of declarative representations, production systems, and goal-directed backward deduction.

---

## 2. Authoritative Clinical Diagnostic Guidelines

All clinical symptom patterns in MediLogic are derived directly from published guidelines issued by authoritative public health agencies and professional medical societies:

5. **World Health Organization (WHO). (2018).**  
   *WHO Global Influenza Surveillance and Response System (GISRS) Case Definitions for ILI and SARI*.  
   - **URL:** [https://www.who.int/teams/global-influenza-programme/surveillance-and-monitoring](https://www.who.int/teams/global-influenza-programme/surveillance-and-monitoring)  
   - **Clinical Standard:** Acute respiratory infection with measured fever $\ge 38^\circ\text{C}$ and cough, with onset within the last 10 days. Codified in rules `R001`, `R002`, `R003`, and `R004`.

6. **Centers for Disease Control and Prevention (CDC). (2023).**  
   *Common Colds: Protect Yourself and Others*.  
   - **URL:** [https://www.cdc.gov/antibiotic-use/common-cold.html](https://www.cdc.gov/antibiotic-use/common-cold.html)  
   - **Clinical Standard:** Upper respiratory tract infection presentation featuring nasal congestion, pharyngitis, sneezing, and low-grade or absent fever. Codified in rules `R005`, `R006`, and `R007`.

7. **American Academy of Allergy, Asthma & Immunology (AAAAI). (2020).**  
   *Allergic Rhinitis Practice Parameters*.  
   - **URL:** [https://www.aaaai.org/conditions-treatments/allergies/allergic-rhinitis](https://www.aaaai.org/conditions-treatments/allergies/allergic-rhinitis)  
   - **Clinical Standard:** IgE-mediated nasal mucosal inflammation manifesting as paroxysmal sneezing, watery rhinorrhea, and conjunctival pruritus without fever. Codified in rules `R008`, `R009`, and `R010`.

8. **Headache Classification Committee of the International Headache Society (IHS). (2018).**  
   *The International Classification of Headache Disorders, 3rd edition (ICHD-3)*. *Cephalalgia*, 38(1), 1–211.  
   - **URL:** [https://ichd-3.org/1-migraine/](https://ichd-3.org/1-migraine/)  
   - **Clinical Standard:** Diagnostic criteria for migraine without aura: unilateral, pulsating, moderate/severe cranial pain aggravated by routine activity, accompanied by photophobia, phonophobia, or nausea. Codified in rules `R011`, `R012`, `R013`, and `R014`.

9. **American College of Gastroenterology (ACG). (2016).**  
   *ACG Clinical Guideline: Diagnosis, Treatment, and Prevention of Acute Diarrheal Infections in Adults*. *The American Journal of Gastroenterology*, 111(5), 602–622.  
   - **URL:** [https://gi.org/guidelines/clinical-guideline-acute-diarrheal-infections-in-adults/](https://gi.org/guidelines/clinical-guideline-acute-diarrheal-infections-in-adults/)  
   - **Clinical Standard:** Rapid-onset diarrhea accompanied by nausea, vomiting, and abdominal cramping. Codified in rules `R015`, `R016`, and `R017`.

10. **European Association of Urology (EAU). (2022).**  
    *EAU Guidelines on Urological Infections*.  
    - **URL:** [https://uroweb.org/guidelines/urological-infections](https://uroweb.org/guidelines/urological-infections)  
    - **Clinical Standard:** Diagnostic criteria for uncomplicated cystitis (dysuria, frequency, urgency) and ascending pyelonephritis (flank pain, high fever). Codified in rules `R018`, `R019`, `R020`, and `R021`.

11. **American College of Emergency Physicians (ACEP). (2021).**  
    *Emergency Medicine Clinical Practice Guidelines: Red Flag Symptom Recognition*.  
    - **URL:** [https://www.acep.org/](https://www.acep.org/)  
    - **Clinical Standard:** Critical triage criteria defining acute life threats (crushing chest pain, severe dyspnea, acute neurological deficits, meningeal signs, acute surgical abdomen). Codified in `engine/safety.py`.
