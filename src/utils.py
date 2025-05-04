from datetime import datetime


def sorted_tuples_list(dict):
    return sorted(list(dict.items()), key=lambda tup: tup[1], reverse=True)


def add_key_to_dict(key: str, dict: dict):
    if key not in dict.keys():
        dict[key] = {}


def now_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def valid_years_range(years_range: tuple[int, int]) -> bool:
    if years_range and (
        years_range[0] > years_range[1]
        or years_range[0] < 2000
        or years_range[1] > datetime.now().year
    ):
        print(
            f"Years are not valid, given years: start year = {years_range[0]}, end year = {years_range[1]}"
        )
        return False
    return True


def valid_year(year: int) -> bool:
    return year >= 2000 and year <= datetime.now().year
