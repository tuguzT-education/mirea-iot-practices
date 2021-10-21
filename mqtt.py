from typing import Final, Any

from paho.mqtt import client as mqtt_client


class Client(object):
    def __init__(self):
        self.__client_id: Final[str] = 'iot_practice_7'
        self.__host: Final[str] = '192.168.1.15'
        self.__port: Final[int] = 22
        self.__username: Final[str] = 'root'
        self.__password: Final[str] = 'wirenboard'

        self.__client = mqtt_client.Client(self.__client_id)
        self.__client.username_pw_set(self.__username, self.__password)
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        self.__client.on_publish = self.__on_publish
        self.__client.connect(self.__host, self.__port)

    def publish(self, device: str, control: str, payload: str):
        topic = generate_topic(device, control)

        result: mqtt_client.MQTTMessageInfo = self.__client.publish(topic, payload)
        self.__raise_error_if_any(result.rc)

    def subscribe(self, device: str, control: str):
        topic = generate_topic(device, control)

        result_code: int
        message_id: int | None
        result_code, message_id = self.__client.subscribe(topic)
        self.__raise_error_if_any(result_code)

    def unsubscribe(self, device: str, control: str):
        topic = generate_topic(device, control)

        result_code: int
        message_id: int | None
        result_code, message_id = self.__client.unsubscribe(topic)
        self.__raise_error_if_any(result_code)

    def loop(self, timeout: int):
        result_code = self.__client.loop(timeout)
        self.__raise_error_if_any(result_code)

    # noinspection PyUnusedLocal
    @staticmethod
    def __on_connect(client: mqtt_client.Client, userdata: Any, flags: Any, rc: int):
        result = mqtt_client.connack_string(rc)
        print(f'Connected with result "{result}"')

    # noinspection PyUnusedLocal
    @staticmethod
    def __on_disconnect(client: mqtt_client.Client, userdata: Any, rc: int):
        pass

    # noinspection PyUnusedLocal
    @staticmethod
    def __on_message(client: mqtt_client.Client, userdata: Any, message: mqtt_client.MQTTMessage):
        print(f'The message received: topic is "{message.topic}", payload is "{str(message.payload)}"')

    # noinspection PyUnusedLocal
    @staticmethod
    def __on_publish(client: mqtt_client.Client, userdata: Any, message_id: int):
        pass

    @staticmethod
    def __raise_error_if_any(error_code: int):
        if error_code != mqtt_client.MQTT_ERR_SUCCESS:
            error = mqtt_client.error_string(error_code)
            if error != "Unknown error.":
                raise MQTTException(error)


class MQTTException(Exception):
    def __init__(self, message: str):
        self.__message = message
        super().__init__(self.__message)

    def __str__(self) -> str:
        return f'MQTT exception: "{self.__message}"'

    def message(self) -> str:
        return self.__message


def generate_topic(device: str, control: str) -> str:
    return f'/devices/{device}/controls/{control}'
