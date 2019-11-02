import asyncio
from pyppeteer import launch
import pyppeteer


URL = {'google': '', 'yandex': ''}
pyppeteer.DEBUG = True


async def parser(ports=(9050, 9051), title='example1.png'):
    browser = await launch(args=[f'--proxy-server=socks5://127.0.0.1:{ports[0]}', ])
    page = await browser.newPage()
    await page.goto('https://2ip.ru/')
    await page.screenshot({'path': title})
    await browser.close()


async def execute_requests_to_google():
    pass


async def execute_requests_to_yandex():
    pass


async def main():
    await asyncio.gather(parser(), parser(ports=(9111, 9112), title='example2.png'))

# asyncio.get_event_loop().run_until_complete(main(), main((9065, 9066), 'example2.png'))
asyncio.run(main())
