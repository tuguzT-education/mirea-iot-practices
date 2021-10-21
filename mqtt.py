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
        result = mqtt_client.connack_string(rc)
        print(f'Connected with result "{result}"')

    # noinspection PyUnusedLocal
    def on_disconnect(client: mqtt_client.Client, userdata: Any, rc: int):
        print('Disconnected')

    # noinspection PyUnusedLocal
    def on_message(client: mqtt_client.Client, userdata: Any, message: mqtt_client.MQTTMessage):
        print(f'The message received: topic is "{message.topic}", payload is "{str(message.payload)}"')

    new_client = mqtt_client.Client(client_id)
    new_client.username_pw_set(username, password)
    new_client.on_connect = on_connect
    new_client.on_disconnect = on_disconnect
    new_client.on_message = on_message

    new_client.connect(host, port)
    return new_client


def raise_error(error_code: int):
    if error_code != mqtt_client.MQTT_ERR_SUCCESS:
        error = mqtt_client.error_string(error_code)
        if error != "Unknown error.":
            raise Exception(error)


def generate_topic(device: str, control: str) -> str:
    return f'/devices/{device}/controls/{control}'


def publish(self: mqtt_client.Client, device: str, control: str, payload: str):
    topic = generate_topic(device, control)

    result: mqtt_client.MQTTMessageInfo = self.publish(topic, payload)
    raise_error(result.rc)


def subscribe(self: mqtt_client.Client, device: str, control: str):
    topic = generate_topic(device, control)

    rc: int
    message_id: int | None
    rc, message_id = self.subscribe(topic)
    raise_error(rc)


def unsubscribe(self: mqtt_client.Client, device: str, control: str):
    topic = generate_topic(device, control)

    rc: int
    message_id: int | None
    rc, message_id = self.unsubscribe(topic)
    raise_error(rc)
