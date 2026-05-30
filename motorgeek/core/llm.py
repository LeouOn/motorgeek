import json
import os
import re
from pathlib import Path

import yaml

_openai_available = True
_anthropic_available = True
_deepseek_available = True

try:
    import openai
except ImportError:
    _openai_available = False

try:
    import anthropic
except ImportError:
    _anthropic_available = False

try:
    import openai as deepseek_openai
except ImportError:
    _deepseek_available = False


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

        config = _load_config()
        llm_config = config.get("llm", {})

        if self.provider == "openai":
            if not _openai_available:
                raise ImportError(
                    "openai package not installed. Run: pip install openai>=1.0"
                )
            api_key = os.environ.get("OPENAI_API_KEY") or llm_config.get("api_key", "")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set in environment or config.yaml")
            self._client = openai.OpenAI(api_key=api_key)
        elif self.provider == "anthropic":
            if not _anthropic_available:
                raise ImportError(
                    "anthropic package not installed. Run: pip install anthropic>=0.20"
                )
            api_key = os.environ.get("ANTHROPIC_API_KEY") or llm_config.get("api_key", "")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not set in environment or config.yaml")
            self._client = anthropic.Anthropic(api_key=api_key)
        elif self.provider == "deepseek":
            if not _deepseek_available:
                raise ImportError(
                    "openai package not installed. Run: pip install openai>=1.0"
                )
            api_key = os.environ.get("DEEPSEEK_API_KEY") or llm_config.get("api_key", "")
            if not api_key:
                raise ValueError("DEEPSEEK_API_KEY not set in environment or config.yaml")
            self._client = deepseek_openai.OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com",
            )
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
        elif self.provider == "deepseek":
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def complete_json(self, prompt: str, **kwargs) -> dict:
        response = self.complete(prompt, **kwargs)
        match = re.search(r"```json\s*(.*?)```", response, re.DOTALL)
        if match:
            response = match.group(1)
        return json.loads(response)

    def complete_with_tools(
        self,
        messages: list[dict],
        tools: list[dict],
        **kwargs,
    ) -> dict:
        """Send a conversation with tool definitions. Returns the full API response message dict.
        
        Response shape: {"role": "assistant", "content": str|None, "tool_calls": list|None}
        tool_calls entries: {"id": str, "type": "function", "function": {"name": str, "arguments": str}}
        """
        client = self._get_client()

        if self.provider in ("openai", "deepseek"):
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                **kwargs,
            )
            msg = response.choices[0].message
            result = {"role": "assistant", "content": msg.content}
            if msg.tool_calls:
                result["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ]
            return result
        else:
            # Fallback for providers without native tool support: embed tools in prompt
            tools_desc = "\n".join(
                f"- {t['function']['name']}: {t['function']['description']}"
                for t in tools
            )
            enhanced_prompt = (
                f"{messages[-1]['content']}\n\n"
                f"Available tools:\n{tools_desc}\n\n"
                f"To use a tool, respond with JSON: {{\"tool\": \"name\", \"args\": {{...}}}}"
            )
            messages[-1]["content"] = enhanced_prompt
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                **{k: v for k, v in kwargs.items() if k != "tools"},
            )
            content = response.choices[0].message.content
            # Try to parse as JSON tool call
            try:
                parsed = json.loads(content) if content else {}
                if "tool" in parsed:
                    return {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [{
                            "id": "fallback-0",
                            "type": "function",
                            "function": {
                                "name": parsed["tool"],
                                "arguments": json.dumps(parsed.get("args", {})),
                            },
                        }],
                    }
            except json.JSONDecodeError:
                pass
            return {"role": "assistant", "content": content, "tool_calls": None}