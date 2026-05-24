from motorgeek.core.llm import LLMClient

def test_llm_client_initializes():
    client = LLMClient(provider="openai", model="gpt-4o")
    assert client.provider == "openai"
    assert client.model == "gpt-4o"

def test_llm_client_defaults_from_config():
    client = LLMClient()
    assert client.provider in ("openai", "anthropic")