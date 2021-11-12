import mqtt


def main():
    """
    Entry point of the client.
    """

    with mqtt.Client(case_number=14) as client:
        # Датчик температуры устройства WB-MSW v.3
        client.subscribe(device='wb-msw-v3_21', control='Temperature')
        # Датчик движения устройства WB-MSW v.3
        client.subscribe(device='wb-msw-v3_21', control='Current Motion')
        # Напряжение на любом устройстве стенда
        client.subscribe(device='wb-msw-v3_21', control='Input Voltage')

        client.start_dump()
        client.loop_forever()


if __name__ == '__main__':
    main()
