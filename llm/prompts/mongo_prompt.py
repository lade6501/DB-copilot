def build_mongo_prompt(user_input: str, schema: str) -> str:
    return f"""
You are a MongoDB expert.

COLLECTION SCHEMA:
{schema}

USER REQUEST:
{user_input}

TASK:
Convert the request into a MongoDB query.

RULES:
- Use correct MongoDB syntax
- Use find(), aggregate(), insertOne(), updateOne(), deleteOne()
- Prefer find() for read queries
- Always include filters when needed

OUTPUT FORMAT (STRICT JSON):
{{
  "collection": "collection_name",
  "operation": "find | insert | update | delete | aggregate",
  "query": {{}},
  "explanation": "short explanation"
}}

IMPORTANT:
- No markdown
- Only JSON
"""