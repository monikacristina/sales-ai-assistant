import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


def interpret_question(question):

    if client is None:
        raise RuntimeError(
            "Gemini API key is missing. Please check your .env file."
        )

    prompt = f"""
    You are an AI assistant for a sales analytics application.

    Understand the user's question and identify the correct intent.

    Supported intents:
    - total_revenue
    - top_product
    - monthly_revenue
    - top_region
    - compare_months

    Return ONLY valid JSON in this format:

    {{
        "intent": "intent_name",
        "parameters": {{}}
    }}

    If the intent is compare_months, extract month1 and month2
    in MM-YYYY format.

    The sales dataset contains transactions from January to June 2026.

    When the user mentions a month without specifying a year,
    use 2026.

    If the user explicitly specifies a year, use that year.

    User question: {question}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        interpreted = json.loads(response.text)

        if not isinstance(interpreted, dict):
            raise ValueError("Invalid response format.")

        return interpreted

    except Exception as error:
        print(f"Gemini API Error: {error}")

        raise RuntimeError(
            "The AI service is temporarily unavailable. "
            "Please try again later."
        ) from error
