from playwright.sync_api import sync_playwright
import pandas as pd
import boto3
import pickle
from datetime import datetime

def scrape_deeds(date):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False)
        page = browser.new_page()
        url = 'https://rod.beaufortcountysc.gov/BrowserViewDMP/'
        page.goto(url)
        page.click('a:has-text("Document Type")')
        page.wait_for_selector('form[name="docSearchForm"]', state='visible')
        from_date_input = 'form[name="docSearchForm"] input[name="fromdate"]'
        page.wait_for_selector(from_date_input, state='visible')
        page.wait_for_selector(to_date_input, state='visible')
        # Clear the input field before filling
        #         # Fill the "From" date input
        page.fill(from_date_input, date)
        to_date_input = 'form[name="docSearchForm"] input[name="todate"]'
        page.fill(to_date_input, date)
        page.wait_for_timeout(1000)
        page.screenshot(path='after_from_date_screenshot.png')
        browser.close()
    return 0

if __name__ == "__main__":
    test_date ='07/01/2024'
    scrape_deeds(test_date)
