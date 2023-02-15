from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from main import PoolsuiteTracker
import unittest
from unittest.mock import Mock
from pages import *
from locators import *
import time

class PoolsuiteTesting(unittest.TestCase):
      #  Set up / tear down are rerun for each test function. So each test defined in this class is run separately.
      # channel_button_element = ChannelButtonElement()
      channel_elements = ChannelElements()


      def setUp(self):
          PoolsuiteTracker.__init__(self)
          # self.skip_intro = PoolsuiteTracker.skip_intro
          # opts = Options()
          # opts.add_argument('--headless')
          # assert '--headless' in opts.arguments
          # print('setting driver')
          # self.driver = webdriver.Chrome(options=opts)
          # print('getting poolsuite')
          # self.driver.get('https://poolsuite.net/')
          # self.mainPage = pages.MainPage(self.driver)

      def xtest_skip_intro(self):
          print('Running test skip intro')
          self.mainPage.skip_intro(self)
          assert WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".logo"))) # check main pg fully loaded
      
      def xtest_get_channels(self):
          self.mainPage.skip_intro()
          # self.mainPage.click_channels(self)
          self.mainPage.click_element(MainPageLocators.CHANNEL_BTN)
          self.mainPage.get_channels()
          assert WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(MainPageLocators.CHANNEL_LIST_SCROLL)) # check main pg fully loaded
      
      def xtest_select_channel(self):
          print('running test: select channel')
          self.mainPage.skip_intro()
          self.mainPage.click_element(MainPageLocators.CHANNEL_BTN)
          self.mainPage.get_channels()
          for x in range(3,7):
            self.mainPage.select_channel(x)
            self.mainPage.click_element(MainPageLocators.CHANNEL_BTN)
            time.sleep(2)
          assert WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(MainPageLocators.CHANNEL_BTN))
      
      def xtest_buttons(self):
          print('running test: buttons *volume on!*')
          self.mainPage.skip_intro()
          time.sleep(5)
          self.mainPage.click_element(MainPageLocators.NEXT)
          time.sleep(5)
          self.mainPage.click_element(MainPageLocators.PREV)
          self.mainPage.click_element(MainPageLocators.PREV)
          time.sleep(5)
          self.mainPage.click_element(MainPageLocators.PLAY)
          time.sleep(5)
          self.mainPage.click_element(MainPageLocators.PLAY)
          time.sleep(5)

      def test_is_playing(self):
          print('running test: is playing')
          self.mainPage.skip_intro()
          time.sleep(3)
          assert self.mainPage.is_playing()
          self.mainPage.click_element(MainPageLocators.PLAY)
          assert not self.mainPage.is_playing()

          

      def tearDown(self):
          self.driver.close()

# if test is being run, not just inmported, run all of unit tests defined
if __name__ == "__main__":
    unittest.main()