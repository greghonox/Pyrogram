from pyrogram import Client
from datetime import datetime

data = lambda x: int(datetime.now().strftime(x))
api_id = 0
api_hash = ''

phrases_jobs = ['python', 'django']
data_limit = datetime(data('%Y'), data('%m'), 1)
groups_ids = []

app = Client('search jobs', api_id=api_id, api_hash=api_hash)

async def main():
    with open('/tmp/jobs.txt', 'a') as f:
        async with app:
            for group in groups_ids:
                async for message in app.get_chat_history(group):
                    if message.text is None or message.forward_date is None:
                        continue

                    if any(phrase.lower() in message.text.lower()  for phrase in phrases_jobs):
                        job = f'{message.forward_date}\n{message.text}\n{message.link}\n'
                        print(job)
                        f.write(job)

                    if message.forward_date < data_limit:
                        print(f'end {group}')
                        break
                    print('-' * 100)
                    f.write('-' * 100 + '\n')

app.run(main())
