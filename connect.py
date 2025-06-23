import network
import rp2
import time

def connect(ssid: str, psk: str, country="GB", max_wait=30) -> network.WLAN:
    rp2.country(country)
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, psk)

    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print(f"Waiting for connection to {ssid}...")
        time.sleep(1)
    
    if wlan.status() != 3:
        raise RuntimeError(f"Network connection to {ssid} failed")
    else:
        print(f"Connected to {ssid} as {wlan.ifconfig()[0]}")
        
    return wlan
    
