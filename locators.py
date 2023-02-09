from selenium.webdriver.common.by import By

class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

    CURRENT_TRACK = (By.CSS_SELECTOR, ".current-track>h3>a")
    CURRENT_ARTIST = (By.CSS_SELECTOR, ".current-track>h2>a")

