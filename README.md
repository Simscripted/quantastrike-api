# QuantaStrike Chat API

**Масштабируемый FastAPI сервер для QuantaStrike Chat Support Assistant** с интеграцией Claude AI.

## 🚀 Возможности

✅ Консультирует по продуктам QuantaStrike  
✅ Использует Claude AI для интеллектуальных ответов  
✅ Ограничение: 50 вопросов на пользователя  
✅ Проверка релевантности вопросов  
✅ CORS поддержка для веб-сайта  
✅ Асинхронная обработка запросов  
✅ Встроенная документация (Swagger UI)  

## 📋 Требования

- Python 3.8+
- pip

## 🔧 Установка

1. **Перейти в папку проекта:**
```bash
cd "C:\Users\tpsou\OneDrive\Desktop\Claude Code\quantastrike-api"
```

2. **Создать виртуальное окружение (опционально, но рекомендуется):**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Установить зависимости:**
```bash
pip install -r requirements.txt
```

## 🎯 Запуск сервера

```bash
python main.py
```

Сервер запустится на `http://localhost:8000`

**Документация API:** http://localhost:8000/docs (Swagger UI)

## 📡 API Endpoints

### 1. Health Check
```
GET /health
```
Проверка статуса сервера.

### 2. Chat Message
```
POST /api/chat
```
**Body:**
```json
{
  "user_id": "user123",
  "message": "Какой индикатор лучше для скальпинга?"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Для скальпинга рекомендуем Flow 2.0...",
  "remaining_questions": 49,
  "message_id": "user123_1"
}
```

### 3. Get User Limits
```
GET /api/user/{user_id}/limits
```
Получить информацию о лимитах пользователя.

## 🔌 Интеграция с веб-сайтом

В `chat-widget.js` замени функцию `sendMessage()`:

```javascript
async sendMessage() {
  const message = this.chatInput.value.trim();
  if (!message) return;

  this.chatInput.value = '';
  this.addMessage(message, true);

  // Get user session ID (можно использовать localStorage или IP)
  const userId = this.getUserId();

  try {
    const response = await fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        message: message
      })
    });

    const data = await response.json();

    if (data.success) {
      this.addMessage(data.response, false);
      this.updateRemainingQuestions(data.remaining_questions);
    } else {
      this.addMessage(data.response, false);
    }
  } catch (error) {
    this.addMessage('❌ Ошибка подключения к серверу', false);
  }
}

getUserId() {
  let userId = localStorage.getItem('quantastrike_user_id');
  if (!userId) {
    userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('quantastrike_user_id', userId);
  }
  return userId;
}
```

## 📦 Структура проекта

```
quantastrike-api/
├── main.py                 # FastAPI приложение
├── config.py               # Конфигурация
├── requirements.txt        # Зависимости
├── .env                    # Переменные окружения (API ключ)
├── services/
│   ├── claude_ai.py       # Интеграция с Claude API
│   └── user_limits.py     # Управление лимитами
├── knowledge/
│   └── quantastrike_kb.py # База знаний QuantaStrike
└── data/
    ├── user_limits.json   # Хранение лимитов
    └── chat_history.json  # История чатов (опционально)
```

## 🔐 Безопасность

- ✅ API ключ хранится в `.env` (не видно в коде)
- ✅ CORS настроен (можно ограничить до конкретного домена)
- ✅ Валидация входных данных
- ✅ Лимит на размер сообщения

## 🚀 Развертывание

### На локальной машине
```bash
python main.py
```

### На облачном сервере (например, Heroku)
1. Создать `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Deploy:
```bash
git push heroku main
```

### На Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## 📝 Логирование

Все запросы логируются в консоль. Для продвинутого логирования можно добавить:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Sentry для отслеживания ошибок
- CloudWatch для облачных решений

## 🔄 Будущие расширения

1. **Образовательный бот** - отдельный endpoint для обучения
2. **История чатов** - сохранение и анализ разговоров
3. **Аналитика** - метрики вопросов и ответов
4. **Multi-language** - поддержка разных языков
5. **Integrations** - подключение к CRM, Telegram, Slack
6. **Database** - переход на PostgreSQL для масштабирования

## 📞 Поддержка

Для вопросов и поддержки: @Simscripted (Telegram)

## 📄 Лицензия

QuantaStrike © 2026
