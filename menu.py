from telebot import types


def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("❓FAQ", "💬Задать вопрос")
    return kb


