# TODO: If you need to grow this class, consider moving to a sqlite3 database!

import io
import json

DATA_PATH = "data.json"


def __load_json_or_make_empty_object(fp: io.TextIOWrapper):
    data = {}
    fp.seek(0)
    try:
        data = json.load(fp)
    except ValueError as exception:
        print(exception, DATA_PATH, "wasn't a JSON file, making it one...")
        # fp doesn't point to a file with valid json, replacing the content with "{}"
        fp.seek(0)
        fp.write("{}")
        fp.truncate()
        fp.flush()
        return {}
    return data


def get_data() -> dict:
    with open(DATA_PATH, 'a+') as fp:
        return __load_json_or_make_empty_object(fp)


# Helper class for writing to the data file in a sage way
class DataWriter:
    def __init__(self) -> None:
        self.__data_fp: io.TextIOWrapper | None = None

    def __enter__(self):
        self.__data_fp = open(DATA_PATH, 'w+')
        return self

    def __exit__(self, *_):
        if self.__data_fp is not None:
            self.__data_fp.close()

    # Set a new value to the data
    def set_data(self, json_data: dict):
        if self.__data_fp is None:
            return

        self.__data_fp.seek(0)
        json.dump(json_data, self.__data_fp)
        self.__data_fp.truncate()
        self.__data_fp.flush()
