import os
from typing import Optional
from dotenv import load_dotenv

# Загрузить переменные из .env файла
load_dotenv()

class Settings:
    # API Configuration
    API_TITLE = "QuantaStrike Chat API"
    API_VERSION = "1.0.0"

    # Claude API
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    CLAUDE_MODEL = "claude-haiku-4-5-20251001"

    # Limits
    MAX_QUESTIONS_PER_USER = 50
    MAX_MESSAGE_LENGTH = 2000

    # Timeouts
    CLAUDE_TIMEOUT = 30

    # Data paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    USER_LIMITS_FILE = os.path.join(DATA_DIR, "user_limits.json")
    CHAT_HISTORY_FILE = os.path.join(DATA_DIR, "chat_history.json")

    def __init__(self):
        try:
            os.makedirs(self.DATA_DIR, exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create data directory: {e}")

settings = Settings()
