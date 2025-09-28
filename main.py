from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Конфигурация
TOKEN = os.environ.get('BOT_TOKEN', "8239093462:AAHx0SXFXUu45qvCTmz2PwQdPgggtxipot0")
DISCORD_LINK = "https://discord.gg/xesWFVH59m"
TIKTOK_LINK = "https://www.tiktok.com/@jordjostar52"

# Команды бота
async def start_command(update, context):
    await update.message.reply_text(
        "👋 Привет! Я бот для приглашений\n\n"
        "📋 Команды:\n"
        "/discord - Discord сервер\n"
        "/tiktok - TikTok разработчика\n"
        "/help - Помощь\n\n"
        "⚡ Напиши любое сообщение для получения ссылок)"
    )

async def help_command(update, context):
    await update.message.reply_text(
        "ℹ️ Просто напиши любое сообщение и получи ссылки на Discord и TikTok!"
    )

async def discord_command(update, context):
    await update.message.reply_text(
        f"🎮 **Присоединяйся к нашему Discord!**\n\n{DISCORD_LINK}",
        parse_mode='Markdown'
    )

async def tiktok_command(update, context):
    await update.message.reply_text(
        f"🎵 **Подписывайся на TikTok!**\n\n{TIKTOK_LINK}",
        parse_mode='Markdown'
    )

async def handle_all_messages(update, context):
    user_name = update.message.from_user.first_name
    await update.message.reply_text(
        f"🎉 **Привет, {user_name}!**\n\n"
        f"🔗 **Наши сообщества:**\n\n"
        f"🎮 **Discord:** {DISCORD_LINK}\n\n"
        f"🎵 **TikTok:** {TIKTOK_LINK}\n\n"
        f"✨ Используй команды для быстрого доступа!",
        parse_mode='Markdown'
    )

def main():
    print("🚀 Starting Telegram Bot on Render...")
    
    try:
        # Создаем приложение бота
        application = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики команд
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("discord", discord_command))
        application.add_handler(CommandHandler("tiktok", tiktok_command))
        
        # Обработчик для всех текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_messages))
        
        print("✅ Bot configured successfully")
        print("🤖 Starting polling...")
        
        # Запускаем бота
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
