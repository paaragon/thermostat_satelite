import network
import time
import config

class Wifi:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password

    def connect(self):
        start_time = time.time()
        max_wait = config.MAX_CONN_TIME
        station = network.WLAN(network.STA_IF)

        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)

        station.active(True)
        station.connect(self.ssid, self.password)

        while station.isconnected() == False and time.time() - start_time < max_wait:
            pass

        if station.isconnected() == False:
            raise Exception()

        print('Connection successful')
        print(station.ifconfig())
