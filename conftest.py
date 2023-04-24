import pytest

from playwright.sync_api import Browser, Page, BrowserContext


# TODO: figure out autouse
@pytest.fixture(scope="function")
def our_precious(page):
    page.goto("https://todomvc.com/examples/vanillajs/#/active")
    yield page

@pytest.fixture(scope="function")
def someone_elses_precious(browser):
    our_context = browser.new_context()
    our_page = our_context.new_page()
    our_page.goto("https://todomvc.com/examples/vanillajs/#/active")
    # our_page gives us a response object, page loads a different window but empty
    yield our_page, our_context

"""    
@pytest.fixture(scope="session")
def my_browser(browser) -> Page:
    c = browser.new_context()
    p = c.new_page()
    p.goto('https://todomvc.com/examples/vanillajs/')
    yield p
    c.close()
"""

@pytest.fixture(scope="session", autouse=True)
def url(pytestconfig):
    url = None
    if url is None:
        url = pytestconfig.getoption("base_url")
    yield url

@pytest.fixture(scope="session")
def br(browser: Browser, my_context_arguments, pytestconfig) -> BrowserContext:
    new_context = browser.new_context(**my_context_arguments)
    yield new_context
    new_context.close()

@pytest.fixture(scope="function")
def br_page(br) -> Page:
    new_page = br.new_page()
    new_page.goto("https://todomvc.com/examples/vanillajs/")
    yield new_page

@pytest.fixture(scope="session")
def my_context_arguments(url):
    context_args = {
        "base_url": url,
        "locale": "fi-FI",
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
        "java_script_enabled": True,
    }
    return context_args