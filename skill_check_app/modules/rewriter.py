import os
from typing import List
from skill_check_app.modules.llm_switcher import call_model


# ======================================================
# Load HTML Resume Template
# ======================================================
def load_template(template_name: str) -> str:
    """
    Loads an HTML template from: skill_check_app/templates/<template>.html
    Template must contain {{CONTENT}} placeholder.
    """
    template_path = os.path.join("skill_check_app", "templates", f"{template_name}.html")

    if not os.path.exists(template_path):
        # fallback: no wrapper, only raw content
        return "{{CONTENT}}"

    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()



# ======================================================
# Build LLM Prompt for HTML Resume Content
# ======================================================
def build_full_rewrite_html_prompt(
    resume_text: str,
    jd_text: str,
    matched_skills: List[str],
    missing_skills: List[str],
    similarity_score: float
) -> str:
    """
    Use RAPTOR prompting framework + HTML layout guidance.
    LLM produces only the resume inner content (without <html>, <head>, <body>).
    """

    prompt = f"""
You are **RAPTOR-ResumeWriter**, an expert resume writer and HTML resume designer.

Your job is to completely rewrite the RESUME into a powerful, ATS-optimized,
professionally structured HTML5 resume **content block** (only inner content).
This HTML will be placed inside a template that already contains <html>, <head>, and styling.

============================================================================
📌 OUTPUT RULES (VERY IMPORTANT)
============================================================================
You MUST follow these rules:

1. **DO NOT include**:
   - <html>, <head>, <body>, <style>, <meta>, <title>, <script>
   - DO NOT use code fences (no ```html)

2. **ONLY generate clean inner HTML**, such as:
   <h1>, <h2>, <h3>, <p>, <div>, <span>, <ul>, <li>

3. Use simple inline CSS only when required.

4. Sections to include (if applicable):
   - Header (Name, Title, Contact Info)
   - Summary / Professional Profile
   - Core Skills (highlight JD match)
   - Work Experience (rewrite for ATS)
   - Projects (if present)
   - Education
   - Certifications

5. **Do NOT invent fake companies, roles, or education.**
   You must rewrite and enhance ONLY what exists in the original resume.

6. Improve writing with:
   - Power verbs
   - Quantified impact
   - Industry-standard phrasing
   - Clear bullet lists

7. Strong alignment with the JD is required.
   Incorporate MATCHED SKILLS naturally.
   Integrate MISSING SKILLS only when they are believable.

============================================================================
📌 RAPTOR FRAMEWORK (apply internally)
============================================================================
R — Retrieve key facts from resume  
A — Align with JD relevance  
P — Prioritize relevant skills & responsibilities  
T — Transform content into ATS-optimized bullets  
O — Output clean HTML  
R — Refine tone, clarity, and seniority  

============================================================================
📌 CONTEXT
============================================================================
FIT SCORE: {similarity_score}
MATCHED SKILLS: {matched_skills}
MISSING SKILLS: {missing_skills}

JOB DESCRIPTION:
{jd_text}

---------------------------------------------
ORIGINAL RESUME:
{resume_text}
---------------------------------------------

Now return ONLY the rewritten HTML content block.
"""
    return prompt



# ======================================================
# Main Resume Rewriter
# ======================================================
def rewrite_full_resume_html(
    resume_text: str,
    jd_text: str,
    matched_skills: List[str],
    missing_skills: List[str],
    similarity_score: float,
    provider: str,
    model: str,
    template: str = "professional",
    groq_api_key: str = "",
    gemini_api_key: str = "",
) -> str:
    """
    Generate FULL HTML resume:
    1. LLM creates inner content only.
    2. Selected template wraps the content into final HTML resume.
    """

    # Step 1 — build prompt
    prompt = build_full_rewrite_html_prompt(
        resume_text=resume_text,
        jd_text=jd_text,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        similarity_score=similarity_score,
    )

    # Step 2 — call LLM
    try:
        html_content = call_model(
            provider=provider,
            model=model,
            prompt=prompt,
            groq_api_key=groq_api_key,
            gemini_api_key=gemini_api_key,
        )

    except Exception as e:
        return f"<!-- Resume Rewrite Error: {str(e)} -->"

    # Clean accidental code fences
    html_content = (
        html_content.replace("```html", "")
                    .replace("```", "")
                    .strip()
    )

    # Step 3 — load template
    template_html = load_template(template)

    # Step 4 — merge {{CONTENT}} placeholder
    final_html = template_html.replace("{{CONTENT}}", html_content)

    return final_html
