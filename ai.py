import os
from openai import OpenAI
from db import add_message, get_user_history

OPENAI_KEY = os.getenv("openai_key")
client = OpenAI(api_key=OPENAI_KEY)

SYSTEM_PROMPT = """
Ты техподдержка приложения InfinityHub
Отвечай только по функционалу приложения, коротко и по делу
Если вопрос непонятный — спрашивай детали: телефон, ОС, версия приложения, что именно не работает
Не придумывай функций, которых нет и не отвечай на темы вне функционала InfinityHub
"""

def ask_support_ai(user_text, user_id=None):
    """
    Возвращает ответ AI на вопрос пользователя.
    Хранит историю диалогов, если указан user_id.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if user_id:
        add_message(user_id, "user", user_text)
        history = get_user_history(user_id, limit=10)
        for role, content in history:
            messages.append({"role": role, "content": content})
    else:
        messages.append({"role": "user", "content": user_text})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=messages
    )
    answer = response.choices[0].message.content
    if user_id:
        add_message(user_id, "assistant", answer)
    return answer
