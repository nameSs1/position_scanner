import asyncio
from pyppeteer import launch
import pyppeteer


URL = {'google': '', 'yandex': ''}
pyppeteer.DEBUG = True


async def parser(port=9050, host='127.0.0.1'):
    browser = await launch(args=[f'--proxy-server=socks5://{host}:{port}', ])
    page = await browser.newPage()
    # await page.goto('https://2ip.ru/')
    # await page.screenshot({'path': title})
    # await browser.close()


async def execute_requests_to_google():
    pass


async def execute_requests_to_yandex():
    pass


async def run_parsers():
    queue = asyncio.Queue()
    await asyncio.gather(parser(), parser(port=9052))


if __name__ == '__main__':
    asyncio.run(run_parsers())
