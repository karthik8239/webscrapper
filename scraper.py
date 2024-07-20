from playwright.sync_api import sync_playwright
import pandas as pd
import boto3
import pickle
from datetime import datetime

##method to scrap_the_deeds
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
        page.fill(from_date_input, date)
        to_date_input = 'form[name="docSearchForm"] input[name="todate"]'
        page.wait_for_selector(to_date_input, state='visible')
        page.fill(to_date_input, date)
        input_selector = 'form[name="docSearchForm"] .tree-view-wrapper .tree-checkbox'
        page.click(input_selector)
        search_selector = 'form[name="docSearchForm"] button.btn-xs.btn-primary'
        page.wait_for_selector(search_selector, state='visible')
        page.screenshot(path='after_documents_tab_fill.png')
        with browser.contexts()[0].expect_page() as new_page_info:
            page.click(search_selector)
        
        new_page = new_page_info.value
        new_page.wait_for_load_state('networkidle')
        
        # Wait for the table to be visible
        table_selector = 'table.results-table'  # Update this selector based on the actual table selector
        new_page.wait_for_selector(table_selector, state='visible')
        ##page.click(search_selector)
        ##page.wait_for_load_state('networkidle', timeout=60000)
        ##select all deeds
        page.screenshot(path='after_navigate_to_results_screenshot.png')
        browser.close()
    return 0

##Passing the date as argument in the main method
if __name__ == "__main__":
    test_date ='07/01/2024'
    scrape_deeds(test_date)
