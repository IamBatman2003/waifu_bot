from telethon import TelegramClient, events
import asyncio
import random

# === USER 1 CREDENTIALS ===
api_id_1 = 20326269
api_hash_1 = '03b46c9c32134a194f7e908fe0d1e986'
phone_1 = '+94704291133'

# === USER 2 CREDENTIALS ===
api_id_2 = 20700287
api_hash_2 = 'b891a147402520ddec8934adea2f10f9'
phone_2 = '+94757949309'

# === GROUP LINK ===
group_link = 'https://t.me/+Xtr_KT98qWA0Yzg1'

# === Clients ===
client_1 = TelegramClient('user1_session', api_id_1, api_hash_1)
client_2 = TelegramClient('user2_session', api_id_2, api_hash_2)

# === Control ===
spam_active = False
stop_event = asyncio.Event()

# === Emojis ===
emojis_user1 = ["💖", "🌸", "😊", "✨"]
emojis_user2 = ["🔥", "😎", "🎯", "💥"]

# === Function to Send Messages with Delay & Typing ===
async def send_limited_messages(client, phone, name, delay, emoji_list, max_messages, stop_event):
    await client.start(phone)
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
            await client.send_read_acknowledge(group)
            await client.send_message(group, f"{random.choice(emoji_list)} Message #{i+1}")
            print(f"[✅] {name} sent message {i+1}/{max_messages}")
            await asyncio.sleep(delay + random.uniform(0.2, 0.6))  # Extra randomness
        except Exception as e:
            print(f"[⚠️] {name} error: {e}")
            break

# === /START handler ===
@client_1.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    global spam_active
    if not spam_active:
        print("[🚀] Spamming started.")
        spam_active = True
        stop_event.clear()
        asyncio.create_task(send_limited_messages(client_1, phone_1, "User 1", 1.8, emojis_user1, 35, stop_event))
        asyncio.create_task(send_limited_messages(client_2, phone_2, "User 2", 2.0, emojis_user2, 35, stop_event))

# === /STOP handler ===
@client_1.on(events.NewMessage(pattern='/stop'))
async def stop_handler(event):
    global spam_active
    if spam_active:
        print("[🛑] Stopping spam.")
        spam_active = False
        stop_event.set()

# === Main ===
async def main():
    await client_1.start(phone_1)
    await client_2.start(phone_2)
    print("[✅] Waiting for /start and /stop...")
    await client_1.run_until_disconnected()

# === Run ===
asyncio.run(main())
