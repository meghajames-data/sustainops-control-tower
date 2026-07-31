from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def read_file(file_path: Path) -> pd.DataFrame:
    """Read CSV or Excel files."""

    extension = file_path.suffix.lower()

    if extension == ".csv":
        try:
            return pd.read_csv(file_path)
        except UnicodeDecodeError:
            return pd.read_csv(file_path, encoding="latin-1")

    if extension in {".xlsx", ".xls"}:
        return pd.read_excel(file_path)

    raise ValueError(f"Unsupported file type: {extension}")


def inspect_file(file_path: Path) -> None:
    """Print basic information about one dataset."""

    print("\n" + "=" * 80)
    print(f"FILE: {file_path.relative_to(PROJECT_ROOT)}")
    print("=" * 80)

    dataframe = read_file(file_path)

    print(f"Rows: {dataframe.shape[0]:,}")
    print(f"Columns: {dataframe.shape[1]}")

    print("\nColumn names:")
    for number, column in enumerate(dataframe.columns, start=1):
        print(f"{number}. {column}")

    print("\nData types:")
    print(dataframe.dtypes)

    print("\nMissing values:")
    missing = dataframe.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if missing.empty:
        print("No missing values.")
    else:
        print(missing)

    print("\nDuplicate rows:")
    print(dataframe.duplicated().sum())

    print("\nFirst five rows:")
    print(dataframe.head())


def main() -> None:
    supported_types = {".csv", ".xlsx", ".xls"}

    files = [
        file_path
        for file_path in RAW_DATA_DIR.rglob("*")
        if file_path.is_file()
        and file_path.suffix.lower() in supported_types
    ]

    if not files:
        print("No CSV or Excel files were found.")
        return

    print(f"Found {len(files)} dataset file(s).")

    for file_path in sorted(files):
        try:
            inspect_file(file_path)
        except Exception as error:
            print(f"\nCould not read {file_path.name}")
            print(f"Error: {error}")


if __name__ == "__main__":
    main()