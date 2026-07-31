from pathlib import Path
import re

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOGISTICS_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "supply_chain_logistics"
    / "Supply chain logistics problem.xlsx"
)

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def clean_column_name(column_name: str) -> str:
    """Convert a column name into lowercase snake_case."""

    cleaned = column_name.strip().lower()
    cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned)
    cleaned = cleaned.strip("_")

    return cleaned


def clean_text_columns(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Trim whitespace from text columns."""

    for column in dataframe.select_dtypes(
        include=["object", "string"]
    ).columns:
        dataframe[column] = (
            dataframe[column]
            .astype("string")
            .str.strip()
        )

    return dataframe


def load_and_clean_sheet(
    sheet_name: str,
) -> pd.DataFrame:
    """Load and perform basic cleaning on one worksheet."""

    dataframe = pd.read_excel(
        LOGISTICS_FILE,
        sheet_name=sheet_name,
    )

    dataframe.columns = [
        clean_column_name(column)
        for column in dataframe.columns
    ]

    dataframe = clean_text_columns(dataframe)
    dataframe = dataframe.drop_duplicates()

    return dataframe


def clean_order_list() -> pd.DataFrame:
    """Clean the logistics order sheet."""

    dataframe = load_and_clean_sheet("OrderList")

    dataframe["order_id"] = (
        dataframe["order_id"]
        .round()
        .astype("Int64")
        .astype("string")
    )

    dataframe["order_date"] = pd.to_datetime(
        dataframe["order_date"],
        errors="coerce",
    )

    dataframe["product_id"] = (
        dataframe["product_id"]
        .astype("Int64")
        .astype("string")
    )

    numeric_columns = [
        "tpt",
        "ship_ahead_day_count",
        "ship_late_day_count",
        "unit_quantity",
        "weight",
    ]

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

    dataframe = dataframe.dropna(
        subset=[
            "order_id",
            "order_date",
            "origin_port",
            "carrier",
            "plant_code",
            "destination_port",
        ]
    )

    dataframe["delivery_status"] = "On time"

    dataframe.loc[
        dataframe["ship_late_day_count"] > 0,
        "delivery_status",
    ] = "Late"

    dataframe.loc[
        dataframe["ship_ahead_day_count"] > 0,
        "delivery_status",
    ] = "Early"

    dataframe["is_late"] = (
        dataframe["ship_late_day_count"] > 0
    )

    dataframe["total_weight"] = dataframe["weight"]

    return dataframe.reset_index(drop=True)


def clean_freight_rates() -> pd.DataFrame:
    """Clean freight-rate data."""

    dataframe = load_and_clean_sheet("FreightRates")

    numeric_columns = [
        "minm_wgh_qty",
        "max_wgh_qty",
        "minimum_cost",
        "rate",
        "tpt_day_cnt",
    ]

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

    dataframe = dataframe.dropna(
        subset=[
            "carrier",
            "orig_port_cd",
            "dest_port_cd",
            "rate",
        ]
    )

    return dataframe.reset_index(drop=True)


def clean_simple_sheet(
    sheet_name: str,
) -> pd.DataFrame:
    """Clean smaller reference sheets."""

    return load_and_clean_sheet(
        sheet_name
    ).reset_index(drop=True)


def save_dataframe(
    dataframe: pd.DataFrame,
    filename: str,
) -> None:
    """Save a dataframe to the processed folder."""

    output_path = PROCESSED_DIR / filename

    dataframe.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Created {filename}: "
        f"{len(dataframe):,} rows"
    )


def main() -> None:
    """Clean all logistics workbook sheets."""

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    order_list = clean_order_list()
    freight_rates = clean_freight_rates()

    warehouse_costs = clean_simple_sheet(
        "WhCosts"
    )

    warehouse_capacities = clean_simple_sheet(
        "WhCapacities"
    )

    products_per_plant = clean_simple_sheet(
        "ProductsPerPlant"
    )

    vmi_customers = clean_simple_sheet(
        "VmiCustomers"
    )

    plant_ports = clean_simple_sheet(
        "PlantPorts"
    )

    save_dataframe(
        order_list,
        "logistics_orders_clean.csv",
    )

    save_dataframe(
        freight_rates,
        "freight_rates_clean.csv",
    )

    save_dataframe(
        warehouse_costs,
        "warehouse_costs_clean.csv",
    )

    save_dataframe(
        warehouse_capacities,
        "warehouse_capacities_clean.csv",
    )

    save_dataframe(
        products_per_plant,
        "products_per_plant_clean.csv",
    )

    save_dataframe(
        vmi_customers,
        "vmi_customers_clean.csv",
    )

    save_dataframe(
        plant_ports,
        "plant_ports_clean.csv",
    )

    print(
        "Logistics cleaning completed successfully."
    )


if __name__ == "__main__":
    main()