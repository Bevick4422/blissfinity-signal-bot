from telegram import Bot
import asyncio

TOKEN = "8893369285:AAHi1aRkGG8AJ5M66C_cNVGAmTOn_gvtM9M"
CHAT_ID = "6953501418"

async def send_message():
    print("Starting bot...")

    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text="🚀 Blissfinity Signal Bot Connected Successfully!"
    )

    print("Message sent successfully!")

asyncio.run(send_message())