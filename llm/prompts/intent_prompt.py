def build_intent_prompt(user_input: str) -> str:
    return f"""
Classify the user request.

USER INPUT:
{user_input}

OUTPUT FORMAT (STRICT JSON):
{{
  "intent": "read | write | update | delete",
  "database": "sql | mongodb",
  "complexity": "simple | medium | complex"
}}

RULES:
- "read" → SELECT / find
- "write" → INSERT
- "update" → UPDATE
- "delete" → DELETE
- Default database = "sql" if not specified

IMPORTANT:
- Return ONLY JSON
- No markdown
- No explanation
"""