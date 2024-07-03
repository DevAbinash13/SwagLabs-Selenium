from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import test_setup

class BasePage:
    def __init__(self, driver,wait):
        self.driver = driver
        self.wait = wait

    def presence_of_elem(self,locator):
        elem = self.wait.until(EC.presence_of_element_located(locator))
        return elem

    def elem_clickable(self,locator):
        elem = self.wait.until(EC.element_to_be_clickable(locator))
        return elem

    def elem_invisible(self,locator):
        elem = self.wait.until(EC.invisibility_of_element(locator))
        return elem