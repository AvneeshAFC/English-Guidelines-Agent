import os

API_URL = "http://127.0.0.1:8000"
STATUS_CODE = {
    "SUCCESS": 200,
    "BAD_REQUEST": 400,
    "INTERNAL_SERVER_ERROR": 500,
}

DEFAULT_GUIDELINES = """
1. Grammar and Spelling: Ensure all text is free of grammatical errors and spelling mistakes.
2. Clarity and Conciseness: Sentences should be clear, concise, and easy to understand. Avoid jargon where possible.
3. Sentence Structure: Vary sentence structure to maintain reader engagement. Avoid run-on sentences.
4. Active Voice: Use active voice more than passive voice for more direct and impactful writing.
5. Tone: Maintain a professional and formal tone throughout the document.
"""