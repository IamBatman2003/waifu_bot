from telethon import TelegramClient, events
import asyncio
import random

# === USER SESSIONS ===
api_id_1 = 20326269
api_hash_1 = '03b46c9c32134a194f7e908fe0d1e986'

api_id_2 = 20700287
api_hash_2 = 'b891a147402520ddec8934adea2f10f9'

api_id_3 = 24906423
api_hash_3 = '9823ed5cf0dac9192b183bf61eef4e0d'

# === GROUP LINK ===
group_link = 'https://t.me/+7_bRIW46wjNjNjll'

# === AUTHORIZED USER IDS ===
allowed_user_ids = [1745055042, 7280186793]

# === INIT CLIENTS ===
client_1 = TelegramClient('user1_session', api_id_1, api_hash_1)
client_2 = TelegramClient('user2_session', api_id_2, api_hash_2)
client_3 = TelegramClient('user3_session', api_id_3, api_hash_3)

# === MESSAGES ===
user1_messages = [
    *["/XXXXXXXXXXXXXXXXXXXXX"] * 10,
    "Hey there!", "How’s it going?", "Anyone around?", "Feeling good 😊", "What's new?",
]

user2_messages = [
    *["/XXXXXXXXXXXXXXXXXXXXX"] * 10,
    "Yo!", "Let’s go!", "Ready to win!", "Who's next?", "Boom 💥",
]

user3_messages = [
    *["/XXXXXXXXXXXXXXXXXXXXX"] * 10,
    "Hi friends!", "Let's have fun!", "Good vibes!", "Where's everyone?", "Cheers 🥂",
]

# === STATE ===
spam_active = False
stop_event = asyncio.Event()

# === LOOP FUNCTION PER USER ===
async def loop_user_messages(client, name, messages):
    try:
        group = await client.get_entity(group_link)
        print(f"[✅] {name} joined group")
    except Exception as e:
        print(f"[❌] {name} join failed: {e}")
        return

    while not stop_event.is_set():
        msg_count = random.randint(2, 3)
        for _ in range(msg_count):
            if stop_event.is_set():
                break
            msg = random.choice(messages)
            try:
                await client.send_message(group, msg)
                print(f"[📨] {name} sent: {msg}")
            except Exception as e:
                print(f"[⚠️] {name} failed to send: {e}")
            await asyncio.sleep(random.uniform(0.6, 1.2))  # Short delay between messages
        await asyncio.sleep(random.uniform(1.5, 3.0))  # Short break between rounds

# === START COMMAND ===
async def start_handler(event):
    global spam_active
    sender = await event.get_sender()
    if sender.id not in allowed_user_ids:
        await event.respond("🚫 Unauthorized.")
        return
    if spam_active:
        await event.respond("⚠️ Already running.")
        return

    spam_active = True
    stop_event.clear()
    await event.respond("🚀 Spamming started (2–3 messages per loop).")

    await asyncio.gather(
        loop_user_messages(client_1, "User1", user1_messages),
        loop_user_messages(client_2, "User2", user2_messages),
        loop_user_messages(client_3, "User3", user3_messages),
    )

# === STOP COMMAND ===
async def stop_handler(event):
    global spam_active
    sender = await event.get_sender()
    if sender.id not in allowed_user_ids:
        await event.respond("🚫 Unauthorized.")
        return
    if not spam_active:
        await event.respond("⚠️ Not running.")
        return

    stop_event.set()
    spam_active = False
    await event.respond("🛑 Spamming stopped.")

# === REGISTER HANDLERS ===
for client in [client_1, client_2, client_3]:
    @client.on(events.NewMessage(pattern='(?i)^(/start|a)$'))
    async def _(event):
        await start_handler(event)

    @client.on(events.NewMessage(pattern='(?i)^(/stop|s)$'))
    async def _(event):
        await stop_handler(event)

# === MAIN RUNNER ===
async def main():
    await client_1.start()
    await client_2.start()
    await client_3.start()
    print("✅ All clients started. Use /start to begin, /stop to end.")
    await asyncio.gather(
        client_1.run_until_disconnected(),
        client_2.run_until_disconnected(),
        client_3.run_until_disconnected()
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Stopped manually.")
