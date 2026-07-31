from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOGISTICS_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "supply_chain_logistics"
    / "Supply chain logistics problem.xlsx"
)


def main() -> None:
    """Inspect all sheet names and dimensions in the logistics workbook."""

    workbook = pd.ExcelFile(LOGISTICS_FILE)

    print("Workbook sheets:")
    print("-" * 50)

    for sheet_name in workbook.sheet_names:
        dataframe = pd.read_excel(
            LOGISTICS_FILE,
            sheet_name=sheet_name,
        )

        print(f"\nSheet: {sheet_name}")
        print(f"Rows: {dataframe.shape[0]:,}")
        print(f"Columns: {dataframe.shape[1]}")
        print("Column names:")

        for number, column in enumerate(dataframe.columns, start=1):
            print(f"{number}. {column}")


if __name__ == "__main__":
    main()