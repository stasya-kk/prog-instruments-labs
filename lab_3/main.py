import csv
from pathlib import Path

from checksum import calculate_checksum, serialize_result
from validators import validate_row

VARIANT = 8
CSV_PATH = Path(__file__).parent / "8.csv"


def detect_encoding(csv_path: Path) -> str:
    """Определяет кодировку CSV по BOM в начале файла."""
    with csv_path.open("rb") as f:
        head = f.read(4)
    if head.startswith(b"\xff\xfe"):
        return "utf-16"        
    if head.startswith(b"\xfe\xff"):
        return "utf-16"       
    if head.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"      
    return "utf-8"               


def find_invalid_rows(csv_path: Path) -> list[int]:

    encoding = detect_encoding(csv_path)
    invalid_rows: list[int] = []
    with csv_path.open(encoding=encoding, newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row_index, row in enumerate(reader):
            if not validate_row(row):
                invalid_rows.append(row_index)
    return invalid_rows


def main() -> None:
    invalid_rows = find_invalid_rows(CSV_PATH)
    checksum = calculate_checksum(invalid_rows)
    serialize_result(VARIANT, checksum)

    print(f"Невалидных строк: {len(invalid_rows)}")
    print(f"Контрольная сумма: {checksum}")


if __name__ == "__main__":
    main()