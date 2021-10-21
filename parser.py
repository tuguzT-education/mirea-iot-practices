import json
import xmltodict


def main():
    """
    Entry point of the parser.
    """

    with open('result.json', 'r') as file:
        data = json.load(file)
        print(f'Data from JSON: {data}')

    with open('result.xml', 'r') as file:
        data = file.read()
        data = dict(xmltodict.parse(data)['data'])
        print(f'Data from XML: {data}')


if __name__ == '__main__':
    main()
