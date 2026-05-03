class QueryValidator:

    @staticmethod
    def validate_sql(query: str):
        q = query.lower()

        if "drop" in q:
            raise ValueError("DROP operations are not allowed")

        if "delete" in q and "where" not in q:
            raise ValueError("DELETE without WHERE is not allowed")

        if "update" in q and "where" not in q:
            raise ValueError("UPDATE without WHERE is not allowed")

        return True