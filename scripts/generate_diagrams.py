import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('assets/diagrams', exist_ok=True)

def generate_forward_chaining_flowchart():
    fig, ax = plt.subplots(figsize=(8, 10), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 97, 'Forward Chaining Algorithm Flowchart', ha='center', va='center', fontsize=13, fontweight='bold', color='#1A365D')

    steps = [
        ('Start: Initialize Working Memory with Patient Facts', 50, 90, 80, 5, '#EBF8FF', '#3182CE', 'rect'),
        ('Load Rules R from Knowledge Base (Flag Unfired)', 50, 81, 75, 5, '#EDF2F7', '#4A5568', 'rect'),
        ('Pass Loop: Set new_inferences = False', 50, 72, 65, 5, '#EDF2F7', '#4A5568', 'rect'),
        ('For each unfired rule r in R', 50, 63, 60, 5, '#EDF2F7', '#4A5568', 'rect'),
        ('Evaluate Antecedent(r) under Kleene K3 Logic', 50, 54, 70, 5, '#FEFCBF', '#D69E2E', 'rect'),
        ('Antecedent == TRUE ?', 50, 44, 45, 6, '#FFF5F5', '#E53E3E', 'diamond'),
        ('Fire Rule: Apply Modus Ponens (Working Memory += Consequent)', 50, 32, 80, 5, '#F0FFF4', '#38A169', 'rect'),
        ('Mark r as Fired; Log Trace; new_inferences = True', 50, 23, 75, 5, '#FAF5FF', '#805AD5', 'rect'),
        ('new_inferences == True ?', 50, 13, 45, 6, '#FFF5F5', '#E53E3E', 'diamond'),
        ('Stop: Return Working Memory, Derived Conditions & Trace Log', 50, 4, 80, 5, '#C6F6D5', '#22543D', 'rect')
    ]

    for title, cx, cy, w, h, bg, border, shape in steps:
        if shape == 'rect':
            box = patches.FancyBboxPatch((cx - w/2, cy - h/2), w, h, boxstyle='round,pad=0.5', facecolor=bg, edgecolor=border, linewidth=1.5)
            ax.add_patch(box)
            ax.text(cx, cy, title, ha='center', va='center', fontsize=8, fontweight='bold', color='#2D3748')
        elif shape == 'diamond':
            poly = patches.Polygon([[cx, cy + h/2], [cx + w/2, cy], [cx, cy - h/2], [cx - w/2, cy]], closed=True, facecolor=bg, edgecolor=border, linewidth=1.5)
            ax.add_patch(poly)
            ax.text(cx, cy, title, ha='center', va='center', fontsize=8, fontweight='bold', color='#742A2A')

    # Connecting arrows
    ax.annotate('', xy=(50, 84), xytext=(50, 87), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))
    ax.annotate('', xy=(50, 75), xytext=(50, 78), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))
    ax.annotate('', xy=(50, 66), xytext=(50, 69), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))
    ax.annotate('', xy=(50, 57), xytext=(50, 60), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))
    ax.annotate('', xy=(50, 48), xytext=(50, 51), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))
    
    # Diamond 1: YES -> Fire rule (down)
    ax.annotate('', xy=(50, 35), xytext=(50, 41), arrowprops=dict(arrowstyle='->', lw=1.5, color='#2F855A'))
    ax.text(53, 38, 'YES', fontsize=8, fontweight='bold', color='#2F855A')
    
    # Diamond 1: NO -> Loop to next rule (side)
    ax.annotate('', xy=(20, 63), xytext=(27, 44), arrowprops=dict(arrowstyle='->', lw=1.2, color='#C53030', connectionstyle='angle,angleA=0,angleB=90,rad=5'))
    ax.text(23, 46, 'NO', fontsize=8, fontweight='bold', color='#C53030')

    ax.annotate('', xy=(50, 26), xytext=(50, 29), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))
    ax.annotate('', xy=(50, 17), xytext=(50, 20), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))

    # Diamond 2: YES -> Repeat pass (loop back to pass loop)
    ax.annotate('', xy=(12, 72), xytext=(27, 13), arrowprops=dict(arrowstyle='->', lw=1.2, color='#2F855A', connectionstyle='angle,angleA=0,angleB=90,rad=8'))
    ax.text(14, 40, 'YES (Repeat Pass)', fontsize=8, fontweight='bold', color='#2F855A')

    # Diamond 2: NO -> Stop
    ax.annotate('', xy=(50, 7), xytext=(50, 10), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))
    ax.text(53, 8.5, 'NO (Fixed Point)', fontsize=8, fontweight='bold', color='#742A2A')

    plt.tight_layout()
    plt.savefig('assets/diagrams/forward_chaining_flowchart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Generated forward_chaining_flowchart.png')

def generate_backward_chaining_flowchart():
    fig, ax = plt.subplots(figsize=(8, 10), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 97, 'Backward Chaining (Goal-Directed DFS) Flowchart', ha='center', va='center', fontsize=13, fontweight='bold', color='#1A365D')

    steps = [
        ('Start: evaluate_goal(goal_id, visited_goals)', 50, 91, 75, 5, '#EBF8FF', '#3182CE', 'rect'),
        ('Is goal_id in visited_goals ? (Active Stack Check)', 50, 82, 70, 5, '#FEFCBF', '#D69E2E', 'rect'),
        ('Cycle Detected ?', 50, 73, 40, 5.5, '#FFF5F5', '#E53E3E', 'diamond'),
        ('Return ProofNode(status=FAIL, reason=CYCLE)', 82, 64, 34, 5, '#FED7D7', '#9B2C2C', 'rect'),
        ('Is goal_id already known in Working Memory ?', 50, 63, 68, 5, '#FEFCBF', '#D69E2E', 'rect'),
        ('Return ProofNode(status=VERIFIED, source=FACT)', 82, 54, 34, 5, '#C6F6D5', '#22543D', 'rect'),
        ('Find rules concluding goal_id in KB', 50, 53, 60, 5, '#EDF2F7', '#4A5568', 'rect'),
        ('Are there concluding rules ?', 50, 44, 45, 5.5, '#FFF5F5', '#E53E3E', 'diamond'),
        ('For each rule r: Recursively evaluate sub-goals', 50, 33, 70, 5, '#FAF5FF', '#805AD5', 'rect'),
        ('Can antecedent of r be proven TRUE ?', 50, 23, 55, 5.5, '#FFF5F5', '#E53E3E', 'diamond'),
        ('Goal Proven: Return ProofNode(status=VERIFIED)', 25, 12, 45, 5, '#C6F6D5', '#22543D', 'rect'),
        ('Goal Unproven: Return ProofNode(status=FAIL)', 75, 12, 45, 5, '#FED7D7', '#9B2C2C', 'rect')
    ]

    for title, cx, cy, w, h, bg, border, shape in steps:
        if shape == 'rect':
            box = patches.FancyBboxPatch((cx - w/2, cy - h/2), w, h, boxstyle='round,pad=0.5', facecolor=bg, edgecolor=border, linewidth=1.5)
            ax.add_patch(box)
            ax.text(cx, cy, title, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#2D3748')
        elif shape == 'diamond':
            poly = patches.Polygon([[cx, cy + h/2], [cx + w/2, cy], [cx, cy - h/2], [cx - w/2, cy]], closed=True, facecolor=bg, edgecolor=border, linewidth=1.5)
            ax.add_patch(poly)
            ax.text(cx, cy, title, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#742A2A')

    # Arrows
    ax.annotate('', xy=(50, 85), xytext=(50, 88), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))
    ax.annotate('', xy=(50, 76), xytext=(50, 79), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))
    
    # Cycle diamond
    ax.annotate('', xy=(65, 64), xytext=(70, 73), arrowprops=dict(arrowstyle='->', lw=1.3, color='#C53030'))
    ax.text(72, 71, 'YES', fontsize=8, fontweight='bold', color='#C53030')
    ax.annotate('', xy=(50, 66), xytext=(50, 70), arrowprops=dict(arrowstyle='->', lw=1.5, color='#2F855A'))
    ax.text(52, 68, 'NO', fontsize=8, fontweight='bold', color='#2F855A')

    # Fact check
    ax.annotate('', xy=(65, 54), xytext=(68, 63), arrowprops=dict(arrowstyle='->', lw=1.3, color='#2F855A'))
    ax.text(71, 60, 'YES', fontsize=8, fontweight='bold', color='#2F855A')
    ax.annotate('', xy=(50, 56), xytext=(50, 60), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))
    ax.text(52, 58, 'NO', fontsize=8, fontweight='bold', color='#4A5568')

    # Rule search
    ax.annotate('', xy=(50, 47), xytext=(50, 50), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))
    
    # Are rules available?
    ax.annotate('', xy=(50, 36), xytext=(50, 41), arrowprops=dict(arrowstyle='->', lw=1.5, color='#2F855A'))
    ax.text(52, 38, 'YES', fontsize=8, fontweight='bold', color='#2F855A')
    ax.annotate('', xy=(75, 15), xytext=(70, 44), arrowprops=dict(arrowstyle='->', lw=1.3, color='#C53030', connectionstyle='angle,angleA=0,angleB=90,rad=5'))
    ax.text(73, 30, 'NO', fontsize=8, fontweight='bold', color='#C53030')

    # Recursive check
    ax.annotate('', xy=(50, 26), xytext=(50, 30), arrowprops=dict(arrowstyle='->', lw=1.5, color='#4A5568'))
    
    # Can antecedent be proven?
    ax.annotate('', xy=(25, 15), xytext=(35, 23), arrowprops=dict(arrowstyle='->', lw=1.5, color='#2F855A'))
    ax.text(26, 21, 'YES (Success)', fontsize=8, fontweight='bold', color='#2F855A')
    ax.annotate('', xy=(70, 15), xytext=(65, 23), arrowprops=dict(arrowstyle='->', lw=1.5, color='#C53030'))
    ax.text(68, 21, 'NO (Next/Fail)', fontsize=8, fontweight='bold', color='#C53030')

    plt.tight_layout()
    plt.savefig('assets/diagrams/backward_chaining_flowchart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Generated backward_chaining_flowchart.png')

def generate_dfd():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, 'MediLogic Data Flow Diagram (DFD Level 1)', ha='center', va='center', fontsize=13, fontweight='bold', color='#1A365D')

    # External Entity User
    user_box = patches.FancyBboxPatch((4, 45), 16, 25, boxstyle='square,pad=0', facecolor='#E2E8F0', edgecolor='#2D3748', linewidth=2)
    ax.add_patch(user_box)
    ax.text(12, 57.5, 'User / Patient\n(External Entity)', ha='center', va='center', fontsize=9, fontweight='bold', color='#1A202C')

    # Process 1.0
    p1 = patches.Circle((36, 68), 9, facecolor='#EBF8FF', edgecolor='#3182CE', linewidth=2)
    ax.add_patch(p1)
    ax.text(36, 68, '1.0\nSymptom\nInput', ha='center', va='center', fontsize=8, fontweight='bold', color='#2B6CB0')

    # Process 2.0 (Safety)
    p2 = patches.Circle((36, 32), 9, facecolor='#FFF5F5', edgecolor='#E53E3E', linewidth=2)
    ax.add_patch(p2)
    ax.text(36, 32, '2.0\nEmergency\nSafety Check', ha='center', va='center', fontsize=8, fontweight='bold', color='#C53030')

    # Process 3.0 (Inference Engine)
    p3 = patches.Circle((68, 68), 9, facecolor='#FAF5FF', edgecolor='#805AD5', linewidth=2)
    ax.add_patch(p3)
    ax.text(68, 68, '3.0\nRule\nEvaluation\n& Chaining', ha='center', va='center', fontsize=8, fontweight='bold', color='#6B46C1')

    # Process 4.0 (Explanation)
    p4 = patches.Circle((68, 32), 9, facecolor='#F0FFF4', edgecolor='#38A169', linewidth=2)
    ax.add_patch(p4)
    ax.text(4.0, 32, '', ha='center', va='center')
    ax.text(68, 32, '4.0\nExplanation\nFacility', ha='center', va='center', fontsize=8, fontweight='bold', color='#276749')

    # Data Store D1: Knowledge Base
    d1 = patches.FancyBboxPatch((86, 48), 12, 22, boxstyle='round,pad=0.2', facecolor='#FEFCBF', edgecolor='#D69E2E', linewidth=2)
    ax.add_patch(d1)
    ax.text(92, 59, 'D1: Rules\n& Conditions\n(JSON KB)', ha='center', va='center', fontsize=8, fontweight='bold', color='#744210')

    # Flows
    ax.annotate('Selected Symptoms', xy=(27, 68), xytext=(20, 60), arrowprops=dict(arrowstyle='->', lw=1.3, color='#2B6CB0'), fontsize=7)
    ax.annotate('Emergency Flag', xy=(20, 48), xytext=(27, 32), arrowprops=dict(arrowstyle='<-', lw=1.3, color='#C53030'), fontsize=7)
    ax.annotate('Working Memory Facts', xy=(59, 68), xytext=(45, 68), arrowprops=dict(arrowstyle='->', lw=1.3, color='#4A5568'), fontsize=7)
    ax.annotate('Production Rules', xy=(77, 68), xytext=(86, 68), arrowprops=dict(arrowstyle='<-', lw=1.3, color='#D69E2E'), fontsize=7)
    ax.annotate('Firing Trace', xy=(68, 41), xytext=(68, 59), arrowprops=dict(arrowstyle='->', lw=1.3, color='#4A5568'), fontsize=7)
    ax.annotate('Verified Diagnoses & Proof', xy=(18, 54), xytext=(59, 32), arrowprops=dict(arrowstyle='->', lw=1.3, color='#276749', connectionstyle='arc3,rad=-0.2'), fontsize=7)

    plt.tight_layout()
    plt.savefig('assets/diagrams/dfd.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Generated dfd.png')

def generate_use_case():
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, 'MediLogic Use Case Diagram', ha='center', va='center', fontsize=13, fontweight='bold', color='#1A365D')

    # Boundary Box
    bound = patches.FancyBboxPatch((28, 5), 68, 86, boxstyle='round,pad=1', facecolor='#F7FAFC', edgecolor='#4A5568', linewidth=1.5)
    ax.add_patch(bound)
    ax.text(62, 88, 'MediLogic System Boundary', ha='center', va='center', fontsize=10, fontweight='bold', color='#4A5568')

    # Actor: User / Student
    ax.text(12, 60, '옷\nPatient / Student\n(Actor)', ha='center', va='center', fontsize=11, fontweight='bold', color='#1A202C')

    # Use Cases
    cases = [
        ('UC1: Select Symptoms (Tri-State)', 62, 75, 45, 8, '#EBF8FF', '#3182CE'),
        ('UC2: Trigger Forward Diagnosis', 62, 61, 45, 8, '#FAF5FF', '#805AD5'),
        ('UC3: Run Backward Goal Verification', 62, 47, 45, 8, '#FFFAF0', '#DD6B20'),
        ('UC4: View Step-by-Step Explanation', 62, 33, 45, 8, '#F0FFF4', '#38A169'),
        ('UC5: Inspect Knowledge Base Rules', 62, 19, 45, 8, '#FEFCBF', '#D69E2E')
    ]

    for title, cx, cy, w, h, bg, border in cases:
        ellipse = patches.Ellipse((cx, cy), w, h, facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(ellipse)
        ax.text(cx, cy, title, ha='center', va='center', fontsize=8, fontweight='bold', color='#2D3748')
        # Line from actor
        ax.plot([18, cx - w/2], [58, cy], color='#718096', lw=1.2)

    plt.tight_layout()
    plt.savefig('assets/diagrams/use_case.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Generated use_case.png')

def generate_rule_dependency():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, 'Knowledge Base Rule Dependency Lattice', ha='center', va='center', fontsize=13, fontweight='bold', color='#1A365D')

    # Layer 1: Primitive Symptoms (Leaves)
    ax.text(15, 88, 'Layer 1: Observable Symptoms', ha='center', va='center', fontsize=9, fontweight='bold', color='#2B6CB0')
    syms = [
        ('fever', 15, 78), ('cough', 15, 68), ('fatigue', 15, 58),
        ('chills', 15, 48), ('headache', 15, 38), ('chest_pain', 15, 28),
        ('shortness_of_breath', 15, 18), ('sneezing', 15, 8)
    ]
    for name, x, y in syms:
        box = patches.FancyBboxPatch((x-10, y-3), 20, 6, boxstyle='round,pad=0.3', facecolor='#EBF8FF', edgecolor='#3182CE', linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=7.5, color='#1A365D')

    # Layer 2: Intermediate Clinical Findings
    ax.text(50, 88, 'Layer 2: Intermediate Findings', ha='center', va='center', fontsize=9, fontweight='bold', color='#805AD5')
    inter = [
        ('influenza_like_illness', 50, 68),
        ('upper_respiratory_syndrome', 50, 50),
        ('acute_bronchitis_syndrome', 50, 32),
        ('gastroenteritis_syndrome', 50, 14)
    ]
    for name, x, y in inter:
        box = patches.FancyBboxPatch((x-14, y-4), 28, 8, boxstyle='round,pad=0.4', facecolor='#FAF5FF', edgecolor='#805AD5', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#44337A')

    # Layer 3: Terminal Diagnoses (Roots)
    ax.text(85, 88, 'Layer 3: Diagnostic Conclusions', ha='center', va='center', fontsize=9, fontweight='bold', color='#276749')
    diag = [
        ('influenza', 85, 70),
        ('common_cold', 85, 52),
        ('allergic_rhinitis', 85, 34),
        ('pneumonia_suspect', 85, 16)
    ]
    for name, x, y in diag:
        box = patches.FancyBboxPatch((x-12, y-4), 24, 8, boxstyle='round,pad=0.4', facecolor='#F0FFF4', edgecolor='#38A169', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold', color='#1C4532')

    # Arrows from Layer 1 to Layer 2
    ax.annotate('', xy=(36, 68), xytext=(25, 78), arrowprops=dict(arrowstyle='->', lw=1, color='#718096'))
    ax.annotate('', xy=(36, 68), xytext=(25, 68), arrowprops=dict(arrowstyle='->', lw=1, color='#718096'))
    ax.annotate('', xy=(36, 68), xytext=(25, 58), arrowprops=dict(arrowstyle='->', lw=1, color='#718096'))
    ax.annotate('', xy=(36, 50), xytext=(25, 38), arrowprops=dict(arrowstyle='->', lw=1, color='#718096'))
    ax.annotate('', xy=(36, 50), xytext=(25, 8), arrowprops=dict(arrowstyle='->', lw=1, color='#718096'))

    # Arrows from Layer 2 to Layer 3
    ax.annotate('R001', xy=(73, 70), xytext=(64, 68), arrowprops=dict(arrowstyle='->', lw=1.2, color='#2F855A'), fontsize=7, color='#2F855A', fontweight='bold')
    ax.annotate('R002', xy=(73, 52), xytext=(64, 50), arrowprops=dict(arrowstyle='->', lw=1.2, color='#2F855A'), fontsize=7, color='#2F855A', fontweight='bold')
    ax.annotate('R005', xy=(73, 16), xytext=(64, 32), arrowprops=dict(arrowstyle='->', lw=1.2, color='#C53030'), fontsize=7, color='#C53030', fontweight='bold')

    plt.tight_layout()
    plt.savefig('assets/diagrams/rule_dependency.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Generated rule_dependency.png')

if __name__ == '__main__':
    generate_forward_chaining_flowchart()
    generate_backward_chaining_flowchart()
    generate_dfd()
    generate_use_case()
    generate_rule_dependency()
    print('All diagrams generated in assets/diagrams/')
