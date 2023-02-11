from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from locators import *

#  define generic get and set methods to be used for any element targeted via locator

class BasePageElement(object):
    """Base page class that is initialized on every page object class."""

    def __set__(self, obj, value):
        """Sets the text to the value supplied, obj is the parent class where element instance is called i.e. MainPage"""
        print('setting element')
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(By.CSS_SELECTOR, self.locator))
        driver.find_element(By.CSS_SELECTOR, self.locator).clear()
        driver.find_element(By.CSS_SELECTOR, self.locator).send_keys(value)


    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        print('getting element')
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(By.CSS_SELECTOR, self.locator))
        element = driver.find_element(By.CSS_SELECTOR, self.locator)
        return element.text
    
    
# ! Elements
"""create element class by inheriting generic functionality from base"""

class CurrentTrackElement(BasePageElement):
    locator = MainPageLocators.CURRENT_TRACK
