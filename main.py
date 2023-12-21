"""
    assign for start: https://my.telegram.org/auth?to=apps
"""
from telethon.sync import TelegramClient
from re import search


api_id = 0
api_hash = ""

groups_search = ["vaga", "emprego", "grup", "job", "talent", "prof", "ti", "it", "t.i"]
phares_search = ["python"]
search_p = lambda text: search("|".join(groups_search), text.lower())
search_j = lambda text: search("|".join(phares_search), text.lower())
LEN_LENGTH = 200


def write_file(data):
    with open("/tmp/jobs.txt", "a") as file:
        file.write(data)


with TelegramClient("anon", api_id, api_hash) as client:
    for dialog in client.iter_dialogs():
        if dialog.is_group and search_p(dialog.name):
            print(f"Group name: {dialog.name}")
            write_file("-" * LEN_LENGTH + "\n")
            write_file(f"Group name: {dialog.name}\n")
            for message in client.iter_messages(dialog.id, limit=1000):
                if (
                    message.text is not None
                    and len(message.text) > 0
                    and search_j(message.text)
                ):
                    write_file(f"{message.date} {message.text}\n")
                    print(f"Message: {message.text}")
                    write_file("-" * LEN_LENGTH + "\n")

            print("=" * LEN_LENGTH)
            write_file("=" * LEN_LENGTH + "\n")
