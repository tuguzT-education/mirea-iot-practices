import json
from pprint import pprint

import xmltodict
import pandas as pd


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
    time, case_number, temperature, motion, voltage, *_ = lst
    # print('Data from CSV:')
    # print(data_frame)


if __name__ == '__main__':
    main()
