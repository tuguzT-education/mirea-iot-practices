import mqtt


def main():
    client = mqtt.connect()
    mqtt.subscribe(client, device='wb-msw-v3_21', control='Temperature')
    client.loop(timeout=2)
    mqtt.unsubscribe(client, device='wb-msw-v3_21', control='Temperature')


if __name__ == '__main__':
    main()
