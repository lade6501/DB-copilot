from llm.prompts.intent_prompt import build_intent_prompt
from llm.prompts.system_prompt import SYSTEM_PROMPT
from llm.output_parser import OutputParser


class Interpreter:
    def __init__(self, llm):
        self.llm = llm

    def interpret(self, user_input: str):
        prompt = build_intent_prompt(user_input)

        raw = self.llm.generate(prompt, SYSTEM_PROMPT)
        return OutputParser.parse_json(raw)