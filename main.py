import os
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
TOKEN = os.environ.get("BOT_TOKEN")
DISCORD_LINK = "https://discord.gg/xesWFVH59m"
TIKTOK_LINK = "https://www.tiktok.com/@jordjostar52"

async def start_command(update, context):
    await update.message.reply_text(
        "👋 Привет! Я бот для приглашений\n\n"
        "📋 Команды:\n"
        "/discord - Discord сервер\n"
        "/tiktok - TikTok разработчика\n\n"
        "⚡ Напиши любое сообщение для получения ссылок!"
    )

async def discord_command(update, context):
    await update.message.reply_text(f"🎮 Discord: {DISCORD_LINK}")

async def tiktok_command(update, context):
    await update.message.reply_text(f"🎵 TikTok: {TIKTOK_LINK}")

async def handle_message(update, context):
    user_name = update.message.from_user.first_name
    await update.message.reply_text(
        f"🎉 Привет, {user_name}!\n\n"
        f"🔗 Наши сообщества:\n\n"
        f"🎮 Discord: {DISCORD_LINK}\n\n"
        f"🎵 TikTok: {TIKTOK_LINK}"
    )

async def post_init(application):
    await application.bot.set_webhook(url=os.environ.get("KOYEB_APP_URL") + "/webhook")

def main():
    logger.info("🚀 Starting Telegram Bot on Koyeb...")
    
    # Создаем Application
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("discord", discord_command))
    application.add_handler(CommandHandler("tiktok", tiktok_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Для Koyeb используем webhook
    koyeb_app_url = os.environ.get("KOYEB_APP_URL")
    if koyeb_app_url:
        logger.info("🤖 Using webhook mode")
        port = int(os.environ.get("PORT", 8000))
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TOKEN,
            webhook_url=f"{koyeb_app_url}/{TOKEN}"
        )
    else:
        logger.info("🤖 Using polling mode")
        application.run_polling()

if __name__ == '__main__':
    main()
