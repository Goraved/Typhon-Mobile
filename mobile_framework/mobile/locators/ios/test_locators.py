from appium.webdriver.common.mobileby import MobileBy


class TestLocators:
    test_button = (MobileBy.XPATH, '//XCUIElementTypeOther/XCUIElementTypeButton')
    test_input = (MobileBy.XPATH, '//XCUIElementTypeOther/XCUIElementTypeInput')
