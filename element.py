from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from locators import *

#  define generic get and set methods to be used for any element targeted via locator

class BasePageElement(object):
    """Base page class that is initialized on every page object class."""
    # def __init__(self, driver):
    #       self.driver = driver
          
    def __set__(self, obj, value):
        """Sets the text to the value supplied, obj is the parent class where element instance is called i.e. MainPage"""
        print('__set__ element')
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.locator))
        driver.find_element(*self.locator).clear()
        driver.find_element(*self.locator).send_keys(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        print('__get__ element')
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_elements(*self.locator))
        elements = driver.find_elements(*self.locator)
        return elements

    # def click(self):
    #     print('clicking element')
    #     WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.locator))
    #     button = self.driver.find_element(*self.locator)
    #     self.driver.execute_script("arguments[0].click();", button)
    
    
# ! Elements
"""create element class by inheriting generic functionality from base"""

class CurrentTrackElement(BasePageElement):
      locator = MainPageLocators.CURRENT_TRACK
      element = BasePageElement()

class ChannelButtonElement(BasePageElement):
      element = BasePageElement()
      locator = MainPageLocators.CHANNEL_BTN
      

class ChannelElements(BasePageElement):
      # element = BasePageElement()
      locator = MainPageLocators.ALL_CHANNELS
        
class SelectedChannelElement(BasePageElement):
      """locator must be passed depending on which channel is selected"""
      def __init__(self, locator):
        self.locator = locator
        self.element = BasePageElement()

