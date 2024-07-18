from playwright.sync_api import sync_playwright
import pandas as pd
import boto3
import pickle
from datetime import datetime

def scrape_deeds(date):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        url = 'https://rod.beaufortcountysc.gov/BrowserViewDMP/'
        page.goto(url)
        page.click('a:has-text("Document Type")')
        page.screenshot(path='test_screenshot.png')
        ##page.wait_for_selector('input[name="fromdate"]')
        from_date_input = 'input[name="fromdate"][placeholder="MM/DD/YYYY"]'
        page.locator(from_date_input).scroll_into_view_if_needed()
        page.fill(from_date_input, date)
        page.screenshot(path='after_from_date_screenshot.png')
        browser.close()
    return 0

if __name__ == "__main__":
    test_date ='07/01/2024'
    scrape_deeds(test_date)
