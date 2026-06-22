import os
from openai import OpenAI
from knowledge.quantastrike_kb import SYSTEM_PROMPT, QUANTASTRIKE_KNOWLEDGE

class ClaudeAI:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4-turbo"

    async def get_response(self, user_message: str) -> str:
        try:
            system_prompt = SYSTEM_PROMPT.format(knowledge=QUANTASTRIKE_KNOWLEDGE)
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=512,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Error: {str(e)}"

    async def check_relevance(self, question: str) -> bool:
        try:
            from knowledge.quantastrike_kb import RELEVANCE_CHECK_PROMPT
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=10,
                messages=[
                    {"role": "user", "content": RELEVANCE_CHECK_PROMPT.format(question=question)}
                ]
            )
            text = response.choices[0].message.content.strip().upper()
            return "ДА" in text
        except:
            return True

claude_ai = ClaudeAI()
