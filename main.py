"""
    assign for start: https://my.telegram.org/auth?to=apps
"""
from pyrogram import Client
from datetime import datetime

data = lambda x: int(datetime.now().strftime(x))
api_id = 0
api_hash = ''

phrases_jobs = ['python', 'django', 'back end', 'rpa']
data_limit = datetime(data('%Y'), 10, 6)
groups_ids = [-1001052551532, -288176910, -1001052992679, -1001303593538,
              -1001150558288, -1001259501418, -1001393691685, -1001407720564,
              -1001436635321, -288176910, -1001715022220]

app = Client('search jobs', api_id=api_id, api_hash=api_hash)

async def get_dialogs():
    async with app:
        async for dialog in app.get_dialogs():
            print(dialog.chat.title or dialog.chat.first_name, dialog.chat.id)

jobs_search_link = []            
async def main():
    with open('/tmp/jobs.txt', 'a') as f:
        async with app:
            lenght_group = len(groups_ids)
            for e, group in enumerate(groups_ids):
                async for message in app.get_chat_history(group):
                    if message.text is None:
                        continue

                    if message.text.replace(' ', '').lower() in jobs_search_link:
                        continue
                    
                    if any(phrase.lower() in message.text.lower()  for phrase in phrases_jobs):
                        job = f'{message.date}\n{message.text}\n{message.link}\n' + '-' * 100 + '\n'
                        print(job)
                        f.write(job)
                        jobs_search_link.append(message.text.replace(' ', '').lower())

                    if message.date < data_limit:
                        print(f'end {message.chat.title} ({e+1}/{lenght_group})')
                        break                    
# app.run(get_dialogs())
app.run(main())
