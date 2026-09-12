import pandas as pd
import datetime as dt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned"
QUARANTINED_DIR = PROJECT_ROOT / "data" / "quarantined"
TRANSFORMED_DIR = PROJECT_ROOT / "data" / "transformed"

def transform_processing():
    # compute remaining lease
    data = pd.read_csv(CLEANED_DIR / "master_dataset.csv")
    data["transact_date"] = pd.to_datetime(data['month'],format='%Y-%m')
    data["used_month"] = (data["transact_date"].dt.year-data["lease_commence_date"])*12 + data["transact_date"].dt.month -1
    data["remaining_month"] = (99*12) - data["used_month"]

    data["lease_year_left"] = data["remaining_month"] // 12
    data["lease_month_left"] = data["remaining_month"] % 12


    data["remaining_lease"] = (
        data["lease_year_left"].astype(str)
        + " years "
        + data["lease_month_left"]
            .astype(str)
            .str.zfill(2)
        + " months")

    # remove working columns
    data.drop(columns=["transact_date","used_month","remaining_month","lease_year_left","lease_month_left"],inplace=True)

    # remove duplicates 
    data = data.sort_values(by="resale_price",ascending=False)

    column_lst = list(data.columns.values)
    column_lst.remove('resale_price')

    # segregating cleansed and duplicate data
    quarantined_data = data[data.duplicated(subset=column_lst,keep="first")].copy()
    quarantined_data.to_csv(QUARANTINED_DIR / "quarantined_dataset.csv",index=False)

    transformed_data = data.drop_duplicates(subset=column_lst,keep="first").reset_index(drop=True).copy()
    transformed_data.to_csv(TRANSFORMED_DIR / "transformed_dataset.csv", index=False)

if __name__ == "__main__":
    transform_processing()