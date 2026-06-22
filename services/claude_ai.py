import os
import httpx
from knowledge.quantastrike_kb import SYSTEM_PROMPT, QUANTASTRIKE_KNOWLEDGE

class ClaudeAI:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        self.model = "claude-instant-1.2"
        self.api_url = "https://api.anthropic.com/v1/messages"

    async def get_response(self, user_message: str) -> str:
        try:
            system_prompt = SYSTEM_PROMPT.format(knowledge=QUANTASTRIKE_KNOWLEDGE)
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            payload = {
                "model": self.model,
                "max_tokens": 512,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_message}]
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, json=payload, headers=headers, timeout=30)
                if response.status_code != 200:
                    return f"❌ API error {response.status_code}: {response.text}"
                result = response.json()
                if "content" not in result or not result["content"]:
                    return "❌ Invalid API response"
                return result["content"][0]["text"]
        except Exception as e:
            return f"❌ Error: {str(e)}"

    async def check_relevance(self, question: str) -> bool:
        try:
            from knowledge.quantastrike_kb import RELEVANCE_CHECK_PROMPT
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            payload = {
                "model": self.model,
                "max_tokens": 10,
                "messages": [{"role": "user", "content": RELEVANCE_CHECK_PROMPT.format(question=question)}]
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, json=payload, headers=headers, timeout=30)
                if response.status_code != 200:
                    return True
                result = response.json()
                if "content" not in result or not result["content"]:
                    return True
                text = result["content"][0]["text"].strip().upper()
                return "ДА" in text
        except:
            return True

claude_ai = ClaudeAI()
