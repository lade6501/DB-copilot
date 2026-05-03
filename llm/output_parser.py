import json
import re
from typing import Any, Dict


class OutputParserError(Exception):
    pass


class OutputParser:
    """
    Robust parser for LLM outputs (handles messy JSON)
    """

    @staticmethod
    def parse_json(text: str) -> Dict[str, Any]:
        """
        Main entry: parse LLM response into JSON
        """

        if not text:
            raise OutputParserError("Empty response from LLM")

        # Step 1: try direct parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Step 2: extract JSON block
        json_str = OutputParser._extract_json(text)

        # Step 3: clean JSON
        json_str = OutputParser._clean_json(json_str)

        # Step 4: parse again
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise OutputParserError(
                f"Failed to parse JSON after cleanup.\nRaw:\n{text}\nError: {str(e)}"
            )

    # -----------------------------
    # HELPERS
    # -----------------------------

    @staticmethod
    def _extract_json(text: str) -> str:
        """
        Extract JSON object from text
        """

        # match first {...}
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if not match:
            raise OutputParserError(f"No JSON object found in response:\n{text}")

        return match.group(0)

    @staticmethod
    def _clean_json(json_str: str) -> str:
        """
        Clean common LLM JSON issues
        """

        # remove trailing commas
        json_str = re.sub(r",\s*}", "}", json_str)
        json_str = re.sub(r",\s*]", "]", json_str)

        # fix smart quotes
        json_str = json_str.replace("“", '"').replace("”", '"')

        # remove backticks if present
        json_str = json_str.replace("```json", "").replace("```", "")

        return json_str.strip()

    # -----------------------------
    # VALIDATORS
    # -----------------------------

    @staticmethod
    def validate_sql_output(data: Dict[str, Any]) -> Dict[str, Any]:
        required_keys = ["query", "query_type"]

        for key in required_keys:
            if key not in data:
                raise OutputParserError(f"Missing required field: {key}")

        return data

    @staticmethod
    def validate_mongo_output(data: Dict[str, Any]) -> Dict[str, Any]:
        required_keys = ["collection", "operation", "query"]

        for key in required_keys:
            if key not in data:
                raise OutputParserError(f"Missing required field: {key}")

        return data