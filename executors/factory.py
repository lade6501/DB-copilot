from executors.sql_executor import SQLExecutor


class ExecutorFactory:
    @staticmethod
    def get(db_type: str):
        if db_type == "sql":
            return SQLExecutor()

        raise ValueError(f"Unsupported DB type: {db_type}")