from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from element import BasePageElement
from locators import *


# ! Pages
class BasePage(object):
      """Base class 'constructor' to initialize the base page that will be inherited by all pages"""
      def __init__(self, driver):
          self.driver = driver

class MainPage(BasePage):
    
    # current_track_element = CurrentTrackElement()

    def is_title_matches(self):
        """Verifies correct site is loaded"""
        return "Poolsuite" in self.driver.title
    
    def press_space(self):
        """space to skip welcome animation"""
        ActionChains(self.driver).key_down(Keys.SPACE).key_up(Keys.SPACE).perform()

    def skip_intro(self):
        print('skipping intro')
        # mainPage = pages.MainPage(self.driver)
        assert self.mainPage.is_title_matches()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".outer"))) #wait for loading animation
        self.mainPage.press_space()

    def click_channels(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(MainPageLocators.CHANNEL_BTN)) #wait for music box
        button = self.driver.find_element(*MainPageLocators.CHANNEL_BTN)
        print('clicking channels')
        # button.click()
        self.driver.execute_script("arguments[0].click();", button)

    def get_channels(self):
        print('getting channels')
        self.channels = self.driver.find_elements(*MainPageLocators.ALL_CHANNELS)
        print('\nChannels:')
        for (i, channel) in enumerate(self.channels):
            print(f'{i}. {channel.text}')
      
    def select_channel(self, channel={lambda _current_channel: _current_channel + 1 % 7}):
        print('selecting channel')
        if (channel < 4):
          # click channel
          print('DO')
        else:
          # click scroll then channel
          print('DO')
        
        self._current_channel = channel
    
    def record_track(self):
        # access element setter by saving to a new variable
        track_name = self.current_track_element

# track = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".current-track>h3>a")))
# elem = driver.find_element(By.CSS_SELECTOR, ".current-track>h3>a")

