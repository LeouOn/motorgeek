import json
import os
import re
from pathlib import Path

import yaml

_openai_available = True
_anthropic_available = True

try:
    import openai
except ImportError:
    _openai_available = False

try:
    import anthropic
except ImportError:
    _anthropic_available = False


def _load_config():
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {}


class LLMClient:
    def __init__(self, provider=None, model=None):
        config = _load_config()
        llm_config = config.get("llm", {})

        self.provider = provider or llm_config.get("provider", "openai")
        self.model = model or llm_config.get("model", "gpt-4o")
        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client

        if self.provider == "openai":
            if not _openai_available:
                raise ImportError(
                    "openai package not installed. Run: pip install openai>=1.0"
                )
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            self._client = openai.OpenAI(api_key=api_key)
        elif self.provider == "anthropic":
            if not _anthropic_available:
                raise ImportError(
                    "anthropic package not installed. Run: pip install anthropic>=0.20"
                )
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            self._client = anthropic.Anthropic(api_key=api_key)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

        return self._client

    def complete(self, prompt: str, **kwargs) -> str:
        client = self._get_client()

        if self.provider == "openai":
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        elif self.provider == "anthropic":
            response = client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.content[0].text
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def complete_json(self, prompt: str, **kwargs) -> dict:
        response = self.complete(prompt, **kwargs)
        match = re.search(r"```json\s*(.*?)```", response, re.DOTALL)
        if match:
            response = match.group(1)
        return json.loads(response)