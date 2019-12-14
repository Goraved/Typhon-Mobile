import os

from mobile_framework.mobile.base_mobile import BaseMobile

if os.getenv('PLATFORM') == 'android':
    from mobile_framework.mobile.locators.android.test_locators import *
elif os.getenv('PLATFORM') == 'ios':
    from mobile_framework.mobile.locators.ios.test_locators import *


class TestScreen(BaseMobile):
    def open_test_menu(self):
        self.tap(*TestLocators.test_button)

    def fill_test_field(self):
        self.tap(*TestLocators.test_input)