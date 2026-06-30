def build_generation_explanation_prompt(
    user_input: str,
    query: str
) -> str:

    return f"""
You are explaining how an AI converted a natural language request into a database query.

USER REQUEST:
{user_input}

GENERATED QUERY:
{query}

TASK:
Explain:
- how the request was interpreted
- why this query structure was chosen
- any assumptions made
- matching/search behavior used

IMPORTANT:
- Do NOT mention query results
- Focus ONLY on query generation reasoning
- Keep response concise and natural
"""

def build_execution_explanation_prompt(
    user_input: str,
    query: str,
    row_count: int,
    sample_results: list | None = None
) -> str:

    return f"""
You are explaining the execution outcome of a database query.

USER REQUEST:
{user_input}

QUERY:
{query}

RESULT COUNT:
{row_count}

SAMPLE RESULTS:
{sample_results}

TASK:
Explain:
- what data was found
- whether results matched expectation
- any interesting observations
- summarize outcome naturally

IMPORTANT:
- Do NOT explain SQL syntax
- Focus on actual execution outcome
- Be conversational and concise

GOOD EXAMPLE:
"I found 2 matching users, including Vishal and John. 
The search matched successfully using case-insensitive filtering."
"""