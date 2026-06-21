/**
 * Обновленный код для интеграции chat-widget.js с QuantaStrike Chat API
 *
 * Замени функцию sendMessage() в chat-widget.js на следующее:
 */

// ═════════════════════════════════════════════════════════════
// КОНФИГУРАЦИЯ API
// ═════════════════════════════════════════════════════════════

const CHAT_API_CONFIG = {
  BASE_URL: 'http://localhost:8000',  // Или https://api.quantastrike.com на продакшене
  CHAT_ENDPOINT: '/api/chat',
  LIMITS_ENDPOINT: '/api/user'
};

// ═════════════════════════════════════════════════════════════
// МЕТОДЫ ПОЛЬЗОВАТЕЛЯ
// ═════════════════════════════════════════════════════════════

function getUserId() {
  /**
   * Получить или создать уникальный ID пользователя
   * Хранится в localStorage для сохранения лимитов между сеансами
   */
  let userId = localStorage.getItem('quantastrike_user_id');
  if (!userId) {
    userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('quantastrike_user_id', userId);
  }
  return userId;
}

function setUserLimitInfo(remaining) {
  localStorage.setItem('quantastrike_remaining_questions', remaining);
}

function getUserLimitInfo() {
  const remaining = localStorage.getItem('quantastrike_remaining_questions');
  return remaining ? parseInt(remaining) : 50;
}

// ═════════════════════════════════════════════════════════════
// ОСНОВНАЯ ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЯ
// ═════════════════════════════════════════════════════════════

async function sendMessageToAI(messageText) {
  /**
   * Отправить сообщение в QuantaStrike Chat API
   * Обрабатывает ответ и ошибки
   */

  const userId = getUserId();

  try {
    // Показать индикатор загрузки
    this.addMessage('🤖 Обрабатываю ваш вопрос...', false);

    // Отправить запрос к API
    const response = await fetch(`${CHAT_API_CONFIG.BASE_URL}${CHAT_API_CONFIG.CHAT_ENDPOINT}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        message: messageText
      })
    });

    // Удалить индикатор загрузки
    const messages = document.querySelectorAll('.chat-message');
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      if (lastMessage.textContent.includes('Обрабатываю')) {
        lastMessage.remove();
      }
    }

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    const data = await response.json();

    if (data.success) {
      // Успешный ответ
      this.addMessage(data.response, false);

      // Обновить информацию о лимитах
      setUserLimitInfo(data.remaining_questions);
      this.updateLimitInfo(data.remaining_questions);

      // Если это последние вопросы, предупредить пользователя
      if (data.remaining_questions <= 5 && data.remaining_questions > 0) {
        this.addMessage(
          `⚠️ У вас осталось ${data.remaining_questions} вопросов из 50`,
          false
        );
      }
    } else {
      // Нерелевантный вопрос или лимит исчерпан
      this.addMessage(data.response, false);

      if (data.remaining_questions !== undefined) {
        setUserLimitInfo(data.remaining_questions);
        this.updateLimitInfo(data.remaining_questions);
      }
    }
  } catch (error) {
    console.error('Chat API Error:', error);

    // Fallback на локальную логику если API недоступен
    this.addMessage(
      '❌ Ошибка подключения к серверу. Пожалуйста, попробуйте позже или напишите менеджеру @Simscripted',
      false
    );

    // Предложить альтернативные варианты
    this.addButton('👤 Менеджер', () => this.contactManager());
  }
}

function updateLimitInfo(remaining) {
  /**
   * Обновить отображение информации о лимитах в чате
   */
  const limitDisplay = document.getElementById('chat-limit-display');
  if (limitDisplay) {
    if (remaining > 0) {
      limitDisplay.innerHTML = `<small style="color: #7d8cff;">Осталось вопросов: ${remaining}/50</small>`;
    } else {
      limitDisplay.innerHTML = `<small style="color: #ff6b6b;">Лимит исчерпан</small>`;
    }
  }
}

// ═════════════════════════════════════════════════════════════
// ИНИЦИАЛИЗАЦИЯ ПРИ ЗАГРУЗКЕ
// ═════════════════════════════════════════════════════════════

async function initChatWidget() {
  /**
   * Инициализировать чат-виджет и загрузить информацию о лимитах
   */
  const userId = getUserId();

  try {
    const response = await fetch(
      `${CHAT_API_CONFIG.BASE_URL}${CHAT_API_CONFIG.LIMITS_ENDPOINT}/${userId}/limits`
    );

    if (response.ok) {
      const data = await response.json();
      setUserLimitInfo(data.remaining_questions);

      // Добавить информацию о лимитах в интерфейс чата
      const limitDisplay = document.createElement('div');
      limitDisplay.id = 'chat-limit-display';
      limitDisplay.style.padding = '8px 16px';
      limitDisplay.style.textAlign = 'center';
      limitDisplay.style.fontSize = '0.8rem';
      limitDisplay.style.color = '#7d8cff';
      limitDisplay.innerHTML = `Осталось вопросов: ${data.remaining_questions}/50`;

      const chatHeader = document.querySelector('.chat-header');
      if (chatHeader) {
        chatHeader.after(limitDisplay);
      }
    }
  } catch (error) {
    console.warn('Could not fetch user limits:', error);
  }
}

// ═════════════════════════════════════════════════════════════
// ИСПОЛЬЗОВАНИЕ
// ═════════════════════════════════════════════════════════════

/**
 * В файле chat-widget.js найди метод sendMessage() и замени его на:
 *
 * sendMessage() {
 *   const message = this.chatInput.value.trim();
 *   if (!message) return;
 *
 *   this.chatInput.value = '';
 *   this.addMessage(message, true);
 *
 *   sendMessageToAI.call(this, message);
 * }
 *
 * Также добавь в конструктор ChatWidget:
 *
 * constructor() {
 *   // ... существующий код ...
 *   initChatWidget();
 * }
 */
