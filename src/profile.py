import pandas as pd
from data_profiling import ProfileReport
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"
EDITED_DIR = PROJECT_ROOT / "data" / "edited"
CLEANED_DIR = PROJECT_ROOT / "data" / "cleaned"
PROFILING_DIR = PROJECT_ROOT / "profiling"


def profile_processing():
    datasets = []
    for num in range(1,6):
        filepath = RAW_DIR / f"dataset_{num}.csv"
        reader = pd.read_csv(filepath)
        
        title = f"data_profiling_report_{num}"
        report_name=PROFILING_DIR / f"report_{num}.html"
        profile = ProfileReport(reader, title=title)
        profile.to_file(report_name)
        

    # based on profiling, dataset 1 and 5 have extra columns
    numbers = [1,5]

    for num in numbers:
        filepath = RAW_DIR / f"dataset_{num}.csv"
        df=pd.read_csv(filepath)
        df=df.drop(columns="remaining_lease")
        excel_name = EDITED_DIR / f"dataset_edited_{num}.csv"
        df.to_csv(excel_name, index=False)


    files = [
        EDITED_DIR / "dataset_edited_1.csv",
        RAW_DIR / "dataset_2.csv",
        RAW_DIR / "dataset_3.csv",
        RAW_DIR / "dataset_4.csv",
        EDITED_DIR / "dataset_edited_5.csv"
    ]

    datasets = []

    for file in files:
        df = pd.read_csv(file)
        datasets.append(df)

    master_df = pd.concat(
        datasets,
        ignore_index=True,
        sort=False
    )

    master_df.to_csv(
        CLEANED_DIR / "master_dataset.csv",
        index=False
    )

    title = f"data_profiling_report_master"
    report_name=PROFILING_DIR / "report_master.html"
    profile = ProfileReport(master_df, title=title)
    profile.to_file(report_name)
    
    print("profiling completed")

if __name__ == "__main__":
    profile_processing()