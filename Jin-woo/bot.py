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
group_link = 'https://t.me/+7_bRIW46wjNjNjll'

# === ALLOWED USER IDs ===
allowed_user_ids = [1745055042, 7280186793]

# === Clients ===
client_1 = TelegramClient('user1_session', api_id_1, api_hash_1)
client_2 = TelegramClient('user2_session', api_id_2, api_hash_2)

# === Control ===
spam_active = False
stop_event = asyncio.Event()

# === USER 1 MESSAGES (Weighted) ===
user1_messages = [
    *["/XXXXXXXXXXXXXXXXXXXXX"] * 10,
    "Hey! How’s everything going?", "Good vibes only 🌈", "Anyone here today?",
    "I'm just chilling 🍃", "Hope your day’s going great!", "Peace and love fam! ✌️",
    "Wassup crew?", "Haha that was funny 😂", "Where’s everyone at?", "Stay blessed ✨"
]

# === USER 2 MESSAGES (Weighted) ===
user2_messages = [
    *["/XXXXXXXXXXXXXXXXXXXXX"] * 10,
    "Yo! Ready to roll?", "Let’s get it started 🎯", "I’m back in action!",
    "Boom! Just like that 💥", "What’s up pirates? 🏴‍☠️", "Target locked!",
    "Anyone up for a duel? ⚔️", "Who's still awake? 🕒", "Always grinding 💪", "Let's gooo!",
    "That was hilarious 😂"
]

# === Continuous Message Sending Function ===
async def send_continuous_messages(client, name, base_delay, messages, stop_event):
    try:
        group = await client.get_entity(group_link)
        print(f"[✅] {name} connected to group")
    except Exception as e:
        print(f"[❌] {name} group connection failed: {e}")
        return

    while not stop_event.is_set():
        try:
            message = random.choice(messages)
            await client.send_message(group, message)
            print(f"[📩] {name} sent: {message}")

            delay = base_delay + random.uniform(0.3, 0.8)
            await asyncio.sleep(delay)

        except Exception as e:
            print(f"[⚠️] {name} temporary error: {e}")
            await asyncio.sleep(5)

# === Command Handlers ===
async def start_handler(event):
    global spam_active
    sender = await event.get_sender()

    if sender.id not in allowed_user_ids:
        await event.respond("🚫 Unauthorized access!")
        return

    if spam_active:
        await event.respond("⚠️ Already spamming!")
        return

    spam_active = True
    stop_event.clear()

    asyncio.create_task(send_continuous_messages(client_1, "User1", 1.0, user1_messages, stop_event))
    asyncio.create_task(send_continuous_messages(client_2, "User2", 1.1, user2_messages, stop_event))

    await event.respond("🚀 Spamming STARTED!\n\n▶️ Messages will send continuously\n⏹ Use /stop to end")

async def stop_handler(event):
    global spam_active
    sender = await event.get_sender()

    if sender.id not in allowed_user_ids:
        await event.respond("🚫 Unauthorized access!")
        return

    if not spam_active:
        await event.respond("⚠️ Not currently active!")
        return

    spam_active = False
    stop_event.set()
    await event.respond("🛑 Spamming STOPPED!")

# === Register Commands ===
for client in [client_1, client_2]:
    @client.on(events.NewMessage(pattern='/start'))
    async def handle_start(event):
        await start_handler(event)

    @client.on(events.NewMessage(pattern='/stop'))
    async def handle_stop(event):
        await stop_handler(event)

# === Main Bot Runner ===
async def main():
    await client_1.start()
    await client_2.start()

    print("\n" + "=" * 40)
    print("🔰 SPAM BOT ACTIVE 🔰")
    print(f"👥 Monitoring {group_link}")
    print("⚡ Commands: /start | /stop")
    print("=" * 40 + "\n")

    await asyncio.gather(
        client_1.run_until_disconnected(),
        client_2.run_until_disconnected()
    )

# === Run Bot ===
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[🛑] Bot shutdown requested")
    finally:
        print("[🔴] Service terminated")
