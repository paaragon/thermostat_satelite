from umqttsimple import MQTTClient
import config


class MQTT:
    def __init__(self, id, sub_cb):
        self.id = id
        self.client = MQTTClient(id, config.MQTT_SERVER, keepalive=config.MQTT_KEEPALIVE)
        self.client.set_callback(sub_cb)

    def connect(self):
        self.client.connect()

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def check_msg(self):
        self.client.check_msg()

    def publish(self, topic, message):
        print("publishing message " + topic)
        self.client.publish(topic, message)
