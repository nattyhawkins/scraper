from selenium import webdriver
from selenium.webdriver.common import by as By, keys as Keys
# from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('https://poolsuite.net/')
assert "Poolsuite" in driver.title
driver.key_down(Keys.SPACE)
elem = driver.find_element(By.CSS_SELECTOR, ".current-track>h3>a")
print(elem.innerText)

