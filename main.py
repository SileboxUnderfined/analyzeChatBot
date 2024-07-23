from aiogram import Bot, Dispatcher, executor, types
import logging, os, aiosqlite
from botFuncs import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.environ['API_TOKEN'])
dp = Dispatcher(bot)

@dp.message_handler(commands=['start','help'])
async def send_welcome(message: types.Message):
    await message.reply('приветствую. Данный бот был создан @Silebox. Приятного использования.')

@dp.my_chat_member_handler()
async def added_bot(data):
    chat_id = data['chat']['id']
    async with aiosqlite.connect('data.db') as db:
        async with db.execute(f"SELECT * FROM chats WHERE chat_id={chat_id}") as cursor:
            result = await cursor.fetchall()
            if len(result) == 0:
                await db.execute(f"INSERT INTO chats (chat_id, mesages_counts) VALUES ({chat_id},0)")
                await db.commit()

            return
@dp.message_handler()
async def memorize_message(message: types.Message):
    print('keka')
    user_id = message.from_user.id
    username = message.from_user.username
    chat_id = message.chat.id
    text = message.text
    async with aiosqlite.connect('data.db') as db:
        async with db.execute(f"SELECT messages FROM users WHERE user_id={user_id}") as cursor:
            messages = await cursor.fetchall()
            print(messages)
            if len(messages) == 0:
                await db.execute(f"INSERT INTO users (user_id, messages, username, chat_id) VALUES ({user_id},{await addMessageToJSON(new_message=text)},{username},{chat_id})")

            else:
                await db.execute(f"UPDATE users SET messages = {await addMessageToJSON(new_message=text, messages=messages)} WHERE user_id = {user_id}")

            await db.commit()

if __name__ in "__main__":
    executor.start_polling(dp,skip_updates=True)