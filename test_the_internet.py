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