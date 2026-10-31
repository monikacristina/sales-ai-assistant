# AI Sales Analytics Assistant

## Project Overview

The AI Sales Analytics Assistant is a web-based business intelligence
application that allows users to analyze sales data using natural
language questions.

It combines Google Gemini API for natural language understanding
with Python, SQL, and SQLite for accurate data analysis.

Users can ask questions about revenue, products, regions, and
monthly sales through an interactive chat interface.

## Features

- Natural language sales queries
- AI-powered question interpretation using Google Gemini
- Rule-based intent detection for common questions
- Total revenue calculation
- Highest revenue-generating product identification
- Monthly revenue analysis
- Best-performing region identification
- Comparison of revenue between two months
- Interactive chat interface
- Input and AI response validation
- Error handling for API failures

## Technology Stack

### Backend
- Python
- FastAPI
- SQLite
- SQL

### Artificial Intelligence
- Google Gemini API
- Rule-based intent detection

### Frontend
- HTML
- CSS
- JavaScript

### Testing
- Pytest
- HTTPX

## System Architecture

1. User submits a natural language question.
2. Python attempts to identify the question's intent.
3. If recognized, the corresponding analytics function executes.
4. Otherwise, the question is sent to Gemini for interpretation.
5. Gemini returns a structured JSON response.
6. The backend validates the response.
7. Python executes the appropriate SQL query.
8. The result is displayed in the chat interface.

## Data Processing

The application stores the original sales records in SQLite.

Revenue is calculated using:

Revenue = (Quantity × Unit Price) - Discount Amount

Only completed transactions with valid positive quantities
and unit prices are included in analytics.

Returned transactions and invalid records are excluded
from analytical calculations without deleting the
original records.

## Supported Questions

- What is the total revenue?
- Which product generates the highest revenue?
- Show monthly revenue.
- Which region performs best?
- Compare January and February.

The application also supports alternative natural language
wording through Gemini interpretation.

## Project Structure

```text
sales-ai-assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── data_loader.py
│   ├── analytics.py
│   ├── ai_interpreter.py
│   └── assistant.py
│
├── data/
│   ├── sales.csv
│   └── sales.db
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── tests/
│   └── test_analytics.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── AI_USAGE.md
