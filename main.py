from telethon import TelegramClient, events

from message import help

api_id = 26993657
api_hash = "3a35758a62643189b63477aaee915a51"

client = TelegramClient("tagall_session", api_id, api_hash)


@client.on(events.NewMessage(pattern="/tagall"))
async def tag_all(event):
    chat = await event.get_chat()
    text = event.text.partition(" ")[2] if " " in event.text else "!!!"
    participants = await event.client.get_participants(await event.get_chat())
    mentions = ""
    for i in range(0, len(participants), 100):
        count = 0
        for m in participants[i : i + 100]:
            count += 1
            temp = "".join(f"[\u180E](tg://user?id={m.id}) ")
            mentions += temp
            if count == 5:
                await client.send_message(chat, f"**{text}** {mentions}")
                count = 0
                mentions = ""
        await client.send_message(chat, f"**{text}** {mentions}")
    await event.delete()
    await client.send_file(chat, "monke.gif")


@client.on(events.NewMessage(pattern="/tagone"))
async def tag_all(event):
    chat = await event.get_chat()
    text = event.text.partition(" ")[2] if " " in event.text else "внимание!"
    participants = await event.client.get_participants(await event.get_chat())
    for i in range(0, len(participants), 100):
        for m in participants[i : i + 100]:
            if m.is_self == False:
                mentions = "".join(f"[\u180E](tg://user?id={m.id}) ")
                await client.send_message(
                    chat, f"**{m.first_name}, {text}** {mentions}"
                )
    await event.delete()


@client.on(events.NewMessage(pattern="/help"))
async def help_modul(event):
    chat = await event.get_chat()
    await client.send_message(chat, f"{help}")
    await event.delete()


def main():
    client.start()
    client.run_until_disconnected()


if __name__ == "__main__":
    main()