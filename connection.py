import asyncio
from aiohttp import ClientSession
from aiohttp_socks import SocksConnector, SocksVer


class Connection:
    def __init__(self, ports=(9050, 9051), host='127.0.0.1'):
        self.port, self.control_port = ports
        self.host = host
        self.ip = None

    async def change_ip(self):
        while True:
            await self._send_signal_change_ip()
            new_ip = await self.get_ip()
            if self.ip != new_ip:
                self.ip = new_ip
                break

    async def get_ip(self):
        connector = SocksConnector(socks_ver=SocksVer.SOCKS5, host=self.host, port=self.port, rdns=True)
        async with ClientSession(connector=connector) as session:
            async with session.get('http://icanhazip.com/') as response:
                current_ip = await response.text()
                return current_ip.rstrip()

    async def _send_signal_change_ip(self):
        _, writer = await asyncio.open_connection(self.host, self.control_port)
        message = 'AUTHENTICATE\r\nSIGNAL NEWNYM\r\n'
        writer.write(message.encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        await asyncio.sleep(1)

    @classmethod
    def get_ports(cls, file='ports'):
        with open(file, 'r', encoding='utf-8') as file:
            ports = file.readlines()
        return list(map(lambda p: tuple(map(lambda i: int(i), (p.split()))), ports))
