from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import boto3
import json
import pickle
from datetime import datetime
from botocore.exceptions import ClientError


def load_config(config_file='config.json'):
        with open(config_file, 'r') as f:
            return json.load(f)
"""
 function to scrap the deeds for the date
    using playwright chromium
    :param date: date which we are scrapping the data
    :return: deed_info,the dictionary of scrapped deed_data
"""
def scrape_deeds_new(date):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()
        url = 'https://roddaybook.charlestoncounty.org/'
        deed_info = {}
        try:
            page.goto(url)
            page.wait_for_selector("input#rmcfrom", state="visible")
            page.fill("input#rmcfrom", date)
            page.fill("input#rmcto", date)
            with page.expect_navigation(wait_until="networkidle"):
                page.click("input#btnSearch")
                page.wait_for_selector("table#electionstable")
                while True:
                    table_data = page.query_selector_all("table#electionstable tbody tr")
                    for row in table_data:
                        cells = row.query_selector_all("td")
                        if len(cells) > 0:
                            # Extract data from each cell
                            record_date = cells[0].inner_text().strip()
                            record_time = cells[1].inner_text().strip()
                            maker_firm_name = cells[2].inner_text().strip()
                            recipient_firm_name = cells[3].inner_text().strip()
                            inst = cells[4].inner_text().strip()
                            book_page = cells[5].inner_text().strip()
                            orig_book = cells[6].inner_text().strip()
                            orig_page = cells[7].inner_text().strip()

                            # Use "Inst" as the key and other data as sub-dictionary
                            deed_info[inst] = {
                                'Record Date': record_date,
                                'Record Time': record_time,
                                'Maker Firm Name': maker_firm_name,
                                'Recipient Firm Name': recipient_firm_name,
                                'Book-Page': book_page,
                                'Orig Book': orig_book,
                                'Orig Page': orig_page
                            }
                            # Try to click the "Next" button to navigate to the next page
                    next_button = page.query_selector("li.PagedList-skipToNext a")
                    if next_button:
                        next_button.click()
                        # Wait for the table to load on the new page
                        page.wait_for_selector("table#electionstable")
                    else:
                        # No more pages to navigate
                        break

            print(len(deed_info))
        except PlaywrightTimeoutError as e:
            print(f"Timeout error: {str(e)}")
        except Exception as e:
            print(f"An error Occurred:{str(e)}")
        return deed_info
"""
    Check if an S3 bucket exists.

    :param bucket_name: Name of the bucket to check
    :return: True if bucket exists, else False
    """
def check_bucket_exsists(bucket_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return False
    except ClientError:
        return True


"""
 create a S3 Bucket using boto3

    :param bucket_name: Bucket needs to create
    :return: True if bucket was created, else False
"""
def create_bucket(bucket_name):
    try:
        s3_client = boto3.client('s3')
        location = {'LocationConstraint': 'us-east-2'}
        s3_client.create_bucket(Bucket = bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        print(f"Error creating the bucket: {e}")
        return False
    return True


"""
 Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket_name: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
"""
def upload_to_s3(file_name, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_name
    
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name,bucket_name,object_name)
        print(response)
    except Exception as e:
        print(f"Error Uploading the file:{str(e)}")
        return False
    return True    

##Passing the date as argument to the function in the main method
if __name__ == "__main__":
    config = load_config()
    date = config.get('date')
    bucket_name = config.get('bucket_name')
    try:
        deed_info = scrape_deeds_new(date)
        ##deeds = scrape_deeds(date)
        file_name = f"deed_info{date.replace('/','_')}.pkl"
        with open(file_name,'wb') as f:
            pickle.dump(deed_info,f)
        print(f"deed information saved to {file_name}")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        object_name = f"{file_name}_{timestamp}"
        print(bucket_name)
        if check_bucket_exsists:
            create_bucket(bucket_name)
        if(upload_to_s3(file_name, bucket_name, object_name)):
            print(f"File {file_name} uploaded to {bucket_name}/{object_name}")
        else:
            print("File upload failed")
    except Exception as e:
        print(f"An Unexpected error occurred: {str(e)}")