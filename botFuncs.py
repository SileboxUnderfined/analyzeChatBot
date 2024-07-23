import json, aiosqlite

async def addMessageToJSON(new_message: str, messages: str = ""):
    if messages == "":
        result = json.dumps([new_message])
    else:
        loaded: list = json.loads(messages)
        loaded.append(new_message)
        result = json.dumps(loaded)

    return result

async def incrementMessageCount(chat_id):
    async with aiosqlite.connect('data.db') as db:
        async with db.execute(f"SELECT mesages_counts FROM chats WHERE chat_id = {chat_id}") as cursor:
            latest = cursor.fetchall()
            result = int(latest[0]) + 1
            await db.execute(f"UPDATE chats SET mesages_counts = {result} WHERE chat_id = {chat_id}")
            await db.commit()