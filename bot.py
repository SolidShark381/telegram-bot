import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Конфигурация
TOKEN = os.environ.get("BOT_TOKEN", "8239093462:AAHx0SXFXUu45qvCTmz2PwQdPgggtxipot0")
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

def main():
    print("🚀 Starting Telegram Bot on Railway...")
    
    # Создаем Application
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("discord", discord_command))
    application.add_handler(CommandHandler("tiktok", tiktok_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot configured successfully")
    print("🤖 Starting polling...")
    
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
