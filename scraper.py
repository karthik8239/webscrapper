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
        from_date_button = 'button:has-text("Close")'
        to_date_button = 'button:has-text("Close")'
        # Click the button to open the date picker for the "From" date
        page.click(from_date_button)
        page.fill('input[name="fromdate"]', date)
        page.screenshot(path='after_from_date_screenshot.png')
        # page.click(to_date_selector)
        # page.fill(to_date_selector, date)
        # page.screenshot(path='after_date_screenshot.png')
        browser.close()
    return 0

if __name__ == "__main__":
    test_date ='07/01/2024'
    scrape_deeds(test_date)
