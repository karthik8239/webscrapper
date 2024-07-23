from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def scrape_deeds_new(date,url):
    """
    Function to scrape the deeds for the date using Playwright Chromium.
    :param date: Date for which the data is being scraped.
    :return: A dictionary containing the scraped deed data.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
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
            print(f"An error occurred: {str(e)}")
        return deed_info
