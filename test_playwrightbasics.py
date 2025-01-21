import time

from playwright.sync_api import Page

# def test_basic_launch(playwright):
#     browser = playwright.chromium.launch(headless=False,slow_mo=5000)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://rahulshettyacademy.com/loginpagePractise")

def test_corelocator(page:Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise")
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.get_by_label("Password:").fill("learning")
    page.get_by_role("combobox").select_option("teach")
    page.get_by_role("checkbox",name="terms").click()
    page.get_by_role("button",name="Sign In").click()
    time.sleep(5)