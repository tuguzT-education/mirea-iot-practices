import mqtt


def main():
    client = mqtt.Client()
    client.subscribe(device='wb-msw-v3_21', control='Temperature')
    client.loop(timeout=2)
    client.unsubscribe(device='wb-msw-v3_21', control='Temperature')


if __name__ == '__main__':
    main()
