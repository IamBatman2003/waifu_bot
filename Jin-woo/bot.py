from telethon import TelegramClient, events
import asyncio
import random

# === USER 1 SESSION ===
api_id_1 = 20326269
api_hash_1 = '03b46c9c32134a194f7e908fe0d1e986'

# === USER 2 SESSION ===
api_id_2 = 20700287
api_hash_2 = 'b891a147402520ddec8934adea2f10f9'

# === USER 3 SESSION ===
api_id_3 = 24906423
api_hash_3 = '9823ed5cf0dac9192b183bf61eef4e0d'

# === GROUP LINK ===
group_link = 'https://t.me/+mtKgVsrcJg05ZmY1'

# === ALLOWED USER IDs ===
allowed_user_ids = [1745055042, 7280186793]

# === Clients ===
client_1 = TelegramClient('user1_session', api_id_1, api_hash_1)
client_2 = TelegramClient('user2_session', api_id_2, api_hash_2)
client_3 = TelegramClient('user3_session', api_id_3, api_hash_3)

# === Control Flags ===
spam_active = False
stop_event = asyncio.Event()

# === USER 1 MESSAGES ===
user1_messages = [
    *["/XXXXXXXXXXXXXXXXXXXXX"] * 10,
    "Hey! How’s everything going?", "Good vibes only 🌈", "Anyone here today?",
    "I'm just chilling 🍃", "Hope your day’s going great!", "Peace and love fam! ✌️",
    "Wassup crew?", "Haha that was funny 😂", "Where’s everyone at?", "Stay blessed ✨"
]

# === USER 2 MESSAGES ===
user2_messages = [
    *["/XXXXXXXXXXXXXXXXXXXXX"] * 10,
    "Yo! Ready to roll?", "Let’s get it started 🎯", "I’m back in action!",
    "Boom! Just like that 💥", "What’s up pirates? 🏴‍☠️", "Target locked!",
    "Anyone up for a duel? ⚔️", "Who's still awake? 🕒", "Always grinding 💪", "Let's gooo!",
    "That was hilarious 😂"
]

# === USER 3 MESSAGES ===
user3_messages = [
    *["/XXXXXXXXXXXXXXXXXXXXX"] * 10,
    "Hello team 👋", "Just checking in 🧐", "Let’s keep the vibes alive 💫",
    "Good morning crew ☀️", "All systems go 🚀", "We’re live 🔴",
    "Ready for action", "Haha love that 😄", "Stay awesome 🤙"
]

# === Send Messages Function ===
async def send_limited_messages(client, name, messages, stop_event, message_count=None):
    try:
        group = await client.get_entity(group_link)
        print(f"[✅] {name} connected to group")
    except Exception as e:
        print(f"[❌] {name} group connection failed: {e}")
        return

    if message_count is None:
        message_count = random.randint(2, 3)

    for _ in range(message_count):
        if stop_event.is_set():
            break
        try:
            message = random.choice(messages)
            await client.send_message(group, message)
            print(f"[📩] {name} sent: {message}")
            await asyncio.sleep(random.uniform(0.7, 1.3))
        except Exception as e:
            print(f"[⚠️] {name} error: {e}")
            await asyncio.sleep(2)

# === Start Handler ===
async def start_handler(event):
    global spam_active
    sender = await event.get_sender()

    if sender.id not in allowed_user_ids:
        await event.respond("🚫 Unauthorized access!")
        return

    if spam_active:
        await event.respond("⚠️ Already sending messages!")
        return

    spam_active = True
    stop_event.clear()

    await event.respond("🚀 Sending 2–3 messages per user...")

    await asyncio.gather(
        send_limited_messages(client_1, "User1", user1_messages, stop_event, message_count=2),
        send_limited_messages(client_2, "User2", user2_messages, stop_event, message_count=3),
        send_limited_messages(client_3, "User3", user3_messages, stop_event)  # random
    )

    spam_active = False
    await event.respond("✅ All messages sent.")

# === Stop Handler ===
async def stop_handler(event):
    global spam_active
    sender = await event.get_sender()

    if sender.id not in allowed_user_ids:
        await event.respond("🚫 Unauthorized access!")
        return

    if not spam_active:
        await event.respond("⚠️ Not currently sending!")
        return

    spam_active = False
    stop_event.set()
    await event.respond("🛑 Spamming STOPPED!")

# === Register Commands for All Clients ===
for client in [client_1, client_2, client_3]:

    @client.on(events.NewMessage(pattern='(?i)^(/start|a)$'))
    async def handle_start(event):
        await start_handler(event)

    @client.on(events.NewMessage(pattern='(?i)^(/stop|s)$'))
    async def handle_stop(event):
        await stop_handler(event)

# === Main Execution ===
async def main():
    await client_1.start()
    await client_2.start()
    await client_3.start()

    print("\n" + "=" * 50)
    print("🤖 MULTI-USER SPAM BOT READY")
    print(f"📍 Monitoring group: {group_link}")
    print("🛠️  Commands: /start | A | /stop | S")
    print("=" * 50 + "\n")

    await asyncio.gather(
        client_1.run_until_disconnected(),
        client_2.run_until_disconnected(),
        client_3.run_until_disconnected()
    )

# === Run Bot ===
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[🛑] Bot shutdown requested")
    finally:
        print("[🔴] Service terminated")
       
