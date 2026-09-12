from extract import extract_processing
from profile import profile_processing
from transform import transform_processing
from hashed import hash_processing


def main():
    print("data pipeline extraction start")
    
    extract_processing()
    profile_processing()
    transform_processing()
    hash_processing()
    
    print("data pipeline extraction completed")
    
    
if __name__ == "__main__":
    main()
