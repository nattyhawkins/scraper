from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from element import *
from locators import *


# ! Pages
class BasePage(object):
      """Base class 'constructor' to initialize the base page that will be inherited by all pages"""
      def __init__(self, driver):
          self.driver = driver

class MainPage(BasePage):
          
    # Track list related state
    _current_channel = 0
    channels = { 0: 'default' }

    # current_track_element = CurrentTrackElement()
    channel_elements = ChannelElements()

    def is_title_matches(self):
        """Verifies correct site is loaded"""
        return "Poolsuite" in self.driver.title
    
    def press_space(self):
        """space to skip welcome animation"""
        ActionChains(self.driver).key_down(Keys.SPACE).key_up(Keys.SPACE).perform()

    def skip_intro(self):
        print('skipping intro')
        # mainPage = pages.MainPage(self.driver)
        assert self.is_title_matches()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".outer"))) #wait for loading animation
        self.press_space()

    def click_element(self, locator):
        print('clicking element')
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        button = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", button)

    def get_channels(self):
        print('getting channels - page')
        channels = self.channel_elements
        print('\nChannels:')
        for (i, channel) in enumerate(channels):
            print(f'{i}. {channel.text}')
            self.channels[i] = channel.text
      
    def select_channel(self, channel={lambda _current_channel: _current_channel + 1 % 7}):
        print(f'selecting channel {channel}')
        locator = (By.CSS_SELECTOR, f".select-options-scroll li:nth-of-type({channel + 1})")
        if (channel > 3):
            print('scroll down')
            ActionChains(self.driver).move_to_element(self.driver.find_element(*locator)).perform()
        self.click_element(locator)
        self._current_channel = channel
        print(self.channels[self._current_channel]
)
    
    
    
    def record_track(self):
        # access element setter by saving to a new variable
        track_name = self.current_track_element

# track = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".current-track>h3>a")))
# elem = driver.find_element(By.CSS_SELECTOR, ".current-track>h3>a")

