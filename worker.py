from telethon import TelegramClient, events
import re

api_id = 2040
api_hash = 'b18441a1ff607e10a989891a5462e627'
bot_username = 'PashaGiftsBot'
channel_username = 'PaulGifting'

password_pattern = re.compile(r'Пароль:\s*(.+)')
clients = []

async def add_session(name):
    client = TelegramClient(f"sessions/{name}", api_id, api_hash)
    await client.start()
    clients.append(client)

    @client.on(events.NewMessage(chats=channel_username))
    async def handler(event):
        text = event.raw_text
        if event.message.buttons:
            for row in event.message.buttons:
                for button in row:
                    if button.url and "PashaGiftsBot?start=" in button.url:
                        code = button.url.split("start=")[-1]
                        await client.send_message(bot_username, f"/start {code}")
        pass_match = password_pattern.search(text)
        if pass_match:
            password = pass_match.group(1).strip()
            if password.lower() != "установлен":
                clean_password = re.sub(r'[*`]', '', password).strip()
                await client.send_message(bot_username, clean_password)

async def start_all(accounts):
    for name in accounts:
        await add_session(name)

async def stop_all():
    for client in clients:
        await client.disconnect()
    clients.clear()