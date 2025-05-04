from datetime import datetime


def sorted_tuples_list(dict):
    return sorted(list(dict.items()), key=lambda tup: tup[1], reverse=True)


def add_key_to_dict(key: str, dict: dict):
    if key not in dict.keys():
        dict[key] = {}


def now_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
