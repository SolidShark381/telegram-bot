from flask import Flask
from threading import Thread
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import time
import json
import os
import logging
import asyncio

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Telegram Bot</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .container { max-width: 600px; margin: 0 auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Telegram Bot</h1>
            <p>Status: <strong>🟢 ONLINE</strong></p>
            <p>Running on Render.com 24/7</p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return "✅ OK"

@app.route('/ping')
def ping():
    return "pong"

# Функции бота
def get_uptime():
    seconds = int(time.time() - start_time)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}ч {minutes}м"

def load_users():
    try:
        if not os.path.exists('users.json'):
            return set()
        if os.path.getsize('users.json') == 0:
            return set()
        with open('users.json', 'r') as f:
            data = json.load(f)
            return set(data) if isinstance(data, list) else set()
    except:
        return set()

def save_users():
    try:
        with open('users.json', 'w') as f:
            json.dump(list(users_db), f)
    except:
        pass

def add_user(user_id):
    if user_id not in users_db:
        users_db.add(user_id)
        save_users()
        return True
    return False

def track_user(update, context):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    is_new_user = add_user(user_id)
    
    if is_new_user:
        print(f"🎉 Новый пользователь: {user_name}")
    
    return user_name, is_new_user

# КОНФИГУРАЦИЯ
TOKEN = os.environ.get('BOT_TOKEN', "8239093462:AAHx0SXFXUu45qvCTmz2PwQdPgggtxipot0")
DISCORD_LINK = "https://discord.gg/xesWFVH59m"
TIKTOK_LINK = "https://www.tiktok.com/@jordjostar52"

# Инициализация
start_time = time.time()
users_db = load_users()

# Команды бота
async def start_command(update, context):
    user_name, is_new_user = track_user(update, context)
    uptime = get_uptime()
    
    message = (
        f"👋 Привет, {user_name}! Я бот для приглашений\n\n"
        f"📋 **Команды:**\n"
        f"/discord - Discord сервер\n"
        f"/tiktok - TikTok разработчика\n"
        f"/stats - Статистика\n"
        f"/help - Помощь\n\n"
        f"📊 **Статистика:**\n"
        f"👥 Пользователей: {len(users_db)}\n"
        f"⏰ Работает: {uptime}\n\n"
        f"⚡ **Напиши любое сообщение для ссылок!**"
    )
    await update.message.reply_text(message, parse_mode='Markdown')

async def help_command(update, context):
    user_name, _ = track_user(update, context)
    message = "ℹ️ Просто напиши любое сообщение и получи ссылки на Discord и TikTok!"
    await update.message.reply_text(message)

async def discord_command(update, context):
    user_name, _ = track_user(update, context)
    message = f"🎮 **Присоединяйся к нашему Discord!**\n\n{DISCORD_LINK}"
    await update.message.reply_text(message, parse_mode='Markdown')

async def tiktok_command(update, context):
    user_name, _ = track_user(update, context)
    message = f"🎵 **Подписывайся на TikTok!**\n\n{TIKTOK_LINK}"
    await update.message.reply_text(message, parse_mode='Markdown')

async def stats_command(update, context):
    user_name, _ = track_user(update, context)
    uptime = get_uptime()
    message = (
        f"📊 **Статистика:**\n"
        f"👥 Пользователей: {len(users_db)}\n"
        f"⏰ Время работы: {uptime}\n"
        f"🚀 Хостинг: Render.com"
    )
    await update.message.reply_text(message, parse_mode='Markdown')

async def handle_all_messages(update, context):
    user_name, is_new_user = track_user(update, context)
    
    message = (
        f"🎉 **Привет, {user_name}!**\n\n"
        f"🔗 **Наши сообщества:**\n\n"
        f"🎮 **Discord:** {DISCORD_LINK}\n\n"
        f"🎵 **TikTok:** {TIKTOK_LINK}\n\n"
        f"✨ **Используй команды для быстрого доступа!**"
    )
    await update.message.reply_text(message, parse_mode='Markdown')

def run_flask():
    """Запускает Flask сервер на случайном порту"""
    try:
        # Используем порт из переменной окружения или случайный
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"❌ Ошибка Flask: {e}")

def run_bot():
    """Запускает Telegram бота"""
    try:
        # Создаем и настраиваем бота
        application = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("discord", discord_command))
        application.add_handler(CommandHandler("tiktok", tiktok_command))
        application.add_handler(CommandHandler("stats", stats_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_messages))
        
        print("=" * 50)
        print("🤖 Бот запущен на Render.com!")
        print(f"👥 Пользователей: {len(users_db)}")
        print("🌐 Web сервер активен")
        print("=" * 50)
        
        # Запускаем бота
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")

if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Даем время Flask запуститься
    time.sleep(2)
    
    # Запускаем бота в основном потоке
    run_bot()
