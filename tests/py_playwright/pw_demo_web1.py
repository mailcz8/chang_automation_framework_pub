from playwright.sync_api import sync_playwright
import time

def run_playwright_example():
    """
    A synchronus Playwright function to launch a browser, navigate, 
    and take a screenshot.

    Before running:
    1. Install Playwright: pip install playwright
    2. Install browser binaries: playwright install
    """
    # Use sync_playwright() context manager to ensure proper cleanup
    with sync_playwright() as p:
        # 1. Launch a Chromium browser instance
        print("Launching Chromium browser...")
        browser = p.chromium.launch(headless=False) # Set headless=False to see the GUI
        
        # 2. Create a new context and page
        page = browser.new_page()

        # 3. Navigate to a URL
        target_url = "https://www.google.com"
        print(f"Navigating to {target_url}...")
        page.goto(target_url)

        # 4. Wait for the page to load completely (optional, but good practice)
        # We wait for the network to be mostly idle.
        page.wait_for_load_state("networkidle")
        
        # 5. Perform an action: Take a screenshot
        screenshot_path = "google_homepage_screenshot.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved successfully to {screenshot_path}")

        # 6. Perform another action: Fill a search box and click the button
        print("Searching for 'Gemini AI'...")
        # Get the search input field by its name attribute
        search_input = page.get_by_title("Search")
        search_input.fill("Gemini AI")
        time.sleep(5)

        # Click the Google Search button (often tricky, using the text locator for robustness)
        page.get_by_role("button", name="Google Search").click()
        
        # 7. Wait for navigation after the search
        page.wait_for_url("**/search?**")
        print("Successfully navigated to search results page.")
        
        # 8. Close the browser
        browser.close()
        print("Browser closed. Automation finished.")


if __name__ == "__main__":
    try:
        run_playwright_example()
    except Exception as e:
        print(f"An error occurred during Playwright execution: {e}")
        print("Ensure you have run 'pip install playwright' and 'playwright install'")