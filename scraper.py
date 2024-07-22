from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
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
        ##url = 'https://roddaybook.charlestoncounty.org/'
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
            deeds_info = {}
            for row in rows:
                cells = row.query_selector_all('.ag-cell')
                if len(cells) >= 10:  # Ensure we have all expected cells
                    instr_num = cells[5].inner_text().strip()  #  Instr# is in the 6th column (index 5)
                    deeds_info[instr_num] = {
                        'Name': cells[1].inner_text().strip(),
                        'Cross_Party': cells[2].inner_text().strip(),
                        'Date': cells[3].inner_text().strip(),
                        'Type': cells[4].inner_text().strip(),
                        'Book': cells[6].inner_text().strip(),
                        'Page': cells[7].inner_text().strip(),
                        'Legal': cells[8].inner_text().strip(),
                        'Consideration': cells[9].inner_text().strip()
                    }
            print(f"Extracted information for {len(deeds_info)} deeds")
        except PlaywrightTimeoutError as e:
            print(f"Timeout error: {str(e)}")
        except Exception as e:
            print(f"An error Occurred: {str(e)}")

        # Wait for the table to be visible
        page.screenshot(path='after_deeds_screenshot.png')
        browser.close()
    return deeds_info


def scrape_deeds_new(date):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False)
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


##Passing the date as argument in the main method
if __name__ == "__main__":
    date = '2024-07-01'
    try:
        deed_info = scrape_deeds_new(date)
        ##deeds = scrape_deeds(date)
        file_name = f"deed_info{date.replace('/','_')}.pkl"
        with open(file_name,'wb') as f:
            pickle.dump(deed_info,f)
        print(f"deed information saved to {file_name}")
    except Exception as e:
        print(f"An Unexpected error occurred: {str(e)}")