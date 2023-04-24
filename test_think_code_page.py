import time


def test_homepage_loads(page):
    page.goto("http://selenium.thinkcode.se/")
    assert page.inner_text('#helloWorld') == 'Find an element - hello world'

def test_find_an_element(page):
    page.goto("http://selenium.thinkcode.se/helloWorld")
    assert page.inner_text('h1') == 'Hello, world!'

def test_request_password(page):
    page.goto("http://selenium.thinkcode.se/requestPassword")
    page.fill("#account", "horse")
    page.click("name='submit'")
    assert page.inner_text('#confirmation') == "A new password has been sent to horse"
    assert page.inner_text("text=horse")

def test_select_single_checkbox(page):
    page.goto("http://selenium.thinkcode.se/selectColor")
    page.check("[value='blue']")
    assert page.is_checked("[value='blue']")
    assert page.is_checked("[value='red']") == False
    page.click('text=submit')
    assert page.inner_text("[name='color']") == "blue"

def test_select_two_checkboxes(page):
    page.goto("http://selenium.thinkcode.se/selectColor")
    page.check("[value='blue']")
    page.check("[value='red']")
    assert page.is_checked("[value='blue']")
    assert page.is_checked("[value='red']")
    page.click('text=submit')
    assert page.inner_text('ul') == 'red\nblue'
    assert page.locator("li").all_inner_texts() == ['red', 'blue']

def test_500(browser):
    context = browser.new_context(base_url="http://selenium.thinkcode.se/selectColor")
    api_request_context = context.request
    response = api_request_context.post("http://selenium.thinkcode.se/selectColor")
    assert response.status == 500

def test_no_checkboxes(page, browser):
    page.goto("http://selenium.thinkcode.se/selectColor")
    with page.expect_response("http://selenium.thinkcode.se/selectColor") as response_info:
        page.click('text=submit')
        assert response_info.value.status == 500
def test_select_tea(page):
    page.goto("http://selenium.thinkcode.se/selectBeverage")
    assert page.is_checked("[value='tea']") == False
    page.click("[value='tea']")
    assert page.is_checked("[value='tea']")

def test_select_condiment_milksugar(page):
    page.goto("http://selenium.thinkcode.se/selectCondiment")
    page.select_option("select#condiments", "milk")
    # what we had assert(page.locator('#condiments').get_attribute("value") == "Definitely not milk")
    should_be_milk_now = page.locator('select#condiments').input_value()
    assert should_be_milk_now == "milk"
# we want to check that the word "Milk" is visible
# Playwright Slack help https://playwright.dev/python/docs/api/class-elementhandle#element-handle-input-value

def test_exchange_rate_with_wait(page):
    page.goto("http://selenium.thinkcode.se/exchangeRate")
    page.fill("#from", "a")
    page.fill("#to", "b")
    page.click("[type='submit']")
    assert "slow" in page.inner_text("#waitingMessage")
    assert "2.07" in page.inner_text("#exchangeRate")

def test_alert(page):
    page.goto("http://selenium.thinkcode.se/alert")
    page.click("text='Click for an alert'")
    page.on("dialog", lambda dialog: dialog.accept())
    assert page.inner_text('#result') == 'You clicked an alert'

def test_confirmation_ok(page):
    page.goto("http://selenium.thinkcode.se/alert")
    page.on("dialog", lambda dialog: dialog.accept())
    page.click("text='Click for a confirmation'")
    assert page.inner_text('#result') == 'You clicked: Ok'

def test_confirmation_cancel(page):
    page.goto("http://selenium.thinkcode.se/alert")
    page.on("dialog", lambda dialog: dialog.dismiss())
    page.click("text='Click for a confirmation'")
    assert page.inner_text('#result') == 'You clicked: Cancel'

def test_prompt_accept(page):
    page.goto("http://selenium.thinkcode.se/alert")
    page.on("dialog", lambda dialog: dialog.accept('Hello'))
    page.click("text='Click for a prompt'")
    assert page.inner_text('#result') == 'You entered: Hello'


def test_prompt_cancel(page):
    page.goto("http://selenium.thinkcode.se/alert")
    page.on("dialog", lambda dialog: dialog.dismiss())
    page.click("text='Click for a prompt'")
    assert page.inner_text('#result') == 'You entered: null'

def test_new_tab(page):
    page.goto("http://selenium.thinkcode.se/")
    with page.context.expect_page() as tab:
        page.click("text='Pop up - New page or tab'")
        new_tab = tab.value
    assert new_tab.inner_text('#headline') == 'Greetings from pop-up!'
    new_tab.close()
    time.sleep(3)
    page.click("text='Select beverage - radio buttons'")

def test_a_bit_of_everything(page):
    page.goto("http://selenium.thinkcode.se/")
    page.click("text='Buy currency - a little bit of everything'")
    assert page.title() == 'Buy currency'
    page.check("[id='sell']")
    page.select_option("select#toCurrency", "EUR")
    page.fill('#amount', '100')
    page.click("text='Submit'")
    assert page.inner_text('#result') == 'Buying 100 EUR will cost you 0 USD.'



""" TODO:
- screenshot when running the test
"""
