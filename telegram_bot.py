from telegram import Bot
import asyncio
from config import TOKEN, CHAT_ID

async def send_message(message):

    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )