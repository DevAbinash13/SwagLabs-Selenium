import pytest
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture(scope="class")
def test_setup(request):
    driver = webdriver.Edge()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    request.cls.driver = driver
    request.cls.wait = wait
    return driver