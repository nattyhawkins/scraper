from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from main import PoolsuiteTracker
from selenium.webdriver.chrome.options import Options
import unittest
from pages import *
from locators import *
from time import sleep

class PoolsuiteTesting(unittest.TestCase, PoolsuiteTracker):

      def setUp(self):
          PoolsuiteTracker.__init__(self, 'db/db.txt')
          self.mainPage.skip_intro()
          self.start_db()
                    
      def xtest_skip_intro(self):
          print('Running test: skip intro')
          assert WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".logo"))) # check main pg fully loaded
      
      def xtest_get_channels(self):
          print('Running test: get channels')
          self.mainPage.get_channels()
          assert WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(MainPageLocators.PLAYPAUSE)) # check main pg fully loaded
      
      def xtest_ensure_is_playing(self):
          self.mainPage.get_channels()
          self.mainPage.select_channel(3)
          assert self.mainPage.check_if_playing()

      def xtest_select_channel(self):
          print('Running test: select channel')
          self.mainPage.get_channels()
          for x in range(0,7):
            self.mainPage.select_channel(x)
            assert self.mainPage._current_channel == x
            sleep(2)
          assert WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(MainPageLocators.CHANNEL_BTN))

      def xtest_check_if_playing(self):
          print('Running test: is playing')
          assert self.mainPage.check_if_playing()
          self.mainPage.click_element(MainPageLocators.PLAYPAUSE)
          assert not self.mainPage.check_if_playing()
          
      def xtest_record_current_track(self):
          print('Running test: record current track')
          assert self.mainPage._current_track_record is None
          self.mainPage.update_current_track()
          assert self.mainPage._current_track_record is not None
      
      def xtest_track_change(self):
          print('Running test: track change *volume on!*')
          for x in [-1, 1, 0, -2]:
            sleep(5)
            self.mainPage.track_change(x)

      def test_maintain_db(self):
          print('Running test: maintain db')
          start_len = len(self.database)
          sleep(25)
          assert len(self.database) == start_len + 1
          self.mainPage.track_change(1)
          sleep(25)
          assert len(self.database) == start_len + 2

      def xtest_send_email(self):
          """ Sends email to default developer email """
          print('runnning test: send email')
          response = self.send_email_db()
          assert response.status_code == 202

      def xtest_program(self):
          print('Running test: program')
          self.start()
          assert True

      def tearDown(self): 
          # ? pkill -f "(chrome)?(--headless)" // Run in CLI to terminate any rogue headless browser instances
          print('Bye!')
          self.driver.close()
      

# if test is being run, not just imported, run all of unit tests defined
if __name__ == "__main__":
    unittest.main()