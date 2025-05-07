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
group_link = 'https://t.me/+q04dFMa8tKdhNTU1'

# === ALLOWED USER IDs ===
allowed_user_ids = [1745055042, 7280186793]

# === Clients ===
client_1 = TelegramClient('user1_session', api_id_1, api_hash_1)
client_2 = TelegramClient('user2_session', api_id_2, api_hash_2)
client_3 = TelegramClient('user3_session', api_id_3, api_hash_3)

# === Control Flags ===
spam_active = False
stop_event = asyncio.Event()

# === USER MESSAGES ===
user1_messages = [
    "Hey, how’s it going?", "Just finished lunch 🍱", "Nice weather today!",
    "Haha that cracked me up 😂", "What’s everyone up to?", "Chillin' hard 😎",
    "I’m feeling lucky today 🍀", "Need a quick nap 💤", "LOL so true", "Who’s online?",
    "That was epic 💥"
]

user2_messages = [
    "Yo! Let’s get things moving 🚀", "Back at it again 🔁", "Coffee time ☕",
    "Did you guys see that? 😳", "Can't stop laughing 😂", "Grinding nonstop 💪",
    "This chat is lit 🔥", "Let’s keep the energy up!", "I’m hyped!", "That’s insane!",
    "Hold up, what?! 🤯"
]

user3_messages = [
    "Hey fam 👋", "What’s the mission today?", "Time to roll 🎲",
    "Good morning/afternoon/night everyone!", "On my way 🏃‍♂️", "Game on 🎮",
    "Haha no way 🤣", "Feeling pumped!", "Here we go again ⏳", "Let's make some noise!",
    "Checking in 📍"
]

# === Continuous Message Sending Function ===
async def send_messages_forever(client, name, messages, stop_event):
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
            await asyncio.sleep(random.uniform(0.7, 1.5))
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

    await event.respond("🚀 Spamming started (unlimited messages)...")

    await asyncio.gather(
        send_messages_forever(client_1, "User1", user1_messages, stop_event),
        send_messages_forever(client_2, "User2", user2_messages, stop_event),
        send_messages_forever(client_3, "User3", user3_messages, stop_event)
    )

    spam_active = False
    await event.respond("✅ Spamming stopped.")

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
def register_handlers(client):
    @client.on(events.NewMessage(pattern='(?i)^(/start|a)$'))
    async def handle_start(event):
        await start_handler(event)

    @client.on(events.NewMessage(pattern='(?i)^(/stop|s)$'))
    async def handle_stop(event):
        await stop_handler(event)

for client in [client_1, client_2, client_3]:
    register_handlers(client)

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
