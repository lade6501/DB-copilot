from typing import Dict, List
import sqlite3

# Optional Mongo import
try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None


class SchemaLoader:
    """
    Unified schema loader for SQL & MongoDB
    """

    def __init__(self, db_type: str, config: Dict):
        self.db_type = db_type.lower()
        self.config = config

    def load(self) -> str:
        if self.db_type == "sql":
            return SQLSchemaLoader(self.config).load()

        elif self.db_type == "mongodb":
            return MongoSchemaLoader(self.config).load()

        else:
            raise ValueError(f"Unsupported DB type: {self.db_type}")


# -----------------------------
# SQL SCHEMA LOADER
# -----------------------------

class SQLSchemaLoader:
    def __init__(self, config: Dict):
        self.db_path = config.get("db_path", "test.db")

    def load(self) -> str:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        schema_str = ""

        try:
            # Get tables
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';"
            )
            tables = cursor.fetchall()

            for (table_name,) in tables:
                schema_str += f"\nTable: {table_name}\n"

                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()

                for col in columns:
                    col_name = col[1]
                    col_type = col[2]
                    schema_str += f"- {col_name} ({col_type})\n"

        finally:
            conn.close()

        return schema_str.strip()


# -----------------------------
# MONGO SCHEMA LOADER
# -----------------------------

class MongoSchemaLoader:
    def __init__(self, config: Dict):
        if MongoClient is None:
            raise ImportError("pymongo is not installed")

        self.uri = config.get("uri", "mongodb://localhost:27017/")
        self.db_name = config.get("db_name")

    def load(self) -> str:
        client = MongoClient(self.uri)
        db = client[self.db_name]

        schema_str = ""

        try:
            collections = db.list_collection_names()

            for col in collections:
                schema_str += f"\nCollection: {col}\n"

                sample = db[col].find_one()

                if sample:
                    for key, value in sample.items():
                        field_type = type(value).__name__
                        schema_str += f"- {key} ({field_type})\n"
                else:
                    schema_str += "- (empty collection)\n"

        finally:
            client.close()

        return schema_str.strip()