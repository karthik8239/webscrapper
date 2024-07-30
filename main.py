import json
import pickle
import logging
from datetime import datetime
from scraper import scrape_deeds_new
from cloud import check_bucket_exists, create_bucket, upload_to_s3

logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers= [
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def load_config(config_file='config.json'):
    """
    Load configuration from a JSON file.
    :param config_file: Path to the configuration file.
    :return: Configuration data as a dictionary.
    """
    logging.info(f"Loading configuration from {config_file}")
    with open(config_file, 'r') as f:
        return json.load(f)
    
def save_deed_info(date, url):
    """
    Scrape deed information and save it to a pickle file.
    :param date: Date for the deed information.
    :param url: URL to scrape the deed information from.
    :return: Name of the pickle file.
    """
    logging.info(f"Scraping the deed information for date:{date} from URL: {url}")
    deed_info = scrape_deeds_new(date, url)
    file_name = f"deed_info_{date.replace('/', '_')}.pkl"
    with open(file_name, 'wb') as f:
        pickle.dump(deed_info, f)
    print(f"Deed information saved to {file_name}")
    return file_name

def upload_file_to_s3(file_name, bucket_name):
    """
Scrape deed information and save it to a pickle file.
:param date: Date for the deed information.
:param url: URL to scrape the deed information from.
:return: Name of the pickle file.
"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    object_name = f"{timestamp}_{file_name}"
    if not check_bucket_exists(bucket_name):
        create_bucket(bucket_name)
    if upload_to_s3(file_name, bucket_name, object_name):
        print(f"File {file_name} uploaded to {bucket_name}/{object_name}")
        return True
    else:
        print("File upload failed")
        return False

if __name__ == "__main__":
    try:
        config = load_config()
        date = config.get('date')
        bucket_name = config.get('bucket_name')
        url = config.get('url')
        file_name = save_deed_info(date,url)
        upload_file_to_s3(file_name, bucket_name)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
