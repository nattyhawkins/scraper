from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pages
from locators import *
from element import *
from threading import Thread
from time import sleep

"""This page details the main program chain of events, leveraging methods defined on other files"""

class PoolsuiteTracker():    

      def __init__(self):
          opts = Options()
          opts.add_argument('--headless')
          assert '--headless' in opts.arguments
          self.driver = webdriver.Chrome(options=opts)
          self.driver.get('https://poolsuite.net/')
          self.mainPage = pages.MainPage(self.driver)
          self.is_playing = True

          # self.mainPage.skip_intro()
          # self.mainPage.click_element(MainPageLocators.CHANNEL_BTN)
          # self.mainPage.get_channels()
          
          # DB state
          self.database = []
          

        # The database maintenance thread
          # self.thread = Thread(target=self._maintain())
          # self.thread.daemon = True    # Kills the thread when the main process dies
          # self.thread.start()

      def _maintain(self):
          while self.is_playing:
              self.mainPage.update_current_track() #update current track record every 2 mins
              for x in range(6):
                self._update_db()
                sleep(20)          # Check every 20 seconds


      def _update_db(self):
          try:
              check = (self._current_track_record is not None
                      and (len(self.database) == 0
                            or self.database[-1] != self._current_track_record)
                      and self.is_playing())
              if check:
                  self.database.append(self._current_track_record)

          except Exception as e:
              print('error while updating the db: {}'.format(e))
 

      def tearDown(self):
          self.driver.close()

