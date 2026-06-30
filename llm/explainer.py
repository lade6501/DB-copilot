from llm.prompts.explanation_prompt import (
    build_generation_explanation_prompt,
    build_execution_explanation_prompt,
)


class QueryExplainer:
    def __init__(self, llm):
        self.llm = llm

    def explain_generation(
        self,
        user_input: str,
        query: str
    ) -> str:

        prompt = build_generation_explanation_prompt(
            user_input,
            query
        )

        return self.llm.generate(prompt).strip()

    def explain_execution(
        self,
        user_input: str,
        query: str,
        row_count: int,
        sample_results=None
    ) -> str:

        prompt = build_execution_explanation_prompt(
            user_input,
            query,
            row_count,
            sample_results
        )

        return self.llm.generate(prompt).strip()