from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from element import BasePageElement
from locators import *

# ! Elements
class CurrentTrackElement(BasePageElement):
    """create ele ment class by inheriting generic functionality from base"""
    locator = MainPageLocators.CURRENT_TRACK


# ! Pages
class BasePage(object):
      """Base class 'constructor' to initialize the base page that will be inherited by all pages"""
      def __init__(self, driver):
          self.driver = driver

class MainPage(BasePage):
    
    current_track_element = CurrentTrackElement()

    def is_title_matches(self):
        """Verifies page title"""
        return "Poolsuite" in self.driver.title
    
    def press_space(self):
        """space to skip welcome animation"""
        ActionChains(self.driver).key_down(Keys.SPACE).key_up(Keys.SPACE).perform()



# track = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".current-track>h3>a")))
# elem = driver.find_element(By.CSS_SELECTOR, ".current-track>h3>a")

