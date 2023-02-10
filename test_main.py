from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from main import PoolsuiteTracker
import unittest
import pages

class PoolsuiteTesting(unittest.TestCase):
      #  Set up / tear down are rerun for each test function. So each test defined in this class is run separately.
      def setUp(self):
          opts = Options()
          opts.add_argument('--headless')
          assert '--headless' in opts.arguments
          print('setting driver')
          self.driver = webdriver.Chrome(options=opts)
          print('getting poolsuite')
          self.driver.get('https://poolsuite.net/')

      def test_skip_intro(self):
          print('Running test')
          PoolsuiteTracker.skip_intro(self)
          assert WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".logo"))) # check main pg fully loaded

      def tearDown(self):
          self.driver.close()

# if test is being run, not just inmported, run all of unit tests defined
if __name__ == "__main__":
    unittest.main()