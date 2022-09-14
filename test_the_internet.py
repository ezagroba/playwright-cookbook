import time
from playwright.sync_api import expect


def test_geolocation(page, context):
    context.grant_permissions(["geolocation"])
    page.goto("https://the-internet.herokuapp.com/geolocation")
    context.set_geolocation({"latitude": 10, "longitude": 10})
    page.click("text=Where am I?")
    time.sleep(5)

"""We weren't able to get the system-level settings to remember 
to allow Chromium to get our location. SECRETS."""

def test_dropdown(page):
    page.goto("https://the-internet.herokuapp.com/dropdown")
    page.select_option("select#dropdown", "2")
    expect(page.locator("[selected='selected']")).to_contain_text("Option 2")

def test_drag_and_drop(page):
    page.goto("https://the-internet.herokuapp.com/drag_and_drop")
    l = page.locator("#column-a")
    l2 = page.locator("#column-b")
    expect(l).to_contain_text("A")
    l.drag_to(l2)
    expect(l).to_contain_text("B")

def test_file_upload(page):
    page.goto("https://the-internet.herokuapp.com/upload")
    page.locator('input#file-upload').set_input_files('/Users/Elizabeth.Zagroba/Desktop/htsm.pdf')
    page.click("#file-submit")
    expect(page.locator("#uploaded-files")).to_have_text("htsm.pdf")

def test_exit_intent():
    """easier to test with a mouse, why would you automate?"""
    pass

def test_floating_menu(page):
    page.goto("https://the-internet.herokuapp.com/floating_menu")
    page.mouse.wheel(0, 1470000)
    page.locator("a[href='#contact']").click()
    """playwright won't let you check visibility within the viewport as opposed to the 
    whole DOM."""

def test_redirect(page, browser):
    # this is a mess! what we want to do is click the link and check that we have a 302
    context = browser.new_context(base_url="https://the-internet.herokuapp.com/redirector")
    api_request_context = context.request
    response = api_request_context.post("http://selenium.thinkcode.se/selectColor")
    assert response.status == 500
    page.locator('#redirect').click()
