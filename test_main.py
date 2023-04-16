from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from main import PoolsuiteTracker
import unittest
from pages import *
from locators import *
from time import sleep

class PoolsuiteTesting(unittest.TestCase, PoolsuiteTracker):
      #  Set up / tear down are rerun for each test function. So each test defined in this class is run separately.

      def setUp(self):
          PoolsuiteTracker.__init__(self, 'db/db.txt')

      def xtest_skip_intro(self):
          print('Running test skip intro')
          assert WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".logo"))) # check main pg fully loaded
      
      def xtest_get_channels(self):
          # self.mainPage.click_channels(self)
          self.mainPage.click_element(MainPageLocators.CHANNEL_BTN)
          self.mainPage.get_channels()
          assert WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(MainPageLocators.CHANNEL_LIST_SCROLL)) # check main pg fully loaded
      
      def xtest_select_channel(self):
          print('running test: select channel')
          self.mainPage.click_element(MainPageLocators.CHANNEL_BTN)
          self.mainPage.get_channels()
          for x in range(3,7):
            self.mainPage.select_channel(x)
            self.mainPage.click_element(MainPageLocators.CHANNEL_BTN)
            sleep(2)
          assert WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(MainPageLocators.CHANNEL_BTN))

      def xtest_check_is_playing(self):
          print('running test: is playing')
          assert self.mainPage.check_is_playing()
          self.mainPage.click_element(MainPageLocators.PLAYPAUSE)
          assert not self.mainPage.check_is_playing()
          
      def xtest_record_current_track(self):
          print('running test: record current track')
          assert self.mainPage._current_track_record is None
          self.mainPage.update_current_track()
          assert self.mainPage._current_track_record is not None
      
      def xtest_track_change(self):
          print('running test: track change *volume on!*')
          for x in [-1, 1, 0, -2]:
            sleep(5)
            self.mainPage.track_change(x)

      def xtest_maintain_db(self):
          print('running test: maintain db')
          start_len = len(self.database)
          sleep(30)
          assert len(self.database) == start_len + 1
          self.mainPage.track_change(1)
          sleep(30)
          assert len(self.database) == start_len + 2

      def test_send_email(self):
          print('runnning test: send email')
          # self.mainPage.send_email_db()
          PoolsuiteTracker.send_email_db(self)
          assert True

      def tearDown(self):
          # ? pkill -f "(chrome)?(--headless)"
          self.driver.close()
      
      

# if test is being run, not just imported, run all of unit tests defined
if __name__ == "__main__":
    unittest.main()