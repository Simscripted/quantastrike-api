# 🚀 Настройка QuantaStrike Chat API для сайта

## 📋 Краткая инструкция

### Шаг 1: Запустить API сервер

1. Открыть PowerShell/CMD в папке проекта:
```powershell
cd "C:\Users\tpsou\OneDrive\Desktop\Claude Code\quantastrike-api"
```

2. Установить зависимости (если ещё не установлены):
```bash
pip install -r requirements.txt
```

3. Запустить сервер:
```bash
python main.py
```

Или просто двойной клик на `run.bat`

Сервер запустится на **http://localhost:8000**

### Шаг 2: Проверить API

Откройте в браузере:
- **Документация**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Шаг 3: Интегрировать с веб-сайтом

#### Вариант A: Полная замена chat-widget.js

1. Открыть `C:\Users\tpsou\OneDrive\Desktop\Claude Code\quantastrike-site\chat-widget.js`

2. Найти метод `sendMessage()` (примерно на строке 948)

3. Заменить весь метод на:

```javascript
async sendMessage() {
  const message = this.chatInput.value.trim();
  if (!message) return;

  const userId = this.getUserId();
  this.chatInput.value = '';
  this.addMessage(message, true);

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
      if (data.remaining_questions <= 5 && data.remaining_questions > 0) {
        this.addMessage(`⚠️ Осталось ${data.remaining_questions} вопросов`, false);
      }
    } else {
      this.addMessage(data.response, false);
    }
  } catch (error) {
    console.error('Chat API Error:', error);
    this.addMessage('❌ Ошибка сервера. Попробуйте позже или напишите @Simscripted', false);
  }
}
```

4. Добавить метод `getUserId()` в класс ChatWidget (если его нет):

```javascript
getUserId() {
  let userId = localStorage.getItem('quantastrike_user_id');
  if (!userId) {
    userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('quantastrike_user_id', userId);
  }
  return userId;
}
```

#### Вариант B: Использовать готовый файл

1. Скопировать содержимое `chat-widget-integration.js` в `chat-widget.js`

2. Найти функцию `sendMessage()` и заменить её на вызов `sendMessageToAI.call(this, message)`

### Шаг 4: Тестировать

1. Открыть http://localhost:8000/theory.html (или другую страницу)
2. Кликнуть на чат-бот (синяя кнопка внизу справа)
3. Задать вопрос по QuantaStrike
4. Должен прийти ответ от Claude AI ✅

## ⚙️ Конфигурация для продакшена

### На локальной машине (разработка)
```
API_URL = http://localhost:8000
```

### На облачном сервере (продакшн)

1. Развернуть API на сервере (например, Heroku, AWS, DigitalOcean)

2. Обновить URL в chat-widget.js:
```javascript
const API_URL = 'https://api.quantastrike.com';  // Ваш реальный URL
```

3. Обновить CORS в `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://quantastrike.com", "https://www.quantastrike.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔍 Тестирование API

### Через curl

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "message": "Какой индикатор лучше для скальпинга?"
  }'
```

### Через Swagger UI

1. Откройте http://localhost:8000/docs
2. Найти POST `/api/chat`
3. Кликнуть "Try it out"
4. Заполнить параметры и нажать "Execute"

## 📊 Мониторинг

### Логи сервера

Все запросы логируются в консоли. Для сохранения логов:

```bash
python main.py > logs.txt 2>&1
```

### Информация о пользователях

Лимиты хранятся в:
```
C:\Users\tpsou\OneDrive\Desktop\Claude Code\quantastrike-api\data\user_limits.json
```

Формат:
```json
{
  "user_123": {
    "questions_asked": 15,
    "session_start": "2026-06-22T12:00:00",
    "last_question": "2026-06-22T12:15:30"
  }
}
```

## 🚨 Решение проблем

### API не запускается
```
❌ Error: Address already in use

Решение:
1. Порт 8000 занят. Закрыть другие приложения
2. Или запустить на другом порту: uvicorn main:app --port 8001
```

### "Connection refused"
```
❌ Connection refused at http://localhost:8000

Решение:
1. Убедиться, что API запущен
2. Проверить firewall
3. Открыть http://localhost:8000/health в браузере
```

### API ответивает ошибкой
```
❌ 500 Internal Server Error

Решение:
1. Проверить .env файл - есть ли API ключ
2. Проверить интернет подключение
3. Проверить логи в консоли
```

### Лимиты не работают
```
❌ Пользователь может задать более 50 вопросов

Решение:
1. Убедиться, что localStorage работает
2. Очистить браузер кэш/cookies
3. Открыть в новом приватном окне
```

## 📈 Будущие улучшения

- [ ] Сохранение истории чатов в базу данных
- [ ] Аналитика популярных вопросов
- [ ] Интеграция с Telegram для уведомлений
- [ ] WebSocket для real-time чата
- [ ] Кеширование ответов
- [ ] Автоматический апдейт базы знаний
- [ ] Мультиязычная поддержка

## 📞 Поддержка

Если есть проблемы:
1. Проверить логи (`python main.py`)
2. Открыть http://localhost:8000/docs и посмотреть документацию API
3. Написать менеджеру: @Simscripted

---

**Готово!** 🎉 API настроен и готов к использованию на сайте.
