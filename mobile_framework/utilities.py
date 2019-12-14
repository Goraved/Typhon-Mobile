import datetime
import json
import random
import string

import allure
import gevent
import requests

from base_definitions import ROOT_DIR
from mob_configuration.config_parse import os, ENVIRONMENT, APP, GITHUB


class Utilities:

    @staticmethod
    def get_parametrized_locator(locator, parameter):
        return locator[0], locator[1].format(*parameter)

    def get_mobile_screenshot(self):
        try:
            allure.attach(self.driver.get_screenshot_as_png(), name='failure_screenshot',
                          attachment_type=allure.attachment_type.PNG)
        except:
            pass  # Local without allure

    def attach_xml_source(self):
        Utilities.get_mobile_screenshot(self)
        allure.attach(self.driver.page_source, name='xml_source', attachment_type=allure.attachment_type.XML)

    @staticmethod
    def generate_random_key(length=16):
        return ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(length)])

    @staticmethod
    def generate_random_phone_number(length=10):
        return ''.join([random.choice(string.digits) for _ in range(length)])

    @staticmethod
    def convert_dict_to_json(dictionary):
        return json.dumps(dictionary)

    @staticmethod
    def get_current_datetime():
        return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def get_current_datetime_plus_specific_days(plus_days):
        date = datetime.datetime.now() + datetime.timedelta(days=plus_days)
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def get_current_datetime_plus_specific_minutes(plus_minutes):
        date = datetime.datetime.now() + datetime.timedelta(minutes=plus_minutes)
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def get_current_datetime_minus_specific_minutes(plus_minutes):
        date = datetime.datetime.now() - datetime.timedelta(minutes=plus_minutes)
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def fix_mobile_properties():
        if os.path.isdir(f"{ROOT_DIR}/allure-results"):
            if os.path.exists(f"{ROOT_DIR}/allure-results/environment.properties"):
                remove_cycles = 10
                wait_interval = 1
                for _ in range(remove_cycles):
                    try:
                        os.remove(f"{ROOT_DIR}/allure-results/environment.properties")
                        break
                    except FileNotFoundError:
                        gevent.sleep(wait_interval)  # will be useful in parallel mode
        else:
            os.mkdir(f"{ROOT_DIR}/allure-results")
        f = open(f"{ROOT_DIR}/allure-results/environment.properties", "w+")
        f.write(f"Environment {ENVIRONMENT.upper()}\n")
        f.write(f"App {APP}\n")
        f.write(f"Git {GITHUB}\n")
        f.write(f"BrowserStack {Utilities.get_browserstack_session_url()}\n")
        f.write(f"DEVICE {os.getenv('DEVICE')}\n")
        f.write(f"PLATFORM {os.getenv('PLATFORM')}\n")
        f.write(f"BUILDBOT_URL {os.getenv('app_path')}\n")
        f.write(f"BROWSERSTACK_APP {os.getenv('app_url')}\n")

    @staticmethod
    def create_executor_file():
        if os.path.isdir(f"{ROOT_DIR}/allure-results"):
            if os.path.exists(f"{ROOT_DIR}/allure-results/executor.json"):
                remove_cycles = 10
                wait_interval = 1
                for _ in range(remove_cycles):
                    try:
                        os.remove(f"{ROOT_DIR}/allure-results/executor.json")
                        break
                    except FileNotFoundError:
                        gevent.sleep(wait_interval)  # will be useful in parallel mode
        file_exec = '''{
  "name" : "Jenkins",
  "type" : "Jenkins",
  "url" : "http://example.org",
  "buildOrder" : "%s",
  "buildName" : "Build %s",
  "buildUrl" : "%s",
  "reportName" : "Demo allure report",
  "reportUrl" : "%s/allure"
}''' % (os.getenv('BUILD_NUMBER'), os.getenv('BUILD_NUMBER'), os.getenv('BUILD_URL'), os.getenv('BUILD_URL'))
        f = open(f"{ROOT_DIR}/allure-results/executor.json", "w+")
        f.write(file_exec)

    @staticmethod
    def log(msg, msg_type='DEBUG'):
        """
        Method will write log message to the allure report int 'stdout' tab
        """
        current_time = Utilities.get_current_datetime()
        print(f'{current_time} - {msg_type}: \n {msg}\n-------')

    @staticmethod
    def generate_txt_file(name, text='test'):
        if not os.path.exists('temp_files'):
            os.makedirs('temp_files')
        file = open(f"temp_files/{name}.txt", "w")
        file.write(text)
        file.close()
        return os.path.abspath(f"temp_files/{name}.txt")

    @staticmethod
    def remove_file(name):
        if os.path.exists(name):
            os.remove(name)

    @staticmethod
    def check_correct_order(input_list, order_type='desc'):
        reverse_sort = True if order_type.lower() == 'desc' else False
        sorted_list = list(input_list)
        sorted_list.sort(reverse=reverse_sort)
        return input_list == sorted_list

    @staticmethod
    def get_browserstack_session_url():
        headers = {
            'Authorization': "Basic aW50ZWxpdHlkZXYxOk5jUmJZU3FHMWNhV0VLOVN4Y0V2"
        }
        builds_response = requests.request("GET", "https://api-cloud.browserstack.com/app-automate/builds.json",
                                           headers=headers)
        builds_json = builds_response.json()
        project_builds = [_ for _ in builds_json if
                          _['automation_build']['name'].lower() == f'ICE:{os.getenv("PLATFORM")}'.lower()]
        build_id = project_builds[0]['automation_build']['hashed_id']
        sessions_response = requests.request(
            "GET", f"https://api-cloud.browserstack.com/app-automate/builds/{build_id}/sessions.json", headers=headers)
        sessions_json = sessions_response.json()
        session_id = sessions_json[0]['automation_session']
        return session_id['browser_url'].replace('builds', 'dashboard/v2/builds')
