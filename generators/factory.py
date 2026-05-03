from generators.sql_generator import SQLGenerator


class GeneratorFactory:
    @staticmethod
    def get(db_type: str, llm):
        if db_type == "sql":
            return SQLGenerator(llm)

        raise ValueError(f"Unsupported DB type: {db_type}")