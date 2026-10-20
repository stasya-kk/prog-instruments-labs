import re
from typing import Callable, Dict

TELEPHONE_RE = re.compile(r"^\+7-\(\d{3}\)-\d{3}-\d{2}-\d{2}$")

HEIGHT_RE = re.compile(r"^\d\.\d{2}$")

INN_RE = re.compile(r"^\d{12}$")

IDENTIFIER_RE = re.compile(r"^\d{2}-\d{2}/\d{2}$")

OCCUPATION_RE = re.compile(r"^[А-Яа-яЁёA-Za-z\s\-]+$")

LATITUDE_RE = re.compile(r"^-?\d+(\.\d+)?$")

BLOOD_TYPE_RE = re.compile(r"^(A|B|AB|O)[+\u2212]$")

ISSN_RE = re.compile(r"^\d{4}-\d{4}$")

UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def is_valid_telephone(value: str) -> bool:
    return bool(TELEPHONE_RE.match(value))


def is_valid_height(value: str) -> bool:
    if not HEIGHT_RE.match(value):
        return False
    height = float(value)
    return 0.5 <= height <= 2.5


def is_valid_inn(value: str) -> bool:
    return bool(INN_RE.match(value))


def is_valid_identifier(value: str) -> bool:
    return bool(IDENTIFIER_RE.match(value))


def is_valid_occupation(value: str) -> bool:
    if not OCCUPATION_RE.match(value):
        return False
    return bool(re.search(r"[А-Яа-яЁёA-Za-z]", value))


def is_valid_latitude(value: str) -> bool:
    if not LATITUDE_RE.match(value):
        return False
    latitude = float(value)
    return -90.0 <= latitude <= 90.0


def is_valid_blood_type(value: str) -> bool:
    return bool(BLOOD_TYPE_RE.match(value))


def is_valid_issn(value: str) -> bool:
    return bool(ISSN_RE.match(value))


def is_valid_uuid(value: str) -> bool:
    return bool(UUID_RE.match(value))


def is_valid_date(value: str) -> bool:
    if not DATE_RE.match(value):
        return False
    year, month, day = (int(part) for part in value.split("-"))
    if not (1 <= month <= 12):
        return False
    if not (1 <= day <= 31):
        return False
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    max_day = 29 if (month == 2 and leap) else days_in_month[month - 1]
    return day <= max_day


COLUMN_VALIDATORS: Dict[str, Callable[[str], bool]] = {
    "telephone": is_valid_telephone,
    "height": is_valid_height,
    "inn": is_valid_inn,
    "identifier": is_valid_identifier,
    "occupation": is_valid_occupation,
    "latitude": is_valid_latitude,
    "blood_type": is_valid_blood_type,
    "issn": is_valid_issn,
    "uuid": is_valid_uuid,
    "date": is_valid_date,
}


def validate_row(row: Dict[str, str]) -> bool:
    """Возвращает True, если все поля строки валидны."""
    for column, validator in COLUMN_VALIDATORS.items():
        value = row.get(column, "")
        if not validator(value):
            return False
    return True 