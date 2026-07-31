from pathlib import Path
import re

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SMART_MANUFACTURING_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "smart_manufacturing"
    / "smart_manufacturing_dataset.csv"
)

STEEL_ENERGY_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "steel_energy"
    / "Steel_industry_data.csv"
)

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def clean_column_name(column_name: str) -> str:
    """Convert a column name into lowercase snake_case."""

    cleaned = column_name.strip().lower()
    cleaned = re.sub(r"[%()]", "", cleaned)
    cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned)
    cleaned = cleaned.strip("_")

    return cleaned


def clean_smart_manufacturing() -> pd.DataFrame:
    """Clean the smart-manufacturing dataset."""

    dataframe = pd.read_csv(SMART_MANUFACTURING_FILE)

    dataframe.columns = [
        clean_column_name(column)
        for column in dataframe.columns
    ]

    dataframe["timestamp"] = pd.to_datetime(
        dataframe["timestamp"],
        errors="coerce"
    )

    text_columns = [
        "machine_id",
        "material_category",
        "material_name",
    ]

    for column in text_columns:
        dataframe[column] = (
            dataframe[column]
            .astype("string")
            .str.strip()
        )

    numeric_columns = [
        "quantity_used_kg",
        "recycled_material",
        "energy_consumption_kwh",
        "production_output_units",
        "defect_rate",
    ]

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )

    dataframe = dataframe.drop_duplicates()

    dataframe = dataframe.dropna(
        subset=[
            "timestamp",
            "machine_id",
            "energy_consumption_kwh",
            "production_output_units",
        ]
    )

    dataframe = dataframe[
        (dataframe["quantity_used_kg"] >= 0)
        & (dataframe["energy_consumption_kwh"] >= 0)
        & (dataframe["production_output_units"] >= 0)
        & (dataframe["recycled_material"].between(0, 100))
        & (dataframe["defect_rate"].between(0, 100))
    ]

    dataframe["energy_intensity_kwh_per_unit"] = (
        dataframe["energy_consumption_kwh"]
        / dataframe["production_output_units"].replace(0, pd.NA)
    )

    dataframe["estimated_defective_units"] = (
        dataframe["production_output_units"]
        * dataframe["defect_rate"]
        / 100
    )

    dataframe["material_efficiency_units_per_kg"] = (
        dataframe["production_output_units"]
        / dataframe["quantity_used_kg"].replace(0, pd.NA)
    )

    dataframe = dataframe.sort_values("timestamp").reset_index(drop=True)

    return dataframe


def clean_steel_energy() -> pd.DataFrame:
    """Clean the steel-industry energy dataset."""

    dataframe = pd.read_csv(STEEL_ENERGY_FILE)

    dataframe.columns = [
        clean_column_name(column)
        for column in dataframe.columns
    ]

    dataframe = dataframe.rename(
        columns={
            "usage_kwh": "energy_usage_kwh",
            "co2tco2": "co2_emissions_tco2",
            "weekstatus": "week_status",
            "day_of_week": "day_of_week",
            "load_type": "load_type",
        }
    )

    dataframe["date"] = pd.to_datetime(
        dataframe["date"],
        format="%d/%m/%Y %H:%M",
        errors="coerce"
    )

    numeric_columns = [
        "energy_usage_kwh",
        "lagging_current_reactive_power_kvarh",
        "leading_current_reactive_power_kvarh",
        "co2_emissions_tco2",
        "lagging_current_power_factor",
        "leading_current_power_factor",
        "nsm",
    ]

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )

    text_columns = [
        "week_status",
        "day_of_week",
        "load_type",
    ]

    for column in text_columns:
        dataframe[column] = (
            dataframe[column]
            .astype("string")
            .str.strip()
        )

    dataframe = dataframe.drop_duplicates()

    dataframe = dataframe.dropna(
        subset=[
            "date",
            "energy_usage_kwh",
            "co2_emissions_tco2",
        ]
    )

    dataframe = dataframe[
        (dataframe["energy_usage_kwh"] >= 0)
        & (dataframe["co2_emissions_tco2"] >= 0)
    ]

    dataframe["hour"] = dataframe["date"].dt.hour
    dataframe["month"] = dataframe["date"].dt.month
    dataframe["month_name"] = dataframe["date"].dt.month_name()
    dataframe["year"] = dataframe["date"].dt.year
    dataframe["is_weekend"] = (
        dataframe["week_status"]
        .str.lower()
        .eq("weekend")
    )

    dataframe["co2_intensity_tco2_per_kwh"] = (
        dataframe["co2_emissions_tco2"]
        / dataframe["energy_usage_kwh"].replace(0, pd.NA)
    )

    dataframe = dataframe.sort_values("date").reset_index(drop=True)

    return dataframe


def save_processed_data(
    smart_manufacturing: pd.DataFrame,
    steel_energy: pd.DataFrame,
) -> None:
    """Save cleaned datasets as CSV files."""

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    smart_output = (
        PROCESSED_DIR
        / "smart_manufacturing_clean.csv"
    )

    steel_output = (
        PROCESSED_DIR
        / "steel_energy_clean.csv"
    )

    smart_manufacturing.to_csv(
        smart_output,
        index=False
    )

    steel_energy.to_csv(
        steel_output,
        index=False
    )

    print("Cleaned datasets saved successfully.")
    print(f"Smart manufacturing rows: {len(smart_manufacturing):,}")
    print(f"Steel energy rows: {len(steel_energy):,}")
    print(f"Created: {smart_output.relative_to(PROJECT_ROOT)}")
    print(f"Created: {steel_output.relative_to(PROJECT_ROOT)}")


def main() -> None:
    """Run the complete cleaning process."""

    smart_manufacturing = clean_smart_manufacturing()
    steel_energy = clean_steel_energy()

    save_processed_data(
        smart_manufacturing,
        steel_energy,
    )


if __name__ == "__main__":
    main()