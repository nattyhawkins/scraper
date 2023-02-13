from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pages
from locators import *
from element import *

"""This page details the main program chain of events, leveraging methods defined on other files"""

class PoolsuiteTracker():    

      def __init__(self):
          opts = Options()
          opts.add_argument('--headless')
          assert '--headless' in opts.arguments
          self.driver = webdriver.Chrome(options=opts)
          self.driver.get('https://poolsuite.net/')
          self.mainPage = pages.MainPage(self.driver)

          

      # def skip_intro(self):
      #     print('skipping intro')
      #     # mainPage = pages.MainPage(self.driver)
      #     assert self.mainPage.is_title_matches()
      #     WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".outer"))) #wait for loading animation
      #     self.mainPage.press_space()
          
      def get_channels(self):
          print('getting channels main')
          self.skip_intro(self)
          self.mainPage.click_channels()
          self.channels = self.driver.find_elements(*MainPageLocators.ALL_CHANNELS)
          print('\nChannels:')
          for (i, channel) in enumerate(self.channels):
              print(f'{i}. {channel.text}')
      
      def select_channel(self):
          print('selecting channel')
          self.skip_intro(self)





 

      def tearDown(self):
          self.driver.close()

