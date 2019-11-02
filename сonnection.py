import asyncio
from aiohttp import ClientSession
from aiohttp_socks import SocksConnector, SocksVer


class Connection:
    def __init__(self, ports=(9050, 9051), host='127.0.0.1'):
        self.port = ports[0]
        self.control_port = ports[1]
        self.host = host
        self.ip = None

    async def change_ip(self):
        while True:
            await self._send_signal_change_ip()
            new_ip = await self._get_ip()
            new_ip = new_ip.strip()
            if self.ip != new_ip:
                self.ip = new_ip
                break
            await asyncio.sleep(1)

    async def _get_ip(self):
        connector = SocksConnector(socks_ver=SocksVer.SOCKS5, host=self.host, port=self.port, rdns=True)
        async with ClientSession(connector=connector) as session:
            async with session.get('http://icanhazip.com/') as response:
                return await response.text()

    async def _send_signal_change_ip(self):
        _, writer = await asyncio.open_connection(self.host, self.control_port)
        message = 'AUTHENTICATE\r\nSIGNAL NEWNYM\r\n'
        writer.write(message.encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
