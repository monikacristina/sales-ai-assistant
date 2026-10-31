import re

from app.ai_interpreter import interpret_question
from app.analytics import (
    get_total_revenue,
    get_top_product,
    get_monthly_revenue,
    get_top_region,
    compare_months
)


MONTHS = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06"
}


def detect_intent(question):
    text = question.lower().strip()

    # Compare two months
    found_months = []

    for month, number in MONTHS.items():
        if re.search(r"\b" + month + r"\b", text):
            found_months.append(number)

    if len(found_months) == 2 and (
        "compare" in text or "comparison" in text
    ):
        return {
            "intent": "compare_months",
            "parameters": {
                "month1": found_months[0] + "-2026",
                "month2": found_months[1] + "-2026"
            }
        }

    # Total revenue
    if "total revenue" in text or "overall revenue" in text:
        return {
            "intent": "total_revenue",
            "parameters": {}
        }

    # Top product
    # Top product
    if (
        "top product" in text
        or "highest revenue product" in text
        or "product generates the highest revenue" in text
        or "which product sells the most" in text
     ):
        return {
            "intent": "top_product",
            "parameters": {}
        }

    # Monthly revenue
    if "monthly revenue" in text or "revenue by month" in text:
        return {
            "intent": "monthly_revenue",
            "parameters": {}
        }

    # Top region
    if (
        "top region" in text
        or "best performing region" in text
        or "which region performs best" in text
        or "which region performs the best" in text
        or "highest performing region" in text
        or "region performs best" in text
    ):
        return {
            "intent": "top_region",
            "parameters": {}
        }

    return None


def process_question(question):

    interpreted = detect_intent(question)

    # Use Gemini only if Python cannot recognize the question
    if interpreted is None:
        try:
            interpreted = interpret_question(question)
        except RuntimeError as error:
            return {"error": str(error)}
        if not validate_interpretation(interpreted):
            return {
                "error": "The AI returned an invalid response. Please rephrase your question."
            }
    intent = interpreted.get("intent")
    parameters = interpreted.get("parameters", {})

    if intent == "total_revenue":
        result = get_total_revenue()

    elif intent == "top_product":
        result = get_top_product()

    elif intent == "monthly_revenue":
        result = get_monthly_revenue()

    elif intent == "top_region":
        result = get_top_region()

    elif intent == "compare_months":
        month1 = parameters.get("month1")
        month2 = parameters.get("month2")

        if not month1 or not month2:
            return {"error": "Please specify two months to compare."}

        result = compare_months(month1, month2)

    else:
        return {"error": "Sorry, I couldn't understand that question."}

    return {
        "intent": intent,
        "result": result
    }

def validate_interpretation(interpreted):

    if not isinstance(interpreted, dict):
        return False

    intent = interpreted.get("intent")
    parameters = interpreted.get("parameters", {})

    supported_intents = {
        "total_revenue",
        "top_product",
        "monthly_revenue",
        "top_region",
        "compare_months"
    }

    if intent not in supported_intents:
        return False

    if not isinstance(parameters, dict):
        return False

    if intent == "compare_months":

        month1 = parameters.get("month1")
        month2 = parameters.get("month2")

        month_pattern = r"^(0[1-6])-2026$"

        if not month1 or not month2:
            return False

        if not re.match(month_pattern, month1):
            return False

        if not re.match(month_pattern, month2):
            return False

        if month1 == month2:
            return False

    return True
