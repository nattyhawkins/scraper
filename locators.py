from selenium.webdriver.common.by import By

class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

    # ! Channel
    # CHANNEL_BTN = (By.XPATH,"//strong[text()='Channel:']")
    CHANNEL_BTN = (By.CLASS_NAME,"select-wrapper")
    CHANNEL_LIST_SCROLL = (By.CLASS_NAME,"select-options-scroll")
    ALL_CHANNELS = (By.CSS_SELECTOR, ".select-options-scroll li")
    

    # ! Track
    CURRENT_TRACK = (By.CSS_SELECTOR, ".current-track>h3>a")
    CURRENT_ARTIST = (By.CSS_SELECTOR, ".current-track>h2>a")
    PREV = (By.CLASS_NAME, "first")
    PLAYPAUSE = (By.CLASS_NAME, "middle")
    NEXT = (By.CLASS_NAME, "last")

