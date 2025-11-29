import telebot
from tg_token import TOKEN
from menu import main_menu
from faq import FAQ, faq_keyboard
from ai import ask_support_ai

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! 👋 Я техподдержка AqmolaStart. Выбери действие:",
    reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "❓FAQ")
def show_faq(message):
    bot.send_message(
        message.chat.id,
        "Выберите вопрос из FAQ:",
        reply_markup=faq_keyboard()
    )

@bot.callback_query_handler(func=lambda call: call.data in FAQ.keys())
def faq_answer(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, FAQ[call.data])

@bot.message_handler(func=lambda m: m.text == "💬Задать вопрос")
def ask_support(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "Напишите свой вопрос:")
    bot.register_next_step_handler(message, support_reply)

def support_reply(message):
    bot.send_chat_action(message.chat.id, 'typing')
    answer = ask_support_ai(message.text, user_id=message.chat.id)
    bot.send_message(message.chat.id, answer, reply_markup=main_menu())

print("Бот запущен")
bot.polling()



