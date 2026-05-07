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
        self.llm = LLMFactory.get_provider()
        self.interpreter = Interpreter(self.llm)
        self.planner = Planner()
        self.explainer = QueryExplainer(self.llm)

    def run_stream(self, user_input: str, schema: str):

        yield {
            "step": "start",
            "status": "completed",
            "message": "Started processing your request"
        }

      
        # 1. INTERPRET
      
        intent = self.interpreter.interpret(user_input)

        yield {
            "step": "interpret",
            "status": "completed",
            "data": intent,
            "explanation": "Understood your request and identified the type of operation."
        }

        # 2. PLAN
        plan = self.planner.create_plan(intent)

        yield {
            "step": "plan",
            "status": "completed",
            "data": plan,
            "explanation": "Planned steps to generate, validate, and execute the query."
        }

        # 3. GENERATE QUERY
        yield {
            "step": "generate_query",
            "status": "in_progress"
        }

        generator = GeneratorFactory.get(plan["db_type"], self.llm)

        raw_output = generator.generate(user_input, schema)

        parsed = OutputParser.parse_json(raw_output)
        validated_output = OutputParser.validate_sql_output(parsed)

        query = validated_output["query"]

        explanation = self.explainer.explain(user_input, query)

        yield {
            "step": "generate_query",
            "status": "completed",
            "query": query,
            "explanation": explanation
        }

        # 4. VALIDATE
        QueryValidator.validate_sql(query)

        yield {
            "step": "validate",
            "status": "completed",
            "explanation": "Checked the query to ensure it is safe to execute."
        }

        # 5. EXECUTE
        executor = ExecutorFactory.get(plan["db_type"])

        yield {
            "step": "execute",
            "status": "in_progress"
        }

        start = time.time()
        result = executor.execute(query)
        end = time.time()

        execution_time = round(end - start, 4)
        row_count = len(result) if isinstance(result, list) else None

        yield {
            "step": "execute",
            "status": "completed",
            "executed_query": query,
            "execution_time": execution_time,
            "row_count": row_count,
            "result": result,
            "explanation": f"Executed the query and retrieved {row_count or 0} result(s)."
        }

        try:
            summary = self.explainer.explain(
                user_input,
                f"Query returned {row_count or 0} result(s)"
            )
        except:
            summary = f"Found {row_count or 0} result(s) matching your request."

        yield {
            "step": "summary",
            "status": "completed",
            "message": summary
        }

        yield {
            "step": "done"
        }