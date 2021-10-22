from __future__ import annotations

import copy
import datetime
import json
import pathlib
import threading
from typing import Final, Any
from xml.dom.minidom import parseString

import dicttoxml
import pandas as pd
from paho.mqtt import client as mqtt_client


class Client(object):
    """
    Class for MQTT operations on Wirenboard case.
    """

    def __init__(self, case_number: int):
        """
        Constructs instance of Client class with default host, port, username and password.

        :param case_number: number of the case to connect to.
        """
        self.__client_id: Final[str] = 'iot_practices'
        self.__case_number: Final[int] = case_number
        self.__host: Final[str] = f'192.168.1.{case_number}'
        self.__username: Final[str] = 'root'
        self.__password: Final[str] = 'wirenboard'
        self.__dump_interval: Final[float] = 5

        self.__client: Final[mqtt_client.Client] = mqtt_client.Client(self.__client_id)
        self.__client.username_pw_set(self.__username, self.__password)
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        self.__client.on_publish = self.__on_publish
        self.__client.user_data_set(self)

        result_code = self.__client.connect(self.__host)
        self.__raise_error_if_any(result_code)

        self.__timer: threading.Timer | None = None
        self.__data: Final[list[dict[str, Any]]] = list()
        self.__last_data: Final[dict[str, Any]] = dict()

    def __enter__(self) -> Client:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        self.stop_dump()

    def publish(self, device: str, control: str, payload: str):
        """
        Publishes new message to the specified device and control.

        :param device: todo
        :param control: todo
        :param payload: the message to be published
        """
        topic = f'{generate_topic(device, control)}/on'

        result: mqtt_client.MQTTMessageInfo = self.__client.publish(topic, payload)
        self.__raise_error_if_any(result.rc)

    def subscribe(self, device: str, control: str):
        """
        Subscribes to the topic defined by specified device and control.

        :param device: todo
        :param control: todo
        """
        topic = generate_topic(device, control)

        result_code: int
        message_id: int | None
        result_code, message_id = self.__client.subscribe(topic)
        self.__raise_error_if_any(result_code)

    def unsubscribe(self, device: str, control: str):
        """
        Unsubscribes from the topic defined by specified device and control.

        :param device: todo
        :param control: todo
        """
        topic = generate_topic(device, control)

        result_code: int
        message_id: int | None
        result_code, message_id = self.__client.unsubscribe(topic)
        self.__raise_error_if_any(result_code)

    def loop_forever(self, timeout: float = 1.0):
        """
        todo

        :param timeout: todo
        """

        result_code = self.__client.loop_forever(timeout)
        self.__raise_error_if_any(result_code)

    def __dump(self):
        """
        Dumps data retrieved from the subscribed MQTT channels to JSON and XML files.
        """
        self.start_dump()
        print('Dumping data...')

        time = str(datetime.datetime.now())
        self.__last_data['time'] = time
        self.__last_data['case_number'] = self.__case_number
        deepcopy = copy.deepcopy(self.__last_data)
        self.__data.append(deepcopy)

        pathlib.Path('results').mkdir(exist_ok=True)

        with open(f'results/data.json', 'w') as file:
            data = json.dumps(self.__data, indent=4)
            print(data, file=file)

        with open(f'results/data.xml', 'w') as file:
            data = dicttoxml.dicttoxml(self.__data, custom_root='data', attr_type=False)
            data = parseString(data).toprettyxml(indent=' ' * 4, encoding='UTF-8').decode('utf-8')
            print(data, file=file, end='')

        # noinspection PyTypeChecker
        pd.DataFrame(self.__data).to_csv('results/data.csv')

    def start_dump(self):
        """
        Starts dumping data retrieved from the subscribed MQTT channels.
        """
        self.stop_dump()
        self.__timer = threading.Timer(self.__dump_interval, self.__dump)
        self.__timer.start()

    def stop_dump(self):
        """
        Stops dumping data retrieved from the subscribed MQTT channels.
        """
        if self.__timer is not None:
            self.__timer.cancel()

    # noinspection PyUnusedLocal
    @staticmethod
    def __on_connect(client: mqtt_client.Client, self: Client, flags: Any, result_code: int):
        result = mqtt_client.connack_string(result_code)
        print(f'Connected with result "{result}"')

    # noinspection PyUnusedLocal
    @staticmethod
    def __on_disconnect(client: mqtt_client.Client, self: Client, result_code: int):
        pass

    # noinspection PyUnusedLocal
    @staticmethod
    def __on_message(client: mqtt_client.Client, self: Client, message: mqtt_client.MQTTMessage):
        topic = message.topic
        payload = message.payload.decode("utf-8")
        print(f'The message received: topic is "{topic}", payload is "{payload}"')

        key = topic.split('/')
        key: str = key[len(key) - 1].lower()
        self.__last_data[key] = payload

    # noinspection PyUnusedLocal
    @staticmethod
    def __on_publish(client: mqtt_client.Client, self: Client, message_id: int):
        pass

    @staticmethod
    def __raise_error_if_any(error_code: int):
        if error_code != mqtt_client.MQTT_ERR_SUCCESS:
            error = mqtt_client.error_string(error_code)
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
    """
    Generates topic from the device and control for Wirenboard.
    :param device: todo
    :param control: todo
    :return: valid topic for Wirenboard
    """
    return f'/devices/{device}/controls/{control}'
