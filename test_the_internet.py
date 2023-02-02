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

def test_redirect(page):
    page.goto("https://the-internet.herokuapp.com/redirector")
    with page.expect_navigation():
        page.click("#redirect")
    expect(page).to_have_url("https://the-internet.herokuapp.com/status_codes")
    what_our_page_ended = page.goto("https://the-internet.herokuapp.com/redirect")
    assert what_our_page_ended.request.redirected_from.response().status == 302

def test_404(page):
    page.goto("https://the-internet.herokuapp.com/status_codes")
    with page.expect_navigation():
        page.click("a[href='status_codes/404']")
    where_our_page_ended = page.goto("https://the-internet.herokuapp.com/status_codes/404")
    assert where_our_page_ended.status == 404

def test_typos():
    """don't test typos, fix them."""
    pass

def test_iframe(page):
    page.goto("https://the-internet.herokuapp.com/iframe")
    my_text_input = page.frame_locator("#mce_0_ifr").locator("#tinymce")
    my_text_input.fill("Let's just write something inside.")
    my_text_input.select_text()
    page.locator("[aria-label='Bold']").click()
    page.locator("[title='styles']").click()
    page.locator("[title='Inline']").hover()
    page.locator("[title='Code']").click()

def test_nested_frames():
    """this is browser functionality, why would we automate or even test this?"""
    pass

def test_login_page(page):
    page.goto("https://the-internet.herokuapp.com/login")
    page.locator("#username").fill("tomsmith")
    page.locator("#password").fill("SuperSecretPassword!")
    with page.expect_navigation():
        page.click("button[type='Submit']")
    assert "You logged into a secure area!" in page.locator("#flash-messages").inner_text()

def test_table_easy_mode_last_name_sorting(page):
    page.goto("https://the-internet.herokuapp.com/tables")
    page.locator("//span[contains(@class, 'last-name')]").click()
    assert page.locator('#table2 > tbody td.last-name').nth(0).inner_text() == 'Bach'

def test_table_easy_mode_try_to_delete_bach_and_just_give_up(page, browser):
    page.goto("https://the-internet.herokuapp.com/tables")
    lines = page.locator('#table2 > tbody td.last-name').all_inner_texts()
    position = 0
    for line in lines:
        if line == "Bach":
            break
        position+=1
    page.locator("#table2 > tbody td [href='#delete']").nth(position).click()
    expect(page).to_have_url("https://the-internet.herokuapp.com/tables#delete")

def test_table_hard_mode_last_name_sorting(page):
    page.goto("https://the-internet.herokuapp.com/tables")
    page.locator("#table1 > thead > tr span").nth(0).click()
    assert page.locator('#table1 > tbody > tr td').nth(0).inner_text() == 'Bach'

## next time - choose a new page