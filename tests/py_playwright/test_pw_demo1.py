from playwright.sync_api import sync_playwright
import pytest

def test_example1():
    assert 1 + 1 == 2

def test_google_title():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to Google
        page.goto("https://www.google.com")

        # Assert the title
        title = page.title()
        assert "Google" in title

        browser.close()

def test_google_title():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to Google
        page.goto("https://www.google.com")

        # Assert the title
        title = page.title()
        assert "Facebook" in title

        browser.close()