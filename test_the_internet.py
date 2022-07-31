import time


def test_geolocation(page, context):
    context.grant_permissions(["geolocation"])
    #context.set_geolocation({"latitude": 10, "longitude": 10})
    page.goto("https://the-internet.herokuapp.com/geolocation")
    page.click("text=Where am I?")
    time.sleep(5)