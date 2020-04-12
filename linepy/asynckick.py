import asyncio
from aiohttp import ClientSession

class AsyncKick:

    def __init__(self, client, groupId, midlist=list()):
        self.client = client
        self.execute(groupId, midlist)

    async def fetch(self, url, session, data, headers):
        async with session.post(url=url, data=data, headers=headers) as response:
            return await response.read()

    async def bound_fetch(self, sem, url, session, data, headers):
        async with sem:
            await self.fetch(url, session, data, headers)

    async def run(self, authToken, groupId, midlist):
        url = "https://legy-jp.line.naver.jp/S4"
        datas = []
        for mid in midlist:
            data = '\x82!\x00\x10kickoutFromGroup\x15\x00\x18!%s\x19\x18!%s\x00' % (groupId, mid)
            datas.append(data.encode('raw_unicode_escape'))
        headers = {
            'Content-Type': 'application/x-thrift',
            'User-Agent': 'Line/8.16.1',
            'X-Line-Application': "CHROMEOS 2.1.5 Mbah12.1.1",
            'Content-Length': str(len(datas[0])),
            'X-Line-Access': authToken
        }
        tasks = []
        sem = asyncio.Semaphore(1000)
        async with ClientSession() as session:
            for data in datas:
                task = asyncio.ensure_future(self.bound_fetch(sem, url, session, data, headers))
                tasks.append(task)
            responses = asyncio.gather(*tasks)
            await responses

    def execute(self, groupId, midlist=list()):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run(self.client.authToken, groupId, midlist))
        loop.run_until_complete(future)
