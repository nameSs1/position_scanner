import asyncio
from pyppeteer import launch
import pyppeteer
from connection import Connection
from search_query import QueryList

URL = {'google': '', 'yandex': ''}
pyppeteer.DEBUG = True


async def parser(connection, queue):
    connection.ip = await connection.get_ip()
    while not queue.empty():
        query = queue.get()
        browser = await launch(args=[f'--proxy-server=socks5://{connection.host}:{connection.port}', ])
        page = await browser.newPage()
        await execute_requests_to_google(page, query)
        await execute_requests_to_yandex(page, query)
        await browser.close()
        await connection.change_ip()


async def execute_requests_to_google(page, query):
    print('отработала execute_requests_to_google')


async def execute_requests_to_yandex(page, query):
    print('отработала execute_requests_to_yandex')


async def run_parsers():
    queue = asyncio.Queue()
    for query in queries:
        await queue.put(query)
    await asyncio.gather(*[parser(connection, queue) for connection in connections])


if __name__ == '__main__':
    connections = [Connection(), ]
    queries = QueryList('test.json')
    asyncio.run(run_parsers())
