import mqtt


def main():
    client = mqtt.connect()
    client.loop_forever()


if __name__ == '__main__':
    main()
