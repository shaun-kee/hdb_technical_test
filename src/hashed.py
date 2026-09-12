import pandas as pd
import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TRANSFORMED_DIR = (PROJECT_ROOT / "data" / "transformed")
HASHED_DIR = (PROJECT_ROOT / "data" / "hashed")

def hashing(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def hash_processing():
    
    filepath = (TRANSFORMED_DIR / "transformed_dataset.csv")
    reader = pd.read_csv(filepath)
    

    reader["block_extract"]=reader["block"].astype(str).replace(r"\D",'',regex=True).str[:3]
    reader["block_extract"]=reader["block_extract"].str.zfill(3)

    reader["avg_price"] = reader.groupby(["month","town","flat_type"])["resale_price"].transform('mean')
    reader["resale_extract"]=reader["avg_price"].astype(str).str[:2]

    reader["month_extract"]=reader["month"].str.split('-').str[-1]
    reader["first_char_extract"]=reader["town"].str[0]

    reader["identifier"]="S"+reader["block_extract"]+reader["resale_extract"]+reader["month_extract"]+reader["first_char_extract"]

    reader["hashed_identifier"]=reader["identifier"].apply(hashing)

    dropped_col = ["block_extract","avg_price","resale_extract","month_extract","first_char_extract","identifier"]

    hashed_data = reader.drop(columns=dropped_col).copy()

    hashed_data.to_csv(HASHED_DIR / "hashed_dataset.csv", index=False)
    
    print("hashing completed")
    
if __name__ == "__main__":
    hash_processing()
