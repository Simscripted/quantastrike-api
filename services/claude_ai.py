import anthropic
from config import settings
from knowledge.quantastrike_kb import SYSTEM_PROMPT, QUANTASTRIKE_KNOWLEDGE

class ClaudeAI:
    def __init__(self):
        self.client = None
        self.model = settings.CLAUDE_MODEL

    def _init_client(self):
        """Инициализировать клиент при первом использовании"""
        if self.client is None:
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY не установлен!")
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def get_response(self, user_message: str) -> str:
        """Получить ответ от Claude с контекстом QuantaStrike"""
        try:
            self._init_client()
            system_prompt = SYSTEM_PROMPT.format(knowledge=QUANTASTRIKE_KNOWLEDGE)

            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            return message.content[0].text
        except Exception as e:
            return f"❌ Ошибка при обработке вашего вопроса: {str(e)}"

    async def check_relevance(self, question: str) -> bool:
        """Проверить релевантность вопроса к QuantaStrike"""
        try:
            self._init_client()
            from knowledge.quantastrike_kb import RELEVANCE_CHECK_PROMPT

            message = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[
                    {"role": "user", "content": RELEVANCE_CHECK_PROMPT.format(question=question)}
                ]
            )

            response = message.content[0].text.strip().upper()
            return "ДА" in response
        except Exception as e:
            # Если ошибка, считаем вопрос релевантным (безопасный вариант)
            return True

claude_ai = ClaudeAI()
