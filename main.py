from machine import Pin, unique_id
import config
from wifi import Wifi
from dht11 import DHT11
import time
import ubinascii
from mqtt import MQTT
import sys

"""
PIN_NUMBERS
"""
DHT_PIN = 4

"""
COMPONENTS DECLARATION
"""
dht_sensor = DHT11(DHT_PIN)

"""
MAIN VARIABLES
"""
sensor_latest_read = time.time()
lcd_display_latest_on = time.time()
curr_temp = None
curr_hum = None

local_client_id = ubinascii.hexlify(unique_id()).decode()
print("Starting " + str(local_client_id))

"""
INITIALIZING DHT11 SENSOR READ
"""
retry = 0
while curr_temp is None and retry < 5:
    result = dht_sensor.read()
    if result["temp"] is not None:
        curr_temp = result["temp"]
        curr_hum = result["hum"]
    else:
        time.sleep(2)
    retry += 1

if curr_temp is None:
    print("Error initializing sensor")
    sys.exit(1)

"""
CONNECTING WIFI
"""
wifi = Wifi(config.WIFI_SSID, config.WIFI_PASS)
try:
    wifi.connect()
except Exception as e:
    print(str(e))
    sys.exit(1)


"""
CONNECTING MQTT SERVER
"""
try:
    publish_read_topic = config.MQTT_TOPIC_PREFIX + \
        "/read/" + local_client_id
    mqtt_client = MQTT(local_client_id, None)
    mqtt_client.connect()
except (Exception, RuntimeError) as e:
    print(str(e))
    sys.exit(1)

publish_startup_topic = config.MQTT_TOPIC_PREFIX + \
    "/startup/" + local_client_id
mqtt_client.publish(publish_startup_topic, "Hello world!")
while True:
    mqtt_client.check_msg()

    # read the sensor
    if time.time() - sensor_latest_read > config.SENSOR_READ_DELAY_SEC:
        sensor_latest_read = time.time()
        result = dht_sensor.read()
        if result["temp"] is not None:
            curr_temp = result["temp"]
            curr_hum = result["hum"]
            mqtt_client.publish(publish_read_topic, str(result))
