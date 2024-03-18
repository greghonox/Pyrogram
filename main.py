"""
    assign for start: https://my.telegram.org/auth?to=apps
"""

from os import getenv
from telethon.sync import TelegramClient
from re import search
from datetime import datetime, timezone, timedelta
from time import sleep
from telethon.errors import rpcerrorlist
import dotenv


dotenv.load_dotenv()


api_id = getenv("API_ID")
api_hash = getenv("API_HASH")

last_date = (datetime.now() - timedelta(days=0)).replace(
    tzinfo=timezone.utc, microsecond=0, second=0, minute=0, hour=0
)
phrase_match = [
    "remunera[ç|c][ã|a]o",
    "benef[í|i]cio",
    "curr[i|í]culo",
    "sal[á|a]rio",
    "requisitos",
    "candidat",
    "linkedin",
    "contato",
    "mail",
]
groups_search = [
    "vaga",
    "django",
    "emprego",
    "pug",
    "job",
    "talent",
    "prof",
    "ti",
    "it",
    "t.i",
    "floripa",
]
phares_no_search = ["hibrído", "hibrido", "presencial.?"]
phares_search = ["python"]

search_p = lambda text: search("|".join(groups_search), text.lower())
search_j = lambda text: search("|".join(phares_search), text.lower())
no_search = lambda text: not search("|".join(phares_no_search), text.lower())
phrase_match_f = lambda text: search("|".join(phrase_match), text.lower())

channel_send_message = [-1002088126719]
messages_read = []

LEN_LENGTH = 200


def write_file(data):
    with open("/tmp/jobs.txt", "a") as file:
        file.write(data)
        print(data)


def send_channel():
    print("publisher in channel")
    while len(messages_read) != 0:
        for channel in channel_send_message:
            try:
                message = messages_read.pop()
                client.send_message(channel, message)
                sleep(0.1)
            except rpcerrorlist.FloodWaitError as e:
                print(f"sleep {e.seconds} seconds, storage {len(messages_read)}")
                sleep(e.seconds)


with TelegramClient("anon", api_id, api_hash) as client:
    for dialog in client.iter_dialogs():
        if (dialog.is_group or dialog.is_channel) and search_p(dialog.name):
            write_file("-" * LEN_LENGTH + "\n")
            write_file(f"Group name: {dialog.name}\n")
            for message in client.iter_messages(dialog.id, limit=1000):
                date = message.date.replace(microsecond=0, second=0, minute=0, hour=0)
                if (
                    message.text is not None
                    and len(message.text) > 0
                    and search_j(message.text)
                    and no_search(message.text)
                    and phrase_match_f(message.text)
                    and date >= last_date
                ):
                    write_file(f"{message.date} {message.text}\n")
                    write_file("-" * LEN_LENGTH + "\n")

                    messages_read.append(f"{message.date} {message.text}\n")
                    messages_read.append(message.text)
            write_file("=" * LEN_LENGTH + "\n")
    messages_read = set(messages_read)
    write_file(f"Total jobs: {len(messages_read)}\n")
    send_channel()
