from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import unittest
import pages

class PoolsuiteTracking(unittest.TestCase):
      #  Set up / tear down are rerun for each test function. So each test defined in this class is run separately.
      def setUp(self):
          self.driver = webdriver.Chrome()
          self.driver.get('https://poolsuite.net/')

      # # runs since starts with test
      # def test_page_title(self):
      #     mainPage = pages.MainPage(self.driver)
      #     assert mainPage.is_title_matches()

      def test_reached_music(self):
          mainPage = pages.MainPage(self.driver)
          WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".outer"))) #wait for loading animation
          mainPage.press_space()
          assert WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".logo"))) # check main pg fully loaded

      def tearDown(self):
          self.driver.close()

# if test is being run, not just inmported, run all of unit tests defined
if __name__ == "__main__":
    unittest.main()