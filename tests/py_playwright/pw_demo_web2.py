from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  #Set healess=True if you don't want to too browser open
        page = browser.new_page()
        for i in ("https://www.google.com", "https://www.temu.com/"):
            print("Open URL: ", i)
            page.goto(i)
            print("Page title:", page.title())
            time.sleep(3)
        browser.close()

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"An error occurred during Playwright execution: {e}")
        print("Ensure you have run 'pip install playwright' and 'playwright install'")