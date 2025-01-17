import asyncio
import logging

from pyrogram import Client
from pyrogram.enums import MessageEntityType
import json
import datetime

import settings
from urls_crowler.parsers import TGParser

log = logging.getLogger('ClientTelegramMaster')


class TGCrowler:
    def __init__(self, api_id, api_hash, phone_number, bot_token):
        self.client = Client(name='Session', api_id=api_id, api_hash=api_hash, phone_number=phone_number)
        self.phone_number = phone_number
        self.bot_token = bot_token
        self.parser = TGParser

    async def start_session(self):

        if not (await self.client.connect()):
            phone_hash = (await self.client.send_code(phone_number=self.phone_number)).phone_code_hash
            while not self.client.is_initialized:

                code = ''
                while code == '':
                    try:
                        with open('auth_code.json', 'r+') as code_json:
                            code = json.load(code_json)['code']

                    except Exception as e:
                        print(str(e))
                        await asyncio.sleep(5)
                try:
                    if code != 'error':
                        await self.client.sign_in(phone_number=self.phone_number, phone_code_hash=phone_hash,
                                                  phone_code=code)

                        return
                except Exception as e:
                    print(str(e))
                    with open('auth_code.json', 'w') as code_json:
                        code_json.seek(0)
                        json.dump({'code': 'error'}, code_json)
                        code_json.truncate()
                    await asyncio.sleep(27)
                await asyncio.sleep(3)
            await self.client.start()

    async def stop_session(self):
        await self.client.stop()

    async def run_crowl(self, redis_cache, chat_id, *args, **kwargs):
        await self.start_session()
        data = await self.get_data(donors_id=settings.donors_id)
        results, all_links = self.parser.parse_all_links(data, redis_cache, chat_id, *args, **kwargs)
        return results, all_links

    async def get_data(self, donors_id: list, limit=50) -> dict:
        with open('dates.json', 'r+') as dates_json:
            try:
                dates = json.load(dates_json)
            except Exception as e:
                dates = dict()
                log.warning(e)
            for _id in donors_id:
                if str(_id) not in dates.keys():
                    dates[str(_id)] = {'date': 0}

            dates_json.seek(0)
            json.dump(dates, dates_json)
            dates_json.truncate()

        data = await self.__parse_content(donor_id=donors_id[0], limit=limit)

        for _id in donors_id[1:]:
            data = await self.__parse_content(donor_id=_id, data=data, limit=limit)

        return data

    async def __parse_content(self, donor_id: int, limit=50, data=None) -> dict:
        if data is None:
            data = {}
        try:
            messages = self.client.get_chat_history(chat_id=donor_id, limit=limit)
            messages = [message async for message in messages][::-1]
            if str(donor_id) not in data.keys():
                data[str(donor_id)] = []
            with open('dates.json', 'r+') as dates_json:
                dates = json.load(dates_json)

                for message in messages:
                    if int(datetime.datetime.strptime(str(message.date), '%Y-%m-%d %H:%M:%S').timestamp()) <= \
                            int(dates[str(donor_id)]['date']):
                        continue

                    if message.caption_entities is not None:
                        links = [msg.url for msg in message.caption_entities if
                                 msg.type == MessageEntityType.TEXT_LINK and 't.me' not in msg.url]

                    else:
                        links = []

                    if message.caption is None:
                        if message.text is not None:
                            txt = message.text
                        else:
                            continue
                    else:
                        txt = message.caption

                    data[str(donor_id)].append({'caption': txt, 'links': links,
                                                'message_link': f"https://t.me/{message.chat.username}/{message.id}"})

                    dates[str(donor_id)]['date'] = int(
                        datetime.datetime.strptime(str(message.date), '%Y-%m-%d %H:%M:%S').timestamp())

                dates_json.seek(0)
                json.dump(dates, dates_json)
                dates_json.truncate()
        except Exception as e:
            logging.warning(e)

        return data
