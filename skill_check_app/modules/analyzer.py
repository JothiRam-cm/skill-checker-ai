import json
import re
from typing import Dict
from modules.llm_switcher import call_model


# -----------------------------------------------------------------
# Helper: extract JSON object from messy LLM output using regex
# -----------------------------------------------------------------
def extract_json_safe(text: str) -> dict:
    try:
        # Try clean JSON first
        return json.loads(text)
    except:
        pass

    # Try to extract the largest JSON block
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        json_str = match.group()
        try:
            return json.loads(json_str)
        except:
            pass

    # Last attempt: FIX JSON using dirty cleaning
    try:
        cleaned = (
            text.replace("```json", "")
                .replace("```", "")
                .replace("\n", " ")
        )
        return json.loads(cleaned)
    except:
        return {}  # give up → caller handles fallback


# -----------------------------------------------------------------
# LLM-powered ATS Analysis (JSON Output)
# -----------------------------------------------------------------
def analyze_resume_vs_jd(
    resume_text: str,
    jd_text: str,
    provider: str,
    model: str,
    groq_api_key: str = "",
    gemini_api_key: str = ""
) -> Dict:
    
    prompt = f"""
You are an ATS Evaluation Engine created to perform a deep, multi-layered analysis of resume–job description fit.

Return ONLY a clean JSON object. NO commentary, NO markdown, NO backticks.

JSON SCHEMA (STRICT):
{
  "ats_score": int,                    // Overall ATS compatibility score (0–100)
  "fit_score": int,                    // How well the candidate fits this job (0–100)
  "keyword_coverage": float,           // % of job keywords found in resume (0.0–1.0)
  "matched_skills": [string],          // Skills from JD that the resume already covers
  "missing_skills": [string],          // Skills required but NOT found in the resume
  "summary_feedback": string,          // 5–6 line summary of how well the resume matches the JD
  "experience_feedback": string,       // Critical evaluation of candidate’s past experience vs JD responsibilities
  "missing_keywords": [string],        // JD keywords not present in resume text
  "final_recommendation": string       // Clear verdict: "Strong Fit", "Moderate Fit", or "Weak Fit" + reasoning
}

INSTRUCTIONS — ENSURE ALL:
1. Output MUST be STRICT JSON.  
2. No backticks, no prose outside the JSON.  
3. JSON keys must appear exactly as specified.  
4. All fields MUST be filled.  
5. The evaluation must:
   - Extract keywords from the job description.
   - Compare them against the resume.
   - Analyze experience depth, recency, and relevance.
   - Judge whether the candidate is FIT for the job.
   - Include reasoning inside feedback fields.
6. “final_recommendation” MUST explicitly state whether **I am fit for this job** based on evidence.
7. Treat the resume and JD exactly as provided — no external assumptions.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

Now output ONLY the JSON:
"""

    raw = call_model(
        provider=provider,
        model=model,
        prompt=prompt,
        groq_api_key=groq_api_key,
        gemini_api_key=gemini_api_key
    ).strip()

    # --- Extract & fix JSON safely ---
    parsed = extract_json_safe(raw)

    # If still invalid, fallback
    if not parsed or not isinstance(parsed, dict):
        parsed = {
            "ats_score": 0,
            "fit_score": 0,
            "keyword_coverage": 0,
            "matched_skills": [],
            "missing_skills": [],
            "summary_feedback": "LLM returned invalid JSON.",
            "experience_feedback": "",
            "missing_keywords": [],
            "final_recommendation": ""
        }

    return parsed


# from typing import Dict, List
# from modules.llm_switcher import call_model
# import json


# # =====================================================================
# # SUPERPOWERED ATS ANALYZER (LLM-ONLY)
# # Using RAPTOR prompting + evaluator role + schema-locking
# # =====================================================================

# def build_ats_prompt(resume_text: str, jd_text: str) -> str:
#     """
#     Build an advanced ATS assessment prompt using:
#     - RAPTOR prompting structure
#     - Evaluator role
#     - Schema-driven JSON enforcement
#     """

#     prompt = f"""
# You are **RAPTOR-ATS**, an expert Applicant Tracking System evaluator with
# deep knowledge of hiring standards, job matching, skill evaluation, and
# keyword relevance scoring.

# Your role is to analyze the RESUME against the JOB DESCRIPTION and provide
# a deep ATS-style evaluation following the strict JSON schema below.

# ======================================================================
# 📌 **PROCESS YOU MUST FOLLOW (RAPTOR FRAMEWORK)**
# ======================================================================

# 1. **R — Retrieve Relevant Information**
#    Extract all relevant skills, responsibilities, metrics, and experience 
#    from both the resume and JD.

# 2. **A — Analyze Alignment**
#    Compare responsibilities, skills, seniority, impact depth, and keywords.

# 3. **P — Prioritize Key Skills**
#    Identify the most important JD keywords and skills and measure their 
#    presence in the resume.

# 4. **T — Test Against ATS Rules**
#    - Keyword density
#    - Section completeness
#    - Experience relevance
#    - Missing critical competencies
#    - Action verbs usage
#    - Clarity & structure

# 5. **O — Output Structured Evaluation**
#    Output only JSON following the schema below.

# 6. **R — Recommend Improvements**
#    Recommend missing skills, better phrasing, and content improvements.


# ======================================================================
# 📌 **STRICT JSON SCHEMA YOU MUST FOLLOW**
# ======================================================================

# Return EXACTLY this JSON structure:

# {{
#   "fit_score": 0-100 integer,
#   "ats_score": 0-100 integer,
#   "matched_skills": ["skill1", "skill2", ...],
#   "missing_skills": ["skill1", "skill2", ...],
#   "keyword_coverage": 0-100 integer,
#   "summary_alignment": "string",
#   "experience_alignment": "string",
#   "red_flags": ["string1", "string2"],
#   "recommendations": ["string1", "string2"]
# }}

# Rules:
# - Use lowercase for skills.
# - Be objective, not generic.
# - Do NOT output explanations outside JSON.
# - No code blocks.
# - No commentary.
# - No markdown.


# ======================================================================
# 📌 **INPUTS**
# ======================================================================

# RESUME:
# {resume_text}

# -------------------------------------

# JOB DESCRIPTION:
# {jd_text}

# ======================================================================
# 📌 OUTPUT INSTRUCTIONS
# ======================================================================

# Return ONLY the JSON object, **nothing else**.
# If unsure, make the best reasonable assumption.
# """

#     return prompt



# # =====================================================================
# # MAIN ATS ANALYZER FUNCTION
# # =====================================================================

# def analyze_resume_vs_jd(
#     resume_text: str,
#     jd_text: str,
#     provider: str,
#     model: str,
#     groq_api_key: str = "",
#     gemini_api_key: str = ""
# ) -> Dict:
#     """
#     LLM-powered ATS evaluation with JSON schema validation.
#     """

#     prompt = build_ats_prompt(resume_text, jd_text)

#     # LLM CALL
#     raw = call_model(
#         provider=provider,
#         model=model,
#         prompt=prompt,
#         groq_api_key=groq_api_key,
#         gemini_api_key=gemini_api_key,
#     )

#     # Clean accidental markdown wrappers
#     raw = raw.replace("```json", "").replace("```", "").strip()

#     # JSON Parsing
#     try:
#         data = json.loads(raw)
#     except Exception:
#         return {
#             "error": "LLM returned invalid JSON",
#             "raw_response": raw
#         }

#     # Safety correction if fields missing
#     defaults = {
#         "fit_score": 0,
#         "ats_score": 0,
#         "matched_skills": [],
#         "missing_skills": [],
#         "keyword_coverage": 0,
#         "summary_alignment": "",
#         "experience_alignment": "",
#         "red_flags": [],
#         "recommendations": []
#     }

#     for k, v in defaults.items():
#         if k not in data:
#             data[k] = v

#     return data
