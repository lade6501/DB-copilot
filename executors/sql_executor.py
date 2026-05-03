import sqlite3
from executors.base_executor import BaseExecutor


class SQLExecutor(BaseExecutor):
    def __init__(self, db_path="test.db"):
        self.db_path = db_path

    def execute(self, query: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(query)

            if query.lower().startswith("select"):
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()

                result = [
                    dict(zip(columns, row)) for row in rows
                ]

                return result
            else:
                conn.commit()
                return {"rows_affected": cursor.rowcount}

        finally:
            conn.close()