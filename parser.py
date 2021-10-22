import json
from pprint import pprint

import matplotlib.pyplot as plt
import pandas as pd
import xmltodict


def group_by(iterable: list[float], count: int, round_digits: int) -> list[int] | tuple[list[int], list[str]]:
    if count <= 1:
        return [len(iterable)]
    mi = min(iterable)
    ma = max(iterable)
    step = (ma - mi) / (count - 1)
    counts = [0 for _ in range(count)]
    for i in iterable:
        counts[round((i - mi) / step)] += 1
    labels = [
        f'{round(mi + i * step, round_digits)}-{round(mi + (i + 1) * step, round_digits)}'
        for i in range(len(counts))
    ]
    return counts, labels


def main():
    """
    Entry point of the parser.
    """

    with open('results/data.json', 'r') as file:
        data = json.load(file)
        print('Data from JSON:')
        pprint(data)
        print()

    with open('results/data.xml', 'r') as file:
        data = file.read()
        data = [dict(item) for item in xmltodict.parse(data)['data']['item']]
        print('Data from XML:')
        pprint(data)
        print()

    data_frame = pd.read_csv('results/data.csv')
    _, *lst = [data_frame[column].values.tolist() for column in data_frame]
    temperature, motion, voltage, time, case_number, *_ = lst

    temperature, labels = group_by(temperature, 4, 5)
    plt.xlabel('Интервалы температуры')
    plt.ylabel('Частота записей')
    plt.title('Температура')
    plt.xticks(range(len(temperature)), labels)
    plt.bar(range(len(temperature)), temperature)
    plt.show()

    plt.plot(motion)
    plt.ylabel('Значения движения')
    plt.xlabel('Номер измерения')
    plt.title('Движение')
    plt.show()

    v, labels = group_by(voltage, 5, 3)
    plt.pie(v, labels=labels, autopct=lambda x: round(x / 100 * len(voltage)))
    plt.xlabel('Интервалы напряжения')
    plt.title('Напряжение')
    plt.show()


if __name__ == '__main__':
    main()
