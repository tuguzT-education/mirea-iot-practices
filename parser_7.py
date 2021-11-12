import json
from pprint import pprint

import xmltodict


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


if __name__ == '__main__':
    main()
