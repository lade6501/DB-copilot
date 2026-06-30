import time

from llm.provider import LLMFactory
from llm.output_parser import OutputParser
from llm.explainer import QueryExplainer

from agents.interpreter import Interpreter
from agents.planner import Planner
from agents.validator import QueryValidator

from generators.factory import GeneratorFactory
from executors.factory import ExecutorFactory


class QueryService:
    def __init__(self):
        self.llm = LLMFactory.get_provider(provider="openrouter")

        self.interpreter = Interpreter(self.llm)
        self.planner = Planner()
        self.explainer = QueryExplainer(self.llm)

    def run_stream(self, user_input: str, schema: str):

        yield {
            "step": "start",
            "status": "completed",
            "message": "Started processing your request",
        }

        yield {
            "step": "interpret",
            "status": "in_progress",
        }

        intent = self.interpreter.interpret(user_input)

        yield {
            "step": "interpret",
            "status": "completed",
            "data": intent,
            "explanation": (
                f"Detected a "
                f"{intent.get('intent', 'read')} operation "
                f"for a {intent.get('database', 'sql')} database."
            ),
        }

        yield {
            "step": "plan",
            "status": "in_progress",
        }

        plan = self.planner.create_plan(intent)

        yield {
            "step": "plan",
            "status": "completed",
            "data": plan,
            "explanation": (
                "Prepared execution flow including query generation, "
                "validation, and execution."
            ),
        }

        yield {
            "step": "generate_query",
            "status": "in_progress",
        }

        generator = GeneratorFactory.get(
            plan["db_type"],
            self.llm
        )

        raw_output = generator.generate(
            user_input=user_input,
            schema=schema
        )

        parsed = OutputParser.parse_json(raw_output)

        validated_output = OutputParser.validate_sql_output(parsed)

        query = validated_output["query"]

        generation_explanation = (
            self.explainer.explain_generation(
                user_input=user_input,
                query=query,
            )
        )

        yield {
            "step": "generate_query",
            "status": "completed",
            "query": query,
            "explanation": generation_explanation,
        }

        yield {
            "step": "validate",
            "status": "in_progress",
        }

        QueryValidator.validate_sql(query)

        yield {
            "step": "validate",
            "status": "completed",
            "explanation": (
                "Validation completed successfully. "
                "No unsafe operations were detected."
            ),
        }

        yield {
            "step": "execute",
            "status": "in_progress",
        }

        executor = ExecutorFactory.get(plan["db_type"])

        start_time = time.time()

        result = executor.execute(query)

        end_time = time.time()

        execution_time = round(end_time - start_time, 4)

        row_count = (
            len(result)
            if isinstance(result, list)
            else 0
        )

        execution_summary = (
            f"Query executed successfully and returned "
            f"{row_count} row(s) "
            f"in {execution_time}ms."
        )

        yield {
            "step": "execute",
            "status": "completed",
            "executed_query": query,
            "execution_time": execution_time,
            "row_count": row_count,
            "result": result,
            "explanation": execution_summary,
        }

        yield {
            "step": "done",
        }