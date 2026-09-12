import requests
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

def get_url(url):    
    response = requests.get(url)
    
    response.raise_for_status()
    
    return response.json()

def get_download_link(collection_id=189):
    
    metadata_url = f"https://api-production.data.gov.sg/v2/public/api/collections/{collection_id}/metadata"

    result = get_url(metadata_url)

    dataset_id = result["data"]["collectionMetadata"]["childDatasets"]

    download =[]

    for datasetId in dataset_id:
        print("extracting...")
        download_link =f"https://api-open.data.gov.sg/v1/public/api/datasets/{datasetId}/poll-download"
        result = get_url(download_link)
        
        download.append(result["data"]["url"])
        
        time.sleep(10)
    
    print(f"link download completed")
    
    return download

def extraction(links,output_path):
    response = requests.get(
        links,
        stream=True
    )

    response.raise_for_status()

    with open(output_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                file.write(chunk)

def extract_processing():
    collection_id = 189
    
    RAW_DIR.mkdir(parents=True,exist_ok=True)
    
    download = get_download_link(collection_id)
    
    for index, link in enumerate(download, start=1):
        output_path = RAW_DIR / f"dataset_{index}.csv"
        extraction(link, output_path)    
        
    print(f"extraction completed")

if __name__ == "__main__":
    extract_processing()




