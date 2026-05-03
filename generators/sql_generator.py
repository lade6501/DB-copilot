from generators.base_generator import BaseGenerator
from llm.prompts.sql_prompt import build_sql_prompt
from llm.prompts.system_prompt import SYSTEM_PROMPT


class SQLGenerator(BaseGenerator):
    def __init__(self, llm):
        self.llm = llm

    def generate(self, user_input: str, schema: str):
        prompt = build_sql_prompt(user_input, schema)
        return self.llm.generate(prompt, SYSTEM_PROMPT)