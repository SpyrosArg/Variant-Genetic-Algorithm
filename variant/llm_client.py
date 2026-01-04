import openai
import anthropic
from typing import Optional


class LLMClient:
    
    def __init__(self, model: str, api_key: str):

        self.model = model
        self.api_key = api_key
        
        if model.startswith("gpt"):
            self.provider = "openai"
            self.openai_client = openai.OpenAI(api_key=api_key)
        elif model.startswith("claude"):
            self.provider = "anthropic"
            self.anthropic_client = anthropic.Anthropic(api_key=api_key)
        else:
            raise ValueError(f"Unsupported model: {model}")
    
    def test_attack(self, attack: str) -> str:

        if self.provider == "openai":
            return self._test_openai(attack)
        elif self.provider == "anthropic":
            return self._test_anthropic(attack)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def _test_openai(self, attack: str) -> str:

        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": attack}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _test_anthropic(self, attack: str) -> str:
        """Test attack against Anthropic model."""
        try:
            response = self.anthropic_client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[
                    {"role": "user", "content": attack}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
