#!/usr/bin/env python3
import os
import asyncio
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Конфигурация
TOKEN = "8239093462:AAHx0SXFXUu45qvCTmz2PwQdPgggtxipot0"
DISCORD_LINK = "https://discord.gg/xesWFVH59m"
TIKTOK_LINK = "https://www.tiktok.com/@jordjostar52"

async def start(update, context):
    await update.message.reply_text("👋 Привет! Напиши что-нибудь для ссылок!")

async def handle_message(update, context):
    text = f"🔗 Наши ссылки:\n\nDiscord: {DISCORD_LINK}\nTikTok: {TIKTOK_LINK}"
    await update.message.reply_text(text)

def main():
    print("🤖 Starting bot...")
    
    # Создаем Application
    app = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    print("✅ Bot started successfully!")
    
    # Запускаем polling
    app.run_polling()

if __name__ == '__main__':
    main()
