from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pages


class PoolsuiteTracker():
      def __init__(self):
          opts = Options()
          opts.add_argument('--headless')
          assert opts.headless
          self.driver = webdriver.Chrome(options=opts)
          self.driver.get('https://poolsuite.net/')
          # self.mainPage = pages.MainPage(self.driver)

          # Track list related state
          self._current_track_number = 1
          self.track_list = []
          self.tracks()

      def skip_intro(self):
          mainPage = pages.MainPage(self.driver)
          assert mainPage.is_title_matches()
          WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".outer"))) #wait for loading animation
          print('page loaded, pressing space')
          mainPage.press_space()
          print('skip intro complete')
          

      def get_channels(self):
        '''
        Query page to create list of available channels
        '''
        self.skip_intro()



 

      def tearDown(self):
          self.driver.close()