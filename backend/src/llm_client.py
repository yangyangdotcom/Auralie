from typing import Optional
from openai import OpenAI
from config import Config

class LLMClient:
    """Unified interface for LLM providers"""

    def __init__(self):
        Config.validate()
        self.provider = Config.LLM_PROVIDER

        if self.provider == "openrouter":
            # OpenRouter uses OpenAI SDK with custom base URL
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=Config.OPENROUTER_API_KEY,
            )
            self.model = Config.OPENROUTER_MODEL
            self.app_name = Config.OPENROUTER_APP_NAME
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")

    def generate(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate text using the configured LLM"""

        if self.provider == "openrouter":
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                extra_headers={
                    "HTTP-Referer": f"https://github.com/auralie/{self.app_name}",
                    "X-Title": self.app_name,
                }
            )
            return response.choices[0].message.content

        else:
            raise ValueError(f"Unknown provider: {self.provider}")
