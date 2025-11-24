import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
ENV_GROQ_KEY = os.getenv("GROQ_API_KEY", "")
ENV_GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

# External Clients
import ollama
from groq import Groq
import google.generativeai as genai


# ======================================================
# OLLAMA CALLER
# ======================================================
def call_ollama(model: str, prompt: str) -> str:
    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]

    except Exception as e:
        return f"[Ollama Error: {str(e)}]"



# ======================================================
# GROQ CALLER
# ======================================================
def call_groq(model: str, prompt: str, api_key: str) -> str:
    if not api_key:
        return "[Groq Error: Missing API key]"

    try:
        client = Groq(api_key=api_key)

        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        # New Groq SDK uses "message.content"
        return resp.choices[0].message.content

    except Exception as e:
        return f"[Groq Error: {str(e)}]"



# ======================================================
# GEMINI CALLER
# ======================================================
def call_gemini(model: str, prompt: str, api_key: str) -> str:
    if not api_key:
        return "[Gemini Error: Missing API key]"

    try:
        # Gemini requires "models/<name>"
        if not model.startswith("models/"):
            model = f"models/{model}"

        genai.configure(api_key=api_key)

        gmodel = genai.GenerativeModel(model)
        response = gmodel.generate_content(prompt)

        # Gemini returns .text, not choices
        return response.text

    except Exception as e:
        return f"[Gemini Error: {str(e)}]"



# ======================================================
# UNIVERSAL CALL WRAPPER
# ======================================================
def call_model(provider: str, model: str, prompt: str,
               groq_api_key: str = None, gemini_api_key: str = None) -> str:
    """
    Normalized universal LLM caller for:
    - ollama
    - groq
    - gemini
    """

    provider = provider.lower()

    # -----------------------------------------------
    # OLLAMA (no API key required)
    # -----------------------------------------------
    if provider == "ollama":
        return call_ollama(model, prompt)


    # -----------------------------------------------
    # GROQ
    # -----------------------------------------------
    elif provider == "groq":
        api_key = groq_api_key or ENV_GROQ_KEY
        return call_groq(model, prompt, api_key)


    # -----------------------------------------------
    # GEMINI
    # -----------------------------------------------
    elif provider == "gemini":
        api_key = gemini_api_key or ENV_GEMINI_KEY
        return call_gemini(model, prompt, api_key)


    # -----------------------------------------------
    # INVALID PROVIDER
    # -----------------------------------------------
    else:
        return f"[Error: Unsupported provider '{provider}'. Use: ollama, groq, gemini]"
# ======================================================