import mqtt


def main():
    """
    Entry point of the program.
    """

    client = mqtt.Client(case_number=15)

    # Датчик температуры устройства WB-MSW v.3
    client.subscribe(device='wb-msw-v3_21', control='Temperature')
    # Датчик движения устройства WB-MSW v.3
    client.subscribe(device='', control='')
    # Датчик шума устройства WB-MSW v.3
    client.subscribe(device='', control='')
    # Датчик освещенности устройства WB-MS v.2
    client.subscribe(device='', control='')

    client.loop_forever()


if __name__ == '__main__':
    main()
