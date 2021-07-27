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


def validate_json_schema(file_json: dict, file_schema: dict):
    """ Происходит валидация входных данных."""
    try:
        jsonschema.validate(file_json, file_schema)
        return True
    except jsonschema.exceptions.ValidationError as message:
        print('Ошибка валидации json:', message)
        return False


def prepare_json_to_db(file_json: dict):
    """ Подготовка к сохранению в базу в две таблицы. """
    table_goods = [file_json['id'], file_json['name'], file_json['package_params']['height'], file_json['package_params']['width']]

    table_shops_goods = [file_json['id']]
    for i in file_json['location_and_quantity']:
        table_shops_goods.append(i['location'])
        table_shops_goods.append(i['amount'])

    return table_goods, table_shops_goods


def add_json_to_db(table_goods, table_shops_goods):
    """ Сохранение в базу в две таблицы. """
    # Приложение создаёт таблицы если они не созданы.
    # Приложение только вставляет данные, но не делает удаления.
    # Если пришли новые данные по предмету уже имеющемуся в базе — обновить.
    # Использовать либо sqlite3 либо postgre для хранения данных.


def main():
    """ Старт программы. """
    file_json = load_json('goods.file.json')
    file_schema = load_json('goods.schema.json')

    if validate_json_schema(file_json, file_schema):
        table_goods, table_shops_goods = prepare_json_to_db(file_json)
        add_json_to_db(table_goods, table_shops_goods)


main()
