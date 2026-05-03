import time

from llm.provider import LLMFactory
from llm.output_parser import OutputParser

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

    def run_stream(self, user_input: str, schema: str):

        yield {"step": "start", "message": "Processing started"}

        # 1. INTERPRET
        intent = self.interpreter.interpret(user_input)
        yield {
            "step": "interpret",
            "status": "completed",
            "data": intent
        }

        # 2. PLAN
        plan = self.planner.create_plan(intent)
        yield {
            "step": "plan",
            "status": "completed",
            "data": plan
        }

        # 3. GENERATE QUERY
        yield {"step": "generate_query", "status": "in_progress"}

        generator = GeneratorFactory.get(plan["db_type"], self.llm)

        raw_output = generator.generate(user_input, schema)

        parsed = OutputParser.parse_json(raw_output)
        validated_output = OutputParser.validate_sql_output(parsed)

        query = validated_output["query"]

        yield {
            "step": "generate_query",
            "status": "completed",
            "query": query
        }

        # 4. VALIDATE
        QueryValidator.validate_sql(query)

        yield {
            "step": "validate",
            "status": "completed"
        }

        # 5. EXECUTE
        executor = ExecutorFactory.get(plan["db_type"])

        yield {"step": "execute", "status": "in_progress"}

        start = time.time()
        result = executor.execute(query)
        end = time.time()

        yield {
            "step": "execute",
            "status": "completed",
            "executed_query": query,
            "execution_time": round(end - start, 4),
            "row_count": len(result) if isinstance(result, list) else None,
            "result": result
        }