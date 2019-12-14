import os

import allure
import pytest
from allure_commons._allure import step

from mob_configuration.config_parse import TEST_CASE
from tests.mobile.suite import TestSuite


@allure.feature('Feature')
class TestAdvertising(TestSuite):

    @allure.title('When ads are displayed, user should be able to click and view the ad')
    @allure.link(TEST_CASE + '327967', 'test_case', 'TEST CASE')
    def test_advertising(self):
        with step('Tap on ad screen'):
            self.advertising_screen.open_advertising_menu()
        with step('Check ad screen opened and contains ads'):
            self.advertising_screen.check_correctness_of_ad_menu()

    @allure.title('Ad displays correctly when Language is changed')
    @allure.link(TEST_CASE + '327941', 'test_case', 'TEST CASE')
    @pytest.mark.skipif(os.getenv('PLATFORM') == 'android', reason='Unstable on android')
    def test_advertising_works_with_changed_language(self):
        with step('Switch language to Russian'):
            self.ice_screen.language_switch('russian')
        with step('Tap on ad screen'):
            self.advertising_screen.open_advertising_menu()
        with step('Check ad screen opened and contains ads'):
            self.advertising_screen.check_correctness_of_ad_menu()
        with step('Switch language to English'):
            self.ice_screen.language_switch('english')
