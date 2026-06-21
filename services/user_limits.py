import json
import os
from datetime import datetime
from config import settings

class UserLimitsManager:
    def __init__(self):
        self.limits_file = settings.USER_LIMITS_FILE
        self.max_questions = settings.MAX_QUESTIONS_PER_USER
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Убедиться, что файл лимитов существует"""
        if not os.path.exists(self.limits_file):
            with open(self.limits_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def get_user_limit(self, user_id: str) -> dict:
        """Получить информацию о лимите пользователя"""
        try:
            with open(self.limits_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if user_id in data:
                    return data[user_id]
                else:
                    return {"questions_asked": 0, "session_start": datetime.now().isoformat()}
        except Exception as e:
            return {"questions_asked": 0, "session_start": datetime.now().isoformat()}

    def increment_question_count(self, user_id: str) -> int:
        """Увеличить счётчик вопросов пользователя"""
        try:
            with open(self.limits_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if user_id not in data:
                data[user_id] = {
                    "questions_asked": 0,
                    "session_start": datetime.now().isoformat()
                }

            data[user_id]["questions_asked"] += 1
            data[user_id]["last_question"] = datetime.now().isoformat()

            with open(self.limits_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return data[user_id]["questions_asked"]
        except Exception as e:
            print(f"Error updating limits: {e}")
            return 1

    def can_ask_question(self, user_id: str) -> bool:
        """Проверить, может ли пользователь задать вопрос"""
        limit = self.get_user_limit(user_id)
        return limit.get("questions_asked", 0) < self.max_questions

    def get_remaining_questions(self, user_id: str) -> int:
        """Получить количество оставшихся вопросов"""
        limit = self.get_user_limit(user_id)
        asked = limit.get("questions_asked", 0)
        return max(0, self.max_questions - asked)

    def reset_user_limit(self, user_id: str):
        """Сбросить лимит пользователя (для администраторов)"""
        try:
            with open(self.limits_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if user_id in data:
                data[user_id]["questions_asked"] = 0
                data[user_id]["session_start"] = datetime.now().isoformat()

            with open(self.limits_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error resetting limit: {e}")

user_limits_manager = UserLimitsManager()
