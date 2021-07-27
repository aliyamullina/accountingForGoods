import json
import jsonschema
# Использовать либо sqlite3 либо postgres для хранения данных.
import sqlite3


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
    table_goods = [file_json['id'],
                   file_json['name'],
                   file_json['package_params']['height'],
                   file_json['package_params']['width']]

    table_shops_goods = []
    for i in file_json['location_and_quantity']:
        table_shops_goods.append([file_json['id'], i['location'], i['amount']])

    return tuple(table_goods), tuple(table_shops_goods)


def add_json_to_db(table_goods: tuple, table_shops_goods: tuple):
    """ Сохранение в базу в две таблицы. """
    conn = sqlite3.connect('goods.database.db')
    cursor = conn.cursor()

    # Приложение создаёт таблицы если они не созданы.
    cursor.execute("""CREATE TABLE IF NOT EXISTS goods (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    name            VARCHAR NOT NULL, 
                    package_height  FLOAT NOT NULL,
                    package_width   FLOAT NOT NULL);"""
                   )

    cursor.execute("""CREATE TABLE IF NOT EXISTS shops_goods (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_good         INTEGER NOT NULL, 
                    location        VARCHAR NOT NULL,
                    amount          INTEGER NOT NULL,
                    UNIQUE(id_good, location),
                    FOREIGN KEY (id_good) REFERENCES goods (id));"""
                   )
    conn.commit()

    # Приложение только вставляет данные, но не делает удаления.
    # Если пришли новые данные по предмету уже имеющемуся в базе — обновить.
    cursor.execute(f"""INSERT INTO goods (id, name, package_height, package_width) 
                            VALUES {table_goods}
                            ON CONFLICT(id) DO UPDATE SET 
                            name = EXCLUDED.name, 
                            package_width = EXCLUDED.package_width, 
                            package_height = EXCLUDED.package_height;"""
                   )
    conn.commit()

    for i in table_shops_goods:
        id_good, location, amount = i
        cursor.execute(f"""INSERT INTO shops_goods (id_good, location, amount)
                                VALUES {id_good, location, amount}
                                ON CONFLICT(id_good, location) DO UPDATE SET
                                amount = EXCLUDED.amount;"""
                       )
        conn.commit()
    conn.close()


def main():
    """ Старт приложения. """
    file_json = load_json('goods.file.json')
    file_schema = load_json('goods.schema.json')

    if validate_json_schema(file_json, file_schema):
        table_goods, table_shops_goods = prepare_json_to_db(file_json)
        add_json_to_db(table_goods, table_shops_goods)


main()
