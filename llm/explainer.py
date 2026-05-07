from llm.prompts.explanation_prompt import build_explanation_prompt


class QueryExplainer:
    def __init__(self, llm):
        self.llm = llm

    def explain(self, user_input: str, query: str) -> str:
        prompt = build_explanation_prompt(user_input, query)

        try:
            return self.llm.generate(prompt).strip()
        except:
            return "This query retrieves data based on your request."