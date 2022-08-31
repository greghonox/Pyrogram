from pyrogram import Client
from datetime import datetime

data = lambda x: int(datetime.now().strftime(x))
api_id = 0
api_hash = ''

phrases_jobs = []
data_limit = datetime(data('%Y'), data('%m'), 1)
groups_ids = []

app = Client('search jobs', api_id=api_id, api_hash=api_hash)

async def main():
    async with app:
        for group in groups_ids:
            async for message in app.get_chat_history(group):
                if message.text is None or message.forward_date is None:
                    continue

                if any(phrase in message.text  for phrase in phrases_jobs):
                    print(message.text+'\n'+message.link)

                if message.forward_date < data_limit:
                    print(f'end {group}')
                    break
                print('-' * 100)

app.run(main())
