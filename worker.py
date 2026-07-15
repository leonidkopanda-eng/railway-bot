from telethon import TelegramClient, events
import re
import logging
import os

logger = logging.getLogger(__name__)

api_id = 2040
api_hash = 'b18441a1ff607e10a989891a5462e627'
bot_username = 'PashaGiftsBot'
channel_username = 'PaulGifting'

password_pattern = re.compile(r'Пароль:\s*(.+)')
clients = []

async def add_session(name):
    try:
        session_path = f"sessions/{name}"
        os.makedirs("sessions", exist_ok=True)
        
        client = TelegramClient(session_path, api_id, api_hash)
        await client.start()
        clients.append(client)
        logger.info(f"Session {name} started successfully")

        @client.on(events.NewMessage(chats=channel_username))
        async def handler(event):
            try:
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
                    if password.lower() != "установлено":
                        clean_password = re.sub(r'[*`]', '', password).strip()
                        await client.send_message(bot_username, clean_password)
            except Exception as e:
                logger.error(f"Error in handler: {e}")
    except Exception as e:
        logger.error(f"Error adding session {name}: {e}")

async def start_all(accounts):
    for name in accounts:
        await add_session(name)

async def stop_all():
    for client in clients:
        try:
            await client.disconnect()
        except Exception as e:
            logger.error(f"Error disconnecting client: {e}")
    clients.clear()
    logger.info("All clients disconnected")
