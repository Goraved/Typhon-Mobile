from appium.webdriver.common.mobileby import MobileBy


class TestLocators:
    test_button = (MobileBy.XPATH, '//android.widget.LinearLayout/button')
    test_input = (MobileBy.XPATH, '//android.widget.LinearLayout/input')
