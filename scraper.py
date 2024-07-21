from playwright.sync_api import sync_playwright
import pandas as pd
import boto3
import pickle
from datetime import datetime
from bs4 import BeautifulSoup


##method to scrap_the_deeds
def scrape_deeds(date):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False)
        page = browser.new_page()
        url = 'https://rod.beaufortcountysc.gov/BrowserViewDMP/'
        try:
            page.goto(url)
            page.click('a:has-text("Document Type")')
            page.wait_for_selector('form[name="docSearchForm"]', state='visible')
            from_date_input = 'form[name="docSearchForm"] input[name="fromdate"]'
            page.fill(from_date_input, date)
            to_date_input = 'form[name="docSearchForm"] input[name="todate"]'
            page.fill(to_date_input, date)
            input_selector = 'form[name="docSearchForm"] .tree-view-wrapper .tree-checkbox'
            page.click(input_selector)
            search_selector = 'form[name="docSearchForm"] .col-sm-2 button.btn-xs.btn-primary'
            page.click(search_selector)
            with page.expect_navigation(wait_until="networkidle"):
                page.click(search_selector)
            # Wait for the loading indicator to disappear
            loading_indicator_selector = 'h3:has-text("Please Wait...")'
            page.wait_for_selector(loading_indicator_selector, state='hidden')
            # Wait for the table to be visible
            table_selector = 'form[name="docSearchForm"] .ag-header-container'
            #table_selector = 'form[name="docSearchForm"] .ag-header-container'
            page.wait_for_selector(table_selector, state = 'visible')
            rows = page.query_selector_all('.ag-row')
            deed_info = {}
            for row in rows:
                cells = row.query_selector_all('.ag-cell')
                if len(cells) >= 10:  # Ensure we have all expected cells
                    instr_num = cells[6].inner_text().strip()  # Assuming Instr# is in the 7th column (index 6)
                    deed_info[instr_num] = {
                        'Name': cells[2].inner_text().strip(),
                        'Cross_Party': cells[3].inner_text().strip(),
                        'Date': cells[4].inner_text().strip(),
                        'Type': cells[5].inner_text().strip(),
                        'Book': cells[7].inner_text().strip(),
                        'Page': cells[8].inner_text().strip(),
                        'Legal': cells[9].inner_text().strip(),
                        'Consideration': cells[10].inner_text().strip()
                    }
            print(f"Extracted information for {len(deed_info)} deeds")
        # Wait for the table to be visible
        page.screenshot(path='after_navigate_to_results_screenshot.png')
        browser.close()
    return 0

##Passing the date as argument in the main method
if __name__ == "__main__":
    test_date ='07/01/2024'
    deeds = scrape_deeds(test_date)
