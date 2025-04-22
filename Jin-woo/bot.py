from telethon import TelegramClient, events
import asyncio
import random

# === USER 1 SESSION ===
api_id_1 = 20326269
api_hash_1 = '03b46c9c32134a194f7e908fe0d1e986'

# === USER 2 SESSION ===
api_id_2 = 20700287
api_hash_2 = 'b891a147402520ddec8934adea2f10f9'

# === GROUP LINK ===
group_link = 'https://t.me/+Xtr_KT98qWA0Yzg1'

# === ALLOWED USER IDs ===
allowed_user_ids = [1745055042, 7280186793]

# === Clients ===
client_1 = TelegramClient('user1_session', api_id_1, api_hash_1)
client_2 = TelegramClient('user2_session', api_id_2, api_hash_2)

# === Control ===
spam_active = False
stop_event = asyncio.Event()

# === Message Sets ===
user1_messages = [
    "Hey! How’s everything going?", "Good vibes only", "Anyone here today?",
    "I'm just chilling", "Hope your day’s going great", "Peace and love fam!",
    "Wassup crew?", "Haha that was funny!", "Where’s everyone at?", "Stay blessed!"
]

user2_messages = [
    "Yo! Ready to roll?", "Let’s get it started", "I’m back in action!",
    "Boom! Just like that!", "What’s up pirates?", "Target locked!",
    "Anyone up for a duel?", "Who's still awake?", "Always grinding", "Let's gooo!"
]

# === Function to Send Messages ===
async def send_limited_messages(client, name, delay, messages, max_messages, stop_event):
    try:
        group = await client.get_entity(group_link)
    except Exception as e:
        print(f"[❌] {name} failed to join group: {e}")
        return

    for i in range(max_messages):
        if stop_event.is_set():
            print(f"[🛑] {name} stopped early.")
            break
        try:
            message = random.choice(messages)
            await client.send_read_acknowledge(group)
            await client.send_message(group, message)
            print(f"[✅] {name} sent: {message}")
            await asyncio.sleep(delay + random.uniform(0.3, 0.8))
        except Exception as e:
            print(f"[⚠️] {name} error: {e}")
            break

# === Start Handler (Shared) ===
async def start_handler(event, sender_name):
    global spam_active
    sender = await event.get_sender()

    if sender.id not in allowed_user_ids:
        print(f"[🚫] Unauthorized user: {sender.id}")
        await event.respond("❌ You are not allowed to use this bot.")
        return

    if spam_active:
        await event.respond("⚠️ Already running.")
        return

    print(f"[🚀] Spamming started by {sender_name}.")
    await event.respond("✅ Spamming started.")
    spam_active = True
    stop_event.clear()

    # Start both spamming tasks
    asyncio.create_task(send_limited_messages(client_1, "User 1", 1.6, user1_messages, 50, stop_event))
    asyncio.create_task(send_limited_messages(client_2, "User 2", 1.8, user2_messages, 50, stop_event))

# === Stop Handler (Shared) ===
async def stop_handler(event, sender_name):
    global spam_active
    sender = await event.get_sender()

    if sender.id not in allowed_user_ids:
        print(f"[🚫] Unauthorized user tried to stop: {sender.id}")
        await event.respond("❌ You are not allowed to stop this bot.")
        return

    if not spam_active:
        await event.respond("⚠️ Bot is not running.")
        return

    print(f"[🛑] Spamming stopped by {sender_name}.")
    await event.respond("🛑 Bot stopped.")
    spam_active = False
    stop_event.set()

# === Bind Handlers to both clients ===
@client_1.on(events.NewMessage(pattern='/start'))
async def handle_start_1(event):
    await start_handler(event, "User 1")

@client_2.on(events.NewMessage(pattern='/start'))
async def handle_start_2(event):
    await start_handler(event, "User 2")

@client_1.on(events.NewMessage(pattern='/stop'))
async def handle_stop_1(event):
    await stop_handler(event, "User 1")

@client_2.on(events.NewMessage(pattern='/stop'))
async def handle_stop_2(event):
    await stop_handler(event, "User 2")

# === Main Function ===
async def main():
    await client_1.start()
    await client_2.start()

    if not await client_1.is_user_authorized() or not await client_2.is_user_authorized():
        print("[❌] Please authorize sessions with login_sessions.py")
        return

    print("[✅] Bot is ready. Waiting for /start or /stop commands...")
    await asyncio.gather(
        client_1.run_until_disconnected(),
        client_2.run_until_disconnected()
    )

# === Run Main ===
asyncio.run(main())
