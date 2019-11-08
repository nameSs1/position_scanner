import asyncio
from pyppeteer import launch
import pyppeteer
from connection import Connection
from search_query import QueryList


user_agents = [
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/74.0.3729.169 Mobile Safari/537.36',
]


async def choose_by(page):
    await page.goto('https://www.google.by/')
    await page.xpath('.//a[text()="Настройки"]').click()
    await page.xpath('.//a[text()="Настройки поиска"]').click()
    await page.xpath('.//div[@id="regiontBY"]/div/span').click()
    await page.xpath('.//div[text()="Сохранить"]').click()  # .send_keys (u '\ ue007')
    await page.keyboard.press('Enter')  # driver.switch_to.alert.accept()


async def check_captcha_google(page):
    pass


async def search_google(page):
    pass


async def execute_requests_to_google(page, query):
    await choose_by(page)
    if not await check_captcha_google(page):
        return await search_google(page)


# def search_google(driver, use_req):  # Поиск в google
#     try:
#         with lock_g:
#             driver.get('https://www.google.by')
#             choose_by(driver)  # выбор в настройках гугл региона поиска
#         if check_captcha_google(driver):  # проверка на капчу
#             raise
#         page = driver.find_element(By.XPATH, ".//input[@title='Search' or @title='Поиск' or @title='Шукаць']")
#         page.send_keys(use_req.value_req)
#         page.send_keys(Keys.RETURN)
#         use_req.position_google, use_req.url_result_google = ran_pages_google(use_req, driver)
#     except:  # common.exceptions.NoSuchElementException
#         use_req.position_google, use_req.url_result_google = None, None


async def execute_requests_to_yandex(page, query):
    print('отработала execute_requests_to_yandex')


async def parser(connection):
    connection.ip = await connection.get_ip()
    while any((queries_for_google, queries_for_yandex)):
        browser = await launch(headless=False, slowMo=1000, args=[f'--proxy-server=socks5://{connection.host}:{connection.port}', ])
        page = await browser.newPage()
        await page.setViewport({"width": 1024, "height": 768})
        # await page.setUserAgent(user_agents[0])
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
