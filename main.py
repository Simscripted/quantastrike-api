import uvicorn
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import settings
from services.claude_ai import claude_ai
from services.user_limits import user_limits_manager
from knowledge.quantastrike_kb import OFF_TOPIC_RESPONSE, LIMIT_EXCEEDED_RESPONSE

# ═══════════════════════════════════════════════
# FastAPI Application Setup
# ═══════════════════════════════════════════════

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="API для QuantaStrike Chat Support Assistant"
)

# ─────────────────────────────────────────────
# CORS Configuration (для веб-сайта)
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно ограничить до конкретных доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════
# Data Models
# ═══════════════════════════════════════════════

class ChatMessage(BaseModel):
    user_id: str  # Уникальный ID пользователя (session ID или IP)
    message: str  # Вопрос пользователя

class ChatResponse(BaseModel):
    success: bool
    response: str
    remaining_questions: int
    message_id: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str

# ═══════════════════════════════════════════════
# API Endpoints
# ═══════════════════════════════════════════════

@app.get("/", tags=["Health"])
@app.get("/health", tags=["Health"])
async def health_check() -> HealthResponse:
    """Проверка здоровья API"""
    return HealthResponse(
        status="✅ OK",
        version=settings.API_VERSION
    )

@app.post("/api/chat", tags=["Chat"])
def chat(message: ChatMessage) -> ChatResponse:
    """
    Получить ответ от QuantaStrike Chat Assistant

    - **user_id**: Уникальный идентификатор пользователя (session ID)
    - **message**: Вопрос пользователя
    """

    # Валидация
    if not message.user_id or not message.message:
        raise HTTPException(status_code=400, detail="user_id и message обязательны")

    if len(message.message) > settings.MAX_MESSAGE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Сообщение слишком длинное (макс {settings.MAX_MESSAGE_LENGTH} символов)"
        )

    # Проверить лимит
    if not user_limits_manager.can_ask_question(message.user_id):
        return ChatResponse(
            success=False,
            response=LIMIT_EXCEEDED_RESPONSE,
            remaining_questions=0
        )

    # Проверить релевантность вопроса
    is_relevant = claude_ai.check_relevance(message.message)

    if not is_relevant:
        # Увеличить счётчик даже для нерелевантного вопроса
        user_limits_manager.increment_question_count(message.user_id)
        remaining = user_limits_manager.get_remaining_questions(message.user_id)

        return ChatResponse(
            success=False,
            response=OFF_TOPIC_RESPONSE,
            remaining_questions=remaining
        )

    # Получить ответ от Claude
    response_text = claude_ai.get_response(message.message)

    # Увеличить счётчик вопросов
    question_count = user_limits_manager.increment_question_count(message.user_id)
    remaining = user_limits_manager.get_remaining_questions(message.user_id)

    return ChatResponse(
        success=True,
        response=response_text,
        remaining_questions=remaining,
        message_id=f"{message.user_id}_{question_count}"
    )

@app.get("/api/user/{user_id}/limits", tags=["User"])
async def get_user_limits(user_id: str):
    """Получить информацию о лимитах пользователя"""
    limit_info = user_limits_manager.get_user_limit(user_id)
    remaining = user_limits_manager.get_remaining_questions(user_id)

    return {
        "user_id": user_id,
        "questions_asked": limit_info.get("questions_asked", 0),
        "max_questions": settings.MAX_QUESTIONS_PER_USER,
        "remaining_questions": remaining,
        "session_start": limit_info.get("session_start"),
        "can_ask": user_limits_manager.can_ask_question(user_id)
    }

# ═══════════════════════════════════════════════
# Error Handlers
# ═══════════════════════════════════════════════

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return {
        "success": False,
        "error": "Внутренняя ошибка сервера",
        "details": str(exc)
    }

# ═══════════════════════════════════════════════
# Run Application
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )
