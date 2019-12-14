import os
import platform

import configparser

env_config = configparser.ConfigParser()
ENVIRONMENT = os.getenv('ENVIRONMENT', 'STG')
env_config.read_file(open(f'{os.path.dirname(os.path.abspath(__file__))}/{ENVIRONMENT.lower()}.ini'))

global_config = configparser.ConfigParser()
global_config.read_file(open(f'{os.path.dirname(os.path.abspath(__file__))}/global.ini'))

# Environment settings
APP = f"{os.getenv('PLATFORM', '')}_demo_app"
OS_NAME = platform.system()
OS_VERSION = platform.version()
OS_ARCHITECTURE = platform.architecture()
PROJECT = global_config.get('ENVIRONMENT', 'project')
LINK_TYPE_TEST_CASE = global_config.get('ENVIRONMENT', 'link_type_test_case')
LINK_TYPE_LINK = global_config.get('ENVIRONMENT', 'link_type_link')
TEST_CASE = global_config.get('ENVIRONMENT', 'test_case')
EMAIL_RECIPIENTS = ['[email recipient]']
GITHUB = global_config.get('ENVIRONMENT', 'git_path')
BROWSERSTACK = global_config.get('ENVIRONMENT', 'br_path')
EMAIL_FROM = f"{PROJECT} QA TEAM"
EMAIL_SENDER = '[email sender]'
JSON_URL = env_config.get('PATH', 'json_url')
JSON_TAB_URL = env_config.get('PATH', 'json_tab_url')
