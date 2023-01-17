from machine import Pin
import dht


class DHT11:

    def __init__(self, pin_n):
        self.sensor = dht.DHT11(Pin(pin_n))

    def read(self):
        try:
            self.sensor.measure()
            temp = self.sensor.temperature()
            hum = self.sensor.humidity()
            return {
                "temp": temp,
                "hum": hum
            }
        except OSError as e:
            print(str(e))
            print('Failed to read sensor.')
            return {
                "temp": None,
                "hum": None
            }
