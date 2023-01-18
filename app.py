import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os

client = mqtt.Client()
influxClient = InfluxDBClient(url=os.environ.get('influx_url'),
                              token=os.environ.get('influx_token'),
                              org=os.environ.get('chill'))


def on_connect(client, userdata, flags, rc):
    print("Mqtt connected with result code " + str(rc))

    client.subscribe("sensors/trilsensor")
    client.subscribe("Temperatuur")


def on_message(client, userdata, msg):
    message = str(msg.payload.decode("utf-8"))
    if msg.topic == 'Temperatuur':
        p = Point("measurement").tag("sensor", "temperatuur").tag("component", 1).field("temperature", float(message))
        write_api.write(bucket='sensors', record=p)
    elif msg.topic == 'sensors/trilsensor':
        message_split = message.split(';')
        p = Point("measurement").tag("sensor", "tril").tag("component", 1).field("x", float(message_split[0])).field("y", float(message_split[1])).field("z", float(message_split[2]))
        write_api.write(bucket='sensors', record=p)


client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("chill", password=os.environ.get('mqtt_password'))
client.connect(os.environ.get('mqtt_host'), 1883, 60)
write_api = influxClient.write_api(write_options=SYNCHRONOUS)
query_api = influxClient.query_api()

if __name__ == "__main__":
    client.loop_forever()
