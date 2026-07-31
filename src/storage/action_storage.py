from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ACTION_FILE = PROJECT_ROOT / "database" / "actions.csv"

ACTION_COLUMNS = [
    "action_title",
    "owner",
    "priority",
    "status",
    "deadline",
    "expected_co2_reduction_tco2",
    "expected_annual_cost_saving_usd",
    "notes",
]


def load_actions() -> list[dict]:
    """Load saved actions from the CSV file."""

    if not ACTION_FILE.exists():
        return []

    actions = pd.read_csv(ACTION_FILE)

    if actions.empty:
        return []

    actions = actions.reindex(columns=ACTION_COLUMNS)

    actions["deadline"] = pd.to_datetime(
        actions["deadline"],
        errors="coerce",
    ).dt.date

    return actions.to_dict(orient="records")


def save_actions(actions: list[dict]) -> None:
    """Save all actions permanently to the CSV file."""

    ACTION_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    actions_dataframe = pd.DataFrame(
        actions,
        columns=ACTION_COLUMNS,
    )

    actions_dataframe.to_csv(
        ACTION_FILE,
        index=False,
    )