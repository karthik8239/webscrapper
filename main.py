import json
import pickle
from datetime import datetime
from scraper import scrape_deeds_new
from cloud import check_bucket_exists, create_bucket, upload_to_s3

def load_config(config_file='config.json'):
    """
    Load configuration from a JSON file.
    :param config_file: Path to the configuration file.
    :return: Configuration data as a dictionary.
    """
    with open(config_file, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    config = load_config()
    date = config.get('date')
    bucket_name = config.get('bucket_name')
    url = config.get('url')
    try:
        deed_info = scrape_deeds_new(date)
        file_name = f"deed_info_{date.replace('/', '_')}.pkl"
        with open(file_name, 'wb') as f:
            pickle.dump(deed_info, f)
        print(f"Deed information saved to {file_name}")
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        object_name = f"{timestamp}_{file_name}"
        
        if not check_bucket_exists(bucket_name):
            create_bucket(bucket_name)
        
        if upload_to_s3(file_name, bucket_name, object_name):
            print(f"File {file_name} uploaded to {bucket_name}/{object_name}")
        else:
            print("File upload failed")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
