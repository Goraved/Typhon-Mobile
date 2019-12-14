import json
import os
from copy import copy
from datetime import datetime

from appium import webdriver

from mobile_framework.mobile.devices import DEVICES
from mobile_framework.utilities import Utilities


class Driver:

    def __init__(self, address, port, test_class):
        platform = os.getenv('PLATFORM', 'android')
        device_name = os.getenv('DEVICE', 'test_emu')
        device = DEVICES[device_name]
        self.app = os.getenv('app_path', '').strip()
        if 'br_' in device_name:
            self.app = os.getenv('app_url', '').strip()
            if 'Tablet' in test_class and platform == 'android':
                device = DEVICES['br_nexus_tab']
                os.environ['TAB'] = "True"
            elif 'Tablet' in test_class and platform == 'ios':
                device = DEVICES['br_ipad_tab']
                os.environ['TAB'] = "True"
            else:
                os.environ['TAB'] = ""

        settings = {
            'ios': {
                'xcodeOrgId': '748CDJ9KNG',
                'xcodeSigningId': 'iPhone Developer',
                'app': self.app,
                'autoAcceptAlerts': False,
                'autoDismissAlerts': False,
                'automationName': 'XCUITest',
                'noReset': True,
                'waitForQuiescence': False
            },
            'android': {
                'app': self.app,
                'autoGrantPermissions': True,
                'appPackage': f'com.test.test.{os.getenv("ANDROID_PACKAGE")}',
                'appActivity': 'com.test.test.activities.TestLauncherActivity',
                'noSign': True,
                'noReset': False
            }
        }
        desired_caps = copy(settings[platform])
        desired_caps['platformName'] = platform.replace('_demo', '')
        desired_caps.update(device)
        Utilities.log(json.dumps(desired_caps), 'DESIRE_CAPS')
        if 'br_' in device_name:
            br_user_name = os.getenv('br_user_name')
            br_access_key = os.getenv('br_access_key')
            desired_caps['project'] = 'Test Project Name'
            desired_caps['build'] = f'Test:{os.getenv("PLATFORM").upper()}'
            time = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            desired_caps['name'] = f'Test:{test_class}_{time}'
            desired_caps['browserstack.appium_version'] = '1.15.0'
            self.instance = webdriver.Remote(
                f"https://{br_user_name}:{br_access_key}@hub-cloud.browserstack.com/wd/hub", desired_caps)
        else:
            self.instance = webdriver.Remote(f"http://{address}:{port}/wd/hub", desired_caps)
        os.environ['os_version'] = desired_caps.get('platformVersion', '')
