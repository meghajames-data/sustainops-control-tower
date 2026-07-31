from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ORDERS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "logistics_orders_clean.csv"
)


def main() -> None:
    orders = pd.read_csv(ORDERS_FILE)

    print(
        orders[
            [
                "order_id",
                "product_id",
                "unit_quantity",
                "weight",
                "total_weight",
            ]
        ]
        .head(20)
        .to_string(index=False)
    )

    print("\nWeight consistency by product")

    result = (
        orders.groupby("product_id", as_index=False)
        .agg(
            unique_weight_values=("weight", "nunique"),
            minimum_weight=("weight", "min"),
            maximum_weight=("weight", "max"),
            average_weight=("weight", "mean"),
        )
        .sort_values(
            "unique_weight_values",
            ascending=False,
        )
    )

    print(result.head(20).to_string(index=False))


if __name__ == "__main__":
    main()