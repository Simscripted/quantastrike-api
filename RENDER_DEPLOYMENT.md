# 🚀 Развертывание на Render

## Шаг 1: Подготовка GitHub репозитория

1. Создайте новый репозиторий на GitHub:
   - Перейдите на https://github.com/new
   - Назовите его `quantastrike-api`
   - Нажмите "Create repository"

2. Загрузите код в GitHub:
```bash
cd "C:\Users\tpsou\OneDrive\Desktop\Claude Code\quantastrike-api"
git init
git add .
git commit -m "Initial commit: QuantaStrike Chat API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/quantastrike-api.git
git push -u origin main
```

## Шаг 2: Развертывание на Render

1. **Перейдите на render.com**
   - Откройте https://render.com
   - Зарегистрируйтесь (или войдите)

2. **Создайте новый Web Service**
   - Нажмите "New +"
   - Выберите "Web Service"
   - Подключите GitHub репозиторий `quantastrike-api`
   - Нажмите "Connect"

3. **Настройте сервис**
   - **Name**: `quantastrike-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free` (или платный для лучшей производительности)

4. **Добавьте переменные окружения**
   - Перейдите на вкладку "Environment"
   - Нажмите "Add Environment Variable"
   - **Key**: `ANTHROPIC_API_KEY`
   - **Value**: `ВАШ_API_КЛЮЧ_CLAUDE_ЗДЕСЬ` (замените на свой API ключ)
   - Нажмите "Add"

5. **Развернуть**
   - Нажмите кнопку "Deploy"
   - Ждите завершения (обычно 2-5 минут)

## Шаг 3: Получить URL API

После развертывания вы получите URL вроде:
```
https://quantastrike-api-xxx.onrender.com
```

## Шаг 4: Обновить сайт

1. Откройте `chat-widget.js` в папке `quantastrike-site`

2. Найдите строку:
```javascript
const API_URL = 'http://localhost:8080';
```

3. Замените на:
```javascript
const API_URL = 'https://quantastrike-api-xxx.onrender.com';
```

4. Сохраните файл

## Шаг 5: Обновить CORS в main.py (опционально)

Если хотите ограничить доступ только к вашему домену:

1. Откройте `main.py`

2. Найдите:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
```

3. Замените на:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://quantastrike.com",
        "https://www.quantastrike.com",
        "http://localhost:3000"  # для локальной разработки
    ],
```

4. Сделайте новый коммит и push:
```bash
git add main.py
git commit -m "Update CORS for production"
git push
```

Render автоматически обновит сервис!

## ✅ Готово!

API работает в интернете! 🎉

**Проверьте:**
- https://quantastrike-api-xxx.onrender.com/health
- https://quantastrike-api-xxx.onrender.com/docs

## 🔍 Помощь

- Логи Render: https://dashboard.render.com → выберите сервис → "Logs"
- Документация Render: https://render.com/docs
- Проблемы с API ключом? Убедитесь, что переменная `ANTHROPIC_API_KEY` установлена в Environment

## 📝 Автоматические обновления

Каждый раз, когда вы делаете `git push` в GitHub:
1. Render автоматически отметит новый коммит
2. Перестроит приложение
3. Развернёт новую версию (без downtime)

Удобно для разработки! 🚀
