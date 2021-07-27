import json
import jsonschema


def load_json(file_json: str):
    """ В качестве входных параметров программа получает файл json. """
    try:
        with open(file_json, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except Exception as message:
        print('Ошибка загрузки json:', message)
        return False


def validate_schema(add_json: dict, add_schema: dict):
    """ Происходит валидация входных данных."""
    try:
        jsonschema.validate(add_json, add_schema)
        return True
    except jsonschema.exceptions.ValidationError as message:
        print('Ошибка валидации json:', message)
        return False


def main():
    """ Старт программы. """
    add_json = load_json('goods.file.json')
    add_schema = load_json('goods.schema.json')
    validate_schema(add_json, add_schema)


main()
