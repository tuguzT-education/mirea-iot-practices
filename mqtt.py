from typing import Final, Any

from paho.mqtt import client as mqtt_client

client_id: Final[str] = 'iot_practice_7'
host: Final[str] = '192.168.1.15'
port: Final[int] = 22
username: Final[str] = 'root'
password: Final[str] = 'wirenboard'


def connect() -> mqtt_client.Client:
    # noinspection PyUnusedLocal
    def on_connect(client: mqtt_client.Client, userdata: Any, flags: Any, rc: int):
        if rc == 0:
            print("Connected to the MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    # noinspection PyUnusedLocal
    def on_message(client: mqtt_client.Client, userdata: Any, message: mqtt_client.MQTTMessage):
        print(f"{message.topic} {str(message.payload)}")

    new_client = mqtt_client.Client(client_id)
    new_client.username_pw_set(username, password)
    new_client.on_connect = on_connect
    new_client.on_message = on_message

    new_client.connect(host, port)
    return new_client
