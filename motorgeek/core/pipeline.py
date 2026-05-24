import json
from pathlib import Path
from typing import Optional

from motorgeek.core.llm import LLMClient


class DimensionRouter:
    DIMENSIONS = [
        "performance", "engineering_ice", "engineering_ev",
        "reliability", "consumables", "cost_to_own",
        "historical_context", "mod_potential", "electronics",
        "repair_catalog", "hybrid_system"
    ]

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()

    def route(self, text: str) -> list[str]:
        dims_str = ", ".join(self.DIMENSIONS)
        prompt = f"""You are a dimension classifier for automotive data.

Given the following text, identify which dimensions it contains data for.
Choose from: {dims_str}

Return a JSON array of dimension names. Example: ["performance", "reliability"]

Text:
{text}

Return ONLY the JSON array, no markdown formatting."""

        try:
            response = self.llm.complete(prompt)
            match = _extract_json_array(response)
            if match:
                valid = [d for d in match if d in self.DIMENSIONS]
                if valid:
                    return valid
        except Exception:
            pass
        return ["performance"]


class StructuredExtractor:
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()
        self._prompt_cache = {}

    def _load_prompt(self, dimension: str) -> str:
        if dimension not in self._prompt_cache:
            prompt_path = Path(__file__).parent.parent / "cli" / "prompts" / f"{dimension}.txt"
            if prompt_path.exists():
                with open(prompt_path, "r") as f:
                    self._prompt_cache[dimension] = f.read()
            else:
                self._prompt_cache[dimension] = ""
        return self._prompt_cache[dimension]

    def extract(self, text: str, dimension: str) -> dict:
        template = self._load_prompt(dimension)
        prompt = f"""{template}

Text to extract from:
{text}

Return ONLY the JSON object, no markdown formatting."""

        try:
            response = self.llm.complete(prompt)
            result = _extract_json_object(response)
            if result:
                return result
        except Exception:
            pass
        return {"_error": "extraction failed"}


class IngestPipeline:
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.router = DimensionRouter(llm_client)
        self.extractor = StructuredExtractor(llm_client)

    def run(self, raw_text: str, car_id: int, dimension_hint: Optional[str] = None) -> dict:
        if dimension_hint:
            dimensions = [dimension_hint]
        else:
            dimensions = self.router.route(raw_text)

        results = {}
        for dim in dimensions:
            results[dim] = self.extractor.extract(raw_text, dim)

        return results


def _extract_json_array(text: str) -> Optional[list]:
    text = text.strip()
    match = json.loads(text)
    if isinstance(match, list):
        return match
    return None


def _extract_json_object(text: str) -> Optional[dict]:
    text = text.strip()
    if text.startswith("```"):
        idx = text.find("{")
        if idx != -1:
            text = text[idx:]
        idx = text.rfind("}")
        if idx != -1:
            text = text[:idx+1]
    try:
        result = json.loads(text)
        if isinstance(result, dict):
            return result
    except json.JSONDecodeError:
        pass
    return None