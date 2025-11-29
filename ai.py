import os
from dotenv import load_dotenv
from openai import OpenAI
from db import add_message, get_user_history

load_dotenv()

OPENAI_KEY = os.getenv("openai_key")
client = OpenAI(api_key=OPENAI_KEY)


def ask_support_ai(user_text, user_id=None):
    if user_id:
        add_message(user_id, "user", user_text)
        history = get_user_history(user_id)
        messages_for_ai = [{"role": "system", "content": prompt}]
        for role, content in history:
            messages_for_ai.append({"role": role, "content": content})
    else:
        messages_for_ai = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_text}
        ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_text}
        ]
    )
    return response.choices[0].message.content