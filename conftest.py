import pytest
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture(scope="class")
def test_setup(request):
    options = webdriver.EdgeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Edge(options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    request.cls.driver = driver
    request.cls.wait = wait
    return driver