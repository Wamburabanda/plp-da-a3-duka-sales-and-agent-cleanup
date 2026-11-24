
import pandas as pd

def clean_agent_data(txns, agents):
    """
    Clean transaction and agent datasets.

    Returns:
        clean_df, log
    """

    log = []

    clean = txns.drop_duplicates().copy()

    duplicates_removed = len(txns) - len(clean)

    log.append(
        f"Removed {duplicates_removed} duplicate transactions"
    )

    clean["txn_type"] = (
        clean["txn_type"]
        .str.strip()
        .str.title()
    )

    log.append(
        "Standardized transaction types"
    )

    return clean, log
