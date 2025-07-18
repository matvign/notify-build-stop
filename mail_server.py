# mail_server.py
import asyncio
import os
from aiosmtpd.controller import Controller

smtp_host = os.getenv('smtp_host', 'localhost')
smtp_port = os.getenv('smtp_port', 1025)

class PrintHandler:
    async def handle_DATA(self, server, session, envelope):
        print("Email received:", envelope.content.decode())
        return "250 Message accepted for delivery"

controller = Controller(PrintHandler(), hostname=smtp_host, port=smtp_port)
controller.start()

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    controller.stop()
