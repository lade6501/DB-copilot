import os
from typing import Optional, Dict, Any
import json
from dotenv import load_dotenv
load_dotenv()

from google import genai


class LLMProvider:
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        raise NotImplementedError


class GeminiProvider(LLMProvider):
    def __init__(
        self,
        model: str = "gemini-2.5-flash",
        temperature: float = 0.2,
        max_output_tokens: int = 2048,
    ):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")

        self.client = genai.Client(api_key=api_key)

        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:

        full_prompt = self._build_prompt(prompt, system_prompt)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config={
                    "temperature": self.temperature,
                    "max_output_tokens": self.max_output_tokens,
                },
            )

            return response.text.strip()

        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")

    def _build_prompt(self, prompt: str, system_prompt: Optional[str]) -> str:
        if system_prompt:
            return f"""
SYSTEM:
{system_prompt}

USER:
{prompt}

RESPONSE:
"""
        return prompt


class LLMFactory:
    @staticmethod
    def get_provider(provider: str = "gemini") -> LLMProvider:
        if provider == "gemini":
            return GeminiProvider()
        raise ValueError(f"Unsupported provider: {provider}")