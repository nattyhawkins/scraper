from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from locators import *

#  define generic get and set methods to be used for any element targeted via locator

class BasePageElement(object):
    """Base page class that is initialized on every page object class."""
          
    def __set__(self, obj, value):
        """Sets the text to the value supplied, obj is the parent class where element instance is called i.e. MainPage"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.locator))
        driver.find_element(*self.locator).clear()
        driver.find_element(*self.locator).send_keys(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified object. NOTE select first index if getting one element!"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_elements(*self.locator))
        elements = driver.find_elements(*self.locator)
        return elements
    
    
# ! Elements
"""create element class by inheriting generic functionality from base"""

class CurrentTrackElement(BasePageElement):
      locator = MainPageLocators.CURRENT_TRACK

class CurrentArtistElement(BasePageElement):
      locator = MainPageLocators.CURRENT_ARTIST

class ChannelButtonElement(BasePageElement):
      locator = MainPageLocators.CHANNEL_BTN

class ChannelElements(BasePageElement):
      # element = BasePageElement()
      locator = MainPageLocators.ALL_CHANNELS
        
class SelectedChannelElement(BasePageElement):
      """locator must be passed referencing which channel is selected"""
      def __init__(self, locator):
        self.locator = locator

class PlayElement(BasePageElement):
      locator = MainPageLocators.PLAYPAUSE

