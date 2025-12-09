import telebot
from telebot import types
import schedule
import time
import threading

TOKEN = "8346549546:AAG_rT-DjO1i9gfBk1T7s74MceYgqq5Tjbc"
bot = telebot.TeleBot(TOKEN)

# Har bir foydalanuvchi uchun ma'lumot
users = {}

# ========== START ==========
@bot.message_handler(commands=['start'])
def start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("👤 Login kiritish")
    kb.add("🔒 Parol kiritish")
    kb.add("⏰ Vaqt belgilash")
    kb.add("✅ Faollashtirish")

    bot.send_message(message.chat.id,
        "Xush kelibsiz!\nTugmalar orqali sozlang:",
        reply_markup=kb
    )

# ========== LOGIN ==========
@bot.message_handler(func=lambda m: m.text == "👤 Login kiritish")
def ask_login(message):
    bot.send_message(message.chat.id, "Login yuboring:")
    bot.register_next_step_handler(message, save_login)

def save_login(message):
    users.setdefault(message.chat.id, {})
    users[message.chat.id]["login"] = message.text
    bot.send_message(message.chat.id, "✅ Login saqlandi")

# ========== PASSWORD ==========
@bot.message_handler(func=lambda m: m.text == "🔒 Parol kiritish")
def ask_pass(message):
    bot.send_message(message.chat.id, "Parol yuboring:")
    bot.register_next_step_handler(message, save_pass)

def save_pass(message):
    users.setdefault(message.chat.id, {})
    users[message.chat.id]["password"] = message.text
    bot.send_message(message.chat.id, "✅ Parol saqlandi")

# ========== TIME ==========
@bot.message_handler(func=lambda m: m.text == "⏰ Vaqt belgilash")
def ask_time(message):
    bot.send_message(message.chat.id, "Soatni yuboring (masalan 08:00):")
    bot.register_next_step_handler(message, save_time)

def save_time(message):
    users.setdefault(message.chat.id, {})
    users[message.chat.id]["time"] = message.text
    bot.send_message(message.chat.id, f"✅ Vaqt saqlandi: {message.text}")

# ========== ACTIVATE ==========
@bot.message_handler(func=lambda m: m.text == "✅ Faollashtirish")
def activate(message):
    data = users.get(message.chat.id)

    if not data or "login" not in data or "password" not in data or "time" not in data:
        bot.send_message(message.chat.id, "❗ Avval hamma ma'lumotlarni kiriting")
        return

    t = data["time"]
    schedule.every().day.at(t).do(lambda: notify_user(message.chat.id))

    bot.send_message(message.chat.id, f"✅ Aktiv. Har kuni {t} da ishlaydi")

# ========== NOTIFICATION ==========
def notify_user(chat_id):
    bot.send_message(chat_id, "⏰ Vaqt keldi! emaktab.com ga kiring ✅")

# ========== LOOP ==========
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule).start()
bot.infinity_polling()
