import os
from anthropic import Anthropic
from knowledge.quantastrike_kb import SYSTEM_PROMPT, QUANTASTRIKE_KNOWLEDGE

class ClaudeAI:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    async def get_response(self, user_message: str) -> str:
        """Получить ответ от Claude с контекстом QuantaStrike"""
        try:
            system_prompt = SYSTEM_PROMPT.format(knowledge=QUANTASTRIKE_KNOWLEDGE)
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            return message.content[0].text
        except Exception as e:
            return f"❌ Ошибка при обработке вашего вопроса: {str(e)}"

    async def check_relevance(self, question: str) -> bool:
        """Проверить релевантность вопроса к QuantaStrike"""
        try:
            from knowledge.quantastrike_kb import RELEVANCE_CHECK_PROMPT
            message = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": RELEVANCE_CHECK_PROMPT.format(question=question)}]
            )
            response = message.content[0].text.strip().upper()
            return "ДА" in response
        except Exception as e:
            return True

claude_ai = ClaudeAI()
