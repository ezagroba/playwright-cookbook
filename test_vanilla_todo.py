from playwright.sync_api import expect, Browser, BrowserContext
from time import sleep
import pytest


# TODO: move function into page object
def add_a_todo(our_precious, text):
    our_precious.locator(".new-todo").fill(text)
    our_precious.locator(".info").click()


def test_add_to_do(our_precious):
    ''' numbers 2 and 3 '''
    add_a_todo(our_precious, "decent test data")
    expect(our_precious.locator(".todo-list li label")).to_contain_text("decent test data")
    expect(our_precious.locator(".new-todo")).to_be_empty()


def test_no_main_or_footer_with_no_todos(our_precious):
    '''that guy had this test first (very professional)'''
    expect(our_precious.locator(".main")).not_to_be_visible()
    expect(our_precious.locator(".footer")).not_to_be_visible()


def test_no_main_or_feet_when_all_todos_deleted(our_precious):
    add_a_todo(our_precious, "Valentine's Day <3")
    our_precious.locator(".todo-list").hover()
    our_precious.locator(".destroy").click()
    expect(our_precious.locator(".main")).not_to_be_visible()
    expect(our_precious.locator(".footer")).not_to_be_visible()


def test_toggle_arrow_at_the_top(our_precious):
    add_a_todo(our_precious, "Valentine's Day <3")
    our_precious.locator("#toggle-all").click()
    expect(our_precious.locator(".clear-completed")).to_be_visible()

def test_clear_local_storage_to_dos_are_empty(browser: Browser, context: BrowserContext):
    our_context = browser.new_context(storage_state="empty_local_storage.json")
    our_page = our_context.new_page()
    our_page.goto("https://todomvc.com/examples/vanillajs/#/active")
    how_many_contexts = browser.contexts.count(our_context)
    our_page.locator(".new-todo").fill("Valentine's Day <3")
    #our_page.locator(".info").click()
    our_context(storage_state="no_todos.json")
    our_context.storage_state(path="empty_local_storage.json")
    sleep(2)
    expect(our_page.locator(".todo-list li label")).not_to_contain_text("Valentine's Day <3")


def test_set_storage_and_check_that_its_there(br_page):
    br_page.evaluate("localStorage.setItem('todos-vanillajs', '[{\"title\":\"hello\",\"completed\":false,\"id\":1}]')")
    br_page.goto("https://todomvc.com/examples/vanillajs/")
    expect(br_page.locator(".todo-list li label")).to_contain_text("hello")

def test_set_a_whole_bunch_of_storage_and_check_that_one_exists():
    pass

def get_local_storage_value(context: BrowserContext) -> list:
    #TODO: get rid of ghost tab
    for k, v in context.request.storage_state().items():
        if k == "origins":
            origins = v
            for i in origins:
                local_s = i.get("localStorage")
                if local_s:
                    for y in local_s:
                        ls_content = y.get("value")
                        return ls_content
    raise ValueError("No expected content in browser context")


def test_add_a_todo_on_the_page_and_check_that_its_in_storage(br_page, br):
    br_page.goto("https://todomvc.com/examples/vanillajs/")
    br_page.locator(".new-todo").fill("Valentine's Day <3")
    br_page.locator(".info").click()
    assert "Valentine's Day <3" in get_local_storage_value(br)

@pytest.mark.parametrize("whitespace_item", ["  leading whitespace", "trailing whitespace   ", "middling      whitespace"])
def test_trimming_whitespace_of_all_shapes_and_positions(whitespace_item, br_page):
    br_page.goto("https://todomvc.com/examples/vanillajs/")
    br_page.locator(".new-todo").fill(whitespace_item)
    br_page.locator(".info").click()
    assert #TODO make a list of items to compare to, or trim the whitespace item with Python and then compare