from conftest import test_setup
import pytest
import constants
import time
import os
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import actions
from selenium.webdriver.support.ui import Select

@pytest.mark.usefixtures("test_setup")
class Test_functional_tests():

    def get_base(self):
        #this is the getter method of the base
        base = actions.BasePage(self.driver, self.wait)
        return base

    def test_open_website(self):
        self.driver.get(constants.URL)
        assert self.driver.title == constants.WEBSITE_NAME

    def test_login(self):
        base=self.get_base()
        #pass username in input
        base.presence_of_elem((By.XPATH,"//input[@id='user-name']")).send_keys(constants.UID)
        #pass password in input
        base.presence_of_elem((By.XPATH,"//input[@id='password']")).send_keys(constants.PASS)
        #click the login button
        base.elem_clickable((By.XPATH,"//input[@id='login-button']")).click()
        #assert that title is products
        base.presence_of_elem((By.XPATH,"//span[@class='title']")).text == "Products"

    # def test_login_invalid(self):
    #     base= self.get_base()
    #     #logout
    #     base.elem_clickable((By.XPATH,"//button[@id='react-burger-menu-btn']")).click()
    #     base.elem_clickable((By.XPATH,"//a[@id='logout_sidebar_link']")).click()
    #     #login with invalid creds
    #     # pass username in input
    #     base.presence_of_elem((By.XPATH, "//input[@id='user-name']")).send_keys("abc")
    #     # pass password in input
    #     base.presence_of_elem((By.XPATH, "//input[@id='password']")).send_keys("def")
    #     # click the login button
    #     base.elem_clickable((By.XPATH, "//input[@id='login-button']")).click()
    #     error= base.presence_of_elem((By.XPATH,"//h3[@data-test='error']")).text
    #     assert error == "Epic sadface: Username and password do not match any user in this service"

    def test_add_to_cart(self):
        base= self.get_base()
        lists = self.driver.find_elements(By.XPATH,"//div[@class='inventory_item_name ']")
        #action: if matches with the list of names which is present in constants , add to cart
        for i in constants.LIST_OF_ITEMS:
            for j in lists:
                if i == j.text:
                    base.presence_of_elem((By.XPATH,f"//div[normalize-space()='{i}']/ancestor::div[@class='inventory_item_description']//button")).click()
        #count the number in the badge and assert with the length of the items list which is present in constants
        num= base.presence_of_elem((By.XPATH,"//span[@class='shopping_cart_badge']")).text
        assert num == str(len(constants.LIST_OF_ITEMS))

    # def test_remove_from_cart(self):
    #     base = self.get_base()
    #     #go to cart
    #     cart= base.presence_of_elem((By.XPATH,"//a[@class='shopping_cart_link']"))
    #     cart.click()
    #     #remove button and click
    #     listofremove= self.driver.find_elements(By.XPATH,"//button[@class='btn btn_secondary btn_small cart_button']")
    #     for i in listofremove:
    #         i.click()
    #     #check invisiblity of elem located
    #     value= base.elem_invisible((By.XPATH,"//span[@class='shopping_cart_badge']"))
    #     assert value == True

    def test_checkout(self):
        base = self.get_base()
        # go to cart
        cart= base.presence_of_elem((By.XPATH,"//a[@class='shopping_cart_link']"))
        cart.click()
        #go to checkout page
        base.elem_clickable((By.XPATH,"//button[@id='checkout']")).click()
        #fill the detail
        name = constants.NAME.split(" ")
        base.presence_of_elem((By.XPATH,"//input[@id='first-name']")).send_keys(name[0])
        base.presence_of_elem((By.XPATH,"//input[@id='last-name']")).send_keys(name[1])
        base.presence_of_elem((By.XPATH,"//input[@id='postal-code']")).send_keys(constants.PIN)
        #continue button
        base.presence_of_elem((By.XPATH,"//input[@id='continue']")).click()
        #scroll till the end of the page
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #find the finish button
        base.elem_clickable((By.XPATH,"//button[@id='finish']")).click()
        head= base.presence_of_elem((By.XPATH,"//h2[@class='complete-header']")).text
        assert head=="Thank you for your order!"