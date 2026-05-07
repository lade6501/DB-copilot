def build_explanation_prompt(user_input: str, query: str) -> str:
    return f"""
You are a helpful assistant explaining database queries to non-technical users.

USER REQUEST:
{user_input}

GENERATED SQL QUERY:
{query}

TASK:
Explain what this query does in simple, non-technical language.

RULES:
- Keep it short (1–2 sentences)
- Do NOT mention SQL syntax
- Focus on what data is being retrieved
- Be clear and user-friendly

OUTPUT:
Return only plain text explanation.
"""