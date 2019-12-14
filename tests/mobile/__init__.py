import os
import subprocess

import allure
import gevent
import pytest
from urllib3.exceptions import MaxRetryError

from mobile_framework.mobile.driver import Driver
from mobile_framework.utilities import Utilities


class TestBase:
    driver = None

    @classmethod
    def setup_class(cls, test_class):
        cls.address = '0.0.0.0'
        cls.port = '4327'
        cls.appium_server = subprocess.Popen([f"appium --address {cls.address} --port {cls.port}"], shell=True)
        gevent.sleep(5)
        try:
            for _ in range(5):
                try:
                    cls.driver = Driver(cls.address, cls.port, test_class).instance
                    break
                except Exception as e:
                    print(f'Driver setup crashed - {e}')
                    gevent.sleep(1)
            if os.getenv('PLATFORM') == 'android':  # dunno how to implement for iOS
                crash = True
                for _ in range(5):
                    if cls.driver.current_activity != 'com.test.test.core.activities.TestApplication':
                        cls.driver.reset()
                        gevent.sleep(1)
                    else:
                        crash = False
                        break
                if crash:
                    raise Exception('App crashes!')
        except MaxRetryError:
            cls.appium_server.kill()
            raise Exception('Too many appium servers run')

    @classmethod
    def teardown_class(cls):
        Utilities.fix_mobile_properties()
        cls.driver.quit()
        if 'emu' in os.getenv('DEVICE', ''):
            subprocess.Popen(["adb emu kill"], shell=True)
        cls.appium_server.kill()

    @pytest.fixture(autouse=True)
    def fail_screenshot(self, request):
        yield
        # request.node is an "item" because we use the default
        if request.node.rep_setup.failed or request.node.rep_call.failed:
            Utilities.get_mobile_screenshot(self)

    @staticmethod
    @allure.step('Compare actual and expected values')
    def compare_values(field, actual_value, expected_value):
        assert actual_value == expected_value, f"{field} is - '{actual_value}' instead of - '{expected_value}'"
