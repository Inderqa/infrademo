import time

from playwright.sync_api import Page, expect
from pytest_playwright.pytest_playwright import context


def test_basic_launch(playwright):
    browser = playwright.chromium.launch(headless=False,slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/loginpagePractise")
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.get_by_label("Password:").fill("learning")
    page.get_by_role("combobox").select_option("teach")
    page.get_by_role("checkbox",name="terms").click()
    page.get_by_role("button",name="Sign In").click()
    time.sleep(5)


def test_invalid_login_validate_error_message(page:Page):
    page.goto("https://rahulshettyacademy.com/loginpagePractise")
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.get_by_label("Password:").fill("learning2")
    page.get_by_role("combobox").select_option("teach")
    page.get_by_role("checkbox",name="terms").click()
    page.get_by_role("button",name="Sign In").click()
    expect(page.get_by_text("Incorrect username/password.")).to_be_visible()

def test_handle_child_window(playwright):
    browser = playwright.chromium.launch(headless=False,slow_mo=2000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/loginpagePractise")
    with context.expect_page() as new_page_info:
        page.locator("//a[@class='blinkingText']").click()
    child_page = new_page_info.value
    child_page.wait_for_load_state()
    print("Child Window Title:", child_page.title())
    page.bring_to_front()
    print("Parent Window Title:", page.title())
    browser.close()

def test_handle_dropdown(page:Page):
    page.goto("https://rahulshettyacademy.com/angularpractice/shop")
    phoneProduct = page.locator("app-card").filter(has_text='Nokia Edge')
    phoneProduct.get_by_role('button').click()
    expect(page.locator("//a[contains(normalize-space(text()), 'Checkout')]")).to_be_visible()
    page.locator("//a[contains(normalize-space(text()), 'Checkout')]").click()
    expect(page.locator("//a[contains(text(),'Nokia Edge')]")).to_be_visible()
    expect(page.locator("//td[contains(normalize-space(@class),'col-sm-8')]")).to_have_count(1)


# In following test have window is maximized,scroll into view until locator is visible is used
def test_UIChecks(playwright):
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/AutomationPractice")
    expect(page.locator("//input[@value='Hide']")).to_be_visible()
    page.locator("//input[@value='Show']").click()
    page.locator("//input[@placeholder='Hide/Show Example']").scroll_into_view_if_needed()
    expect(page.locator("//input[@placeholder='Hide/Show Example']")).to_be_visible()
    page.locator("//input[@value='Hide']").click()
    expect(page.locator("//input[@placeholder='Hide/Show Example']")).to_be_hidden()

def test_handle_alert(playwright):
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"],slow_mo=2000)
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/AutomationPractice")
    page.on("dialog",lambda dialog:dialog.accept()) ## Accept the dialog or click okay on alert
    page.get_by_role("button",name="Confirm").click()
    page.on("dialog", lambda dialog: dialog.dismiss()) ##Click cancel on alert
    page.get_by_role("button", name="Confirm").click()


def test_frames(playwright):
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"],slow_mo=2000)
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/AutomationPractice")
    page.locator("#courses-iframe").scroll_into_view_if_needed()
    pageFrame = page.frame_locator("#courses-iframe")
    pageFrame.get_by_role("link",name="All Access plan")
    expect(pageFrame.locator("body")).to_contain_text(" Learn Earn & Shine")
    page.locator("#mousehover").hover()

def test_frames(playwright):
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.goto("https://rahulshettyacademy.com/seleniumPractise/#/offers")
    columns =  page.locator("//th[@role='columnheader']").all()
    for index, column in enumerate(columns):
        if column.inner_text() == "Price":
           Pricecol = index
    rice_row = page.locator("//tbody//tr").filter(has_text="Rice")
    expect(rice_row.locator("td").nth(Pricecol)).to_contain_text("37")


