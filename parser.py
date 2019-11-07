import asyncio
from pyppeteer import launch
import pyppeteer
from connection import Connection
from search_query import QueryList

URL = {'google': '', 'yandex': ''}
pyppeteer.DEBUG = True


async def execute_requests_to_google(page, query):
    return f"{page} {query}"


async def execute_requests_to_yandex(page, query):
    print('отработала execute_requests_to_yandex')


async def parser(connection):
    connection.ip = await connection.get_ip()
    while any((queries_for_google, queries_for_yandex)):
        browser = await launch(args=[f'--proxy-server=socks5://{connection.host}:{connection.port}', ])
        page = await browser.newPage()
        while queries_for_google:
            query = queries_for_google.pop()
            if result := await execute_requests_to_google(page, query):
                query.set_result(result)
            else:
                queries_for_google.append(query)
                break
        while queries_for_yandex:
            query = queries_for_yandex.pop()
            if result := await execute_requests_to_yandex(page, query):
                query.set_result(result)
            else:
                queries_for_yandex.append(query)
                break
        await browser.close()
        await connection.change_ip()


async def run_parsers():
    await asyncio.gather(*[parser(connection) for connection in connections])


if __name__ == '__main__':
    connections = [Connection(), ]
    queries = QueryList('test.json')
    queries_for_google, queries_for_yandex = queries.queries.copy(), queries.queries.copy()
    asyncio.run(run_parsers())
