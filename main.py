import json


def load_json(file_json: str):
    """ В качестве входных параметров программа получает файл json. """
    try:
        with open(file_json, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except Exception as message:
        print('Ошибка загрузки json:', message)
        return False


input_json = load_json('goods.schema.json')
