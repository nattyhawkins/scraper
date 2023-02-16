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

      # ...
 

      def tearDown(self):
          self.driver.close()

