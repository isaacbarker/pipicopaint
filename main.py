from connect import connect
from server import serve_client
from machine import Pin
import uasyncio as asyncio
from config import SSID, PSK, COUNTRY

onboard = Pin("LED", Pin.OUT, value=0)

async def main():
    print("Connecting to network...")
    wlan = connect(SSID, PSK, COUNTRY)

    print(f"Webserver listening on http://{wlan.ifconfig()[0]}:80")
    asyncio.create_task(
        asyncio.start_server(
            serve_client,
            "0.0.0.0",
            80
        )
    )

    # heartbeat
    while True:
        onboard.high()
        await asyncio.sleep(1)
        onboard.low()
        await asyncio.sleep(1)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()