
import pandas as pd

def clean_agent_data(txns, agents):

    log = []

    clean = txns.drop_duplicates().copy()

    duplicates_removed = (
        len(txns)
        - len(clean)
    )

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

    clean["amount"] = pd.to_numeric(
        clean["amount"],
        errors="coerce"
    )

    clean["amount_imputed"] = (
        clean["amount"].isna()
    )

    n_missing = clean[
        "amount_imputed"
    ].sum()

    log.append(
        f"Flagged {n_missing} missing amounts"
    )

    clean["amount"] = clean[
        "amount"
    ].fillna(
        clean["amount"].median()
    )

    log.append(
        "Imputed missing amounts using median"
    )

    clean["txn_date"] = pd.to_datetime(
        clean["txn_date"]
        .str.replace("/", "-"),
        errors="coerce"
    )

    log.append(
        "Standardized date formats"
    )

    q1 = clean["amount"].quantile(0.25)

    q3 = clean["amount"].quantile(0.75)

    iqr = q3 - q1

    upper = q3 + 1.5 * iqr

    clean["is_outlier"] = (
        clean["amount"] > upper
    )

    log.append(
        f"Flagged {clean['is_outlier'].sum()} outliers"
    )

    merged = clean.merge(
        agents,
        on="agent_id",
        how="left"
    )

    unknown_agents = merged[
        "county"
    ].isna().sum()

    log.append(
        f"{unknown_agents} transactions reference unknown agents"
    )

    return merged, log
