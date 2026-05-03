class Planner:
    def create_plan(self, intent: dict):
        return {
            "db_type": intent.get("database", "sql"),
            "operation": intent.get("intent", "read"),
            "steps": ["generate_query", "validate", "execute"]
        }