import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from ai.fallback import DeterministicIntentExtractor
from agents.state import CustomerIntent
from ai.prompts import INTENT_EXTRACTION_PROMPT

load_dotenv()

class LLMClient:
    """
    Unified LLM Client abstraction supporting OpenAI models with automatic
    deterministic fallback when API keys are not supplied.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = None

        if self.api_key and not self.api_key.startswith("your-"):
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except Exception:
                self.client = None

    @property
    def is_llm_active(self) -> bool:
        return self.client is not None

    def extract_intent(self, query: str) -> CustomerIntent:
        """Extract customer shopping intent using LLM or deterministic fallback."""
        if self.client:
            try:
                prompt = INTENT_EXTRACTION_PROMPT.format(query=query)
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You extract structured shopping parameters as valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.0
                )
                data = json.loads(response.choices[0].message.content)
                return CustomerIntent(
                    raw_query=query,
                    category=data.get("category"),
                    budget=data.get("budget"),
                    min_rating=data.get("min_rating"),
                    preferences=data.get("preferences", []),
                    confidence=0.98
                )
            except Exception:
                pass # Fallback to deterministic extraction on any network/API issue

        return DeterministicIntentExtractor.extract_intent(query)

    def generate_merchant_response(self, question: str, analytics_context: Dict[str, Any]) -> Optional[str]:
        """Optional LLM polishing of merchant analytics findings."""
        if not self.client:
            return None

        try:
            prompt = f"""
Merchant Question: "{question}"

Verified Database Telemetry Context:
{json.dumps(analytics_context, indent=2)}

Task: Present this verified data to the merchant in a clear, executive summary format.
DO NOT alter any numbers or invent statistics. Strictly report the provided metrics.
"""
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Razorpay AI Growth Copilot for merchants. Be concise and precise."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception:
            return None

llm_client = LLMClient()
