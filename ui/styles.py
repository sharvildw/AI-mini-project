"""Modern, Friendly, and Clean Healthcare-Themed Visual Styles for MediLogic.

Palette:
- Background: #F8FAFC (clean light slate), Cards: #FFFFFF
- Primary Brand: #0F766E, #0D9488 (Soft Teal)
- Primary Navy: #0F172A, #1E293B, #334155 (Text and Accents)
- Secondary Light: #F1F5F9, #E2E8F0 (Borders and surfaces)
- Success Green: #10B981, #ECFDF5
- Warning Amber: #F59E0B, #FFFBEB
- Emergency Alert: #EF4444, #FEF2F2
"""

def get_custom_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1E293B;
    }

    /* Main Container Clean Spacing */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3.5rem;
        max-width: 1080px;
    }

    /* Modern Simple Hero Card */
    .simple-hero {
        background: linear-gradient(135deg, #0F766E 0%, #115E59 100%);
        color: #FFFFFF;
        padding: 2.2rem 2.4rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px -2px rgba(15, 118, 110, 0.2);
        margin-bottom: 1.8rem;
    }

    .simple-hero h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .simple-hero p {
        color: #CCFBF1 !important;
        font-size: 1.1rem;
        margin-bottom: 0;
        line-height: 1.5;
        max-width: 720px;
    }

    /* Simple Step Cards on Home */
    .steps-container {
        display: flex;
        gap: 1.2rem;
        margin: 1.8rem 0;
        flex-wrap: wrap;
    }

    .step-card {
        flex: 1;
        min-width: 240px;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        text-align: left;
    }

    .step-card .step-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        background: #E6FFFA;
        color: #0F766E;
        font-weight: 800;
        font-size: 1rem;
        border-radius: 10px;
        margin-bottom: 0.8rem;
    }

    .step-card h3 {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0 0 0.4rem 0;
    }

    .step-card p {
        font-size: 0.92rem;
        color: #64748B;
        line-height: 1.45;
        margin: 0;
    }

    /* Emergency Alert Box */
    .simple-emergency-banner {
        background: #FEF2F2;
        border: 1px solid #FCA5A5;
        border-left: 6px solid #DC2626;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.6rem;
        color: #991B1B;
    }

    .simple-emergency-banner h3 {
        color: #991B1B !important;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .simple-emergency-banner ul {
        margin: 0.4rem 0 0.6rem 1.2rem;
        padding: 0;
        font-size: 0.95rem;
        color: #7F1D1D;
    }

    .simple-emergency-banner .callout-tel {
        font-size: 0.95rem;
        font-weight: 700;
        color: #B91C1C;
        margin-top: 0.5rem;
    }

    /* Friendly Educational Notice */
    .simple-disclaimer {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 0.85rem 1.1rem;
        font-size: 0.85rem;
        color: #64748B;
        margin-bottom: 1.5rem;
        line-height: 1.4;
    }

    /* Clean Result Cards */
    .result-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    }

    .result-card-supported {
        border-left: 6px solid #0D9488;
    }

    .result-card h3 {
        color: #0F172A;
        font-size: 1.25rem;
        font-weight: 700;
        margin: 0 0 0.4rem 0;
    }

    .result-card .badge-match {
        display: inline-block;
        background: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
        padding: 0.2rem 0.65rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }

    /* Clean Badges */
    .tag-pill {
        display: inline-block;
        background: #F1F5F9;
        color: #334155;
        border: 1px solid #E2E8F0;
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 0.2rem 0.3rem 0.2rem 0;
    }

    .tag-pill-active {
        background: #CCFBF1;
        color: #0F766E;
        border-color: #99F6E4;
        font-weight: 600;
    }

    /* Friendly Symptom Row Card */
    .symptom-row {
        background: #FFFFFF;
        border: 1px solid #F1F5F9;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        transition: background 0.15s ease;
    }

    .symptom-row:hover {
        background: #F8FAFC;
    }

    /* Clean Card Container */
    .simple-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 1.2rem;
    }

    /* Code Box for Technical Details in AI Lab */
    .tech-box {
        background: #0F172A;
        color: #38BDF8;
        font-family: 'JetBrains Mono', monospace;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        font-size: 0.83rem;
        margin: 0.5rem 0;
        overflow-x: auto;
    }

    /* Clean Sidebar Styling */
    div[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    div[data-testid="stSidebar"] * {
        color: #1E293B !important;
    }
    div[data-testid="stSidebar"] .stRadio label span {
        font-size: 0.95rem;
        font-weight: 500;
    }

    /* Button Enhancements */
    button[kind="primary"] {
        background-color: #0F766E !important;
        border-color: #0F766E !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 0.45rem 1.2rem !important;
    }
    button[kind="primary"]:hover {
        background-color: #115E59 !important;
        border-color: #115E59 !important;
    }

    button[kind="secondary"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        color: #334155 !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
    }
    button[kind="secondary"]:hover {
        background-color: #F1F5F9 !important;
        border-color: #94A3B8 !important;
    }
    </style>
    """
