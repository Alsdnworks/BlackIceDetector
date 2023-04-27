import time

def ap():
    import network
    ssid = 'esp32_AP'
    password = '123456789'
    
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)
    
    print(ap.ifconfig())

def connect():
    import network  
    station = network.WLAN(network.STA_IF)
    time.sleep(2)
    if station.isconnected() == True:
        print("Already connected")
        return
    station.active(True)
    time.sleep(2)
    station.connect('iptime')
    time.sleep(2)

    print("Connection successful")
    print(station.ifconfig())
