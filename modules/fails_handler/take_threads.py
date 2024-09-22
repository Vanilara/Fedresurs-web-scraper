from aiogram import Bot, Dispatcher, types, Router
from config import Config
import asyncio


r = Router()

@r.message()
async def handle_message(message: types.Message):
    thread_name = message.reply_to_message.forum_topic_created.name
    message_thread_id = message.message_thread_id
    print(f'{thread_name} = {message_thread_id}')

async def main():
    bot = Bot(token=Config.FailsHandler.TOKEN)
    dp = Dispatcher()
    dp.include_routers(r)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
