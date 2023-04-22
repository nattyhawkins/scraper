from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from element import *
from locators import *
from track_record import TrackRecord
from time import ctime, sleep
import os

# ! Pages
class BasePage(object):
      """Base class 'constructor' to initialize the base page that will be inherited by all pages"""
      def __init__(self, driver):
          self.driver = driver

class MainPage(BasePage):
    # Channel State
    _current_channel = 0
    channels = { 0: 'Poolsuite FM (Default)' }
    _current_track_record = None

    # Elements
    current_track_element = CurrentTrackElement()
    current_artist_element = CurrentArtistElement()
    play_element = PlayElement()
    channel_elements = ChannelElements()
    
    _is_playing = True
    
    # Methods
    def is_title_matches(self):
        """Verifies correct site is loaded"""
        return "Poolsuite" in self.driver.title
    
    def press_space(self):
        ActionChains(self.driver).key_down(Keys.SPACE).key_up(Keys.SPACE).perform()

    def skip_intro(self):
        assert self.is_title_matches()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".outer"))) #wait for loading animation
        self.press_space()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(MainPageLocators.CURRENT_TRACK)) # wait for 2nd animation
        if not self.check_is_playing():
            self.play_pause()

    def click_element(self, locator):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        button = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", button)

    def get_channels(self):
        self.click_element(MainPageLocators.CHANNEL_BTN)
        channels = self.channel_elements
        print('\nChannels:')
        for (i, channel) in enumerate(channels):
            print(f'{i}. {channel.text}')
            self.channels[i] = channel.text
        self.click_element(MainPageLocators.CHANNEL_BTN)
      
    def select_channel(self, channel={lambda _current_channel: _current_channel + 1 % 7}):
        # print(f'selecting channel {channel}')
        self.click_element(MainPageLocators.CHANNEL_BTN)
        locator = (By.CSS_SELECTOR, f".select-options-scroll li:nth-of-type({channel + 1})")
        if (channel > 3):
            ActionChains(self.driver).move_to_element(self.driver.find_element(*locator)).perform()
        self.click_element(locator)
        self._current_channel = channel
        print(f"Now playing from: {self.channels[self._current_channel]}")

    def check_is_playing(self):
        is_paused = self.play_element[0].get_attribute('class').find('paused')
        self._is_playing = is_paused < 1
        return is_paused < 1
   
    def play_pause(self):
        self.click_element(MainPageLocators.PLAYPAUSE)
        self._is_playing = False

    def track_change(self, action: int):
        """perform track change and keep track of currently playing record"""
        # print(f'track change: {action}')
        if action < 0:
            # once to restart, twice for previous
            for x in range(abs(action)):
                self.click_element(MainPageLocators.PREV)
        elif action == 0:
            self.play_pause()
        elif action > 0:
            for x in range(action):
              self.click_element(MainPageLocators.NEXT)
        
        self.update_current_track()

    def update_current_track(self):
        # if self.check_is_playing():
        self._current_track_record = self.get_current_track_record()
            # print(f"current record: {self._current_track_record} | end")

    def get_current_track_record(self):
        """if still playing after 5s, create record"""
        try:
            channel = self.channels[self._current_channel]
            title = self.current_track_element[0].text
            artist = self.current_artist_element[0].text
            url = self.current_track_element[0].get_attribute('href')
            
            record = TrackRecord(channel, title, artist, url, ctime())
            print(record)
            return record
        except Exception as e:
            print('there was an error: {}'.format(e))
        return None
    
    def welcome(self):
        print('Welcome to this Poolsuite music scraper! Your listening history will be recorded and emailed to you. Note: this project is just for fun and not affiliated with Poolsuite.')
        self._user_address = input("What is your email address? You can skip this to listen anyway: ")
        print(f"Thanks! We will try sending your track history to: '{self._user_address}' ")

    def menu(self):
        print("""
          Controls:
            -2: Back
            -1: Restart
            0: Play/Pause
            1: Next

          Change channel:
            Select channel from above e.g. "C3"

          Q: Quit
        """)





