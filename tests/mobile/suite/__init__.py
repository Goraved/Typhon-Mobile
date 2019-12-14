import os

from allure_commons._allure import step

from mobile_framework.mobile.pages.test_screen import AdvertisingScreen
from mobile_framework.mobile.pages.comment_card_screen import CommentCardScreen
from mobile_framework.mobile.pages.custom_screen import CustomScreen
from mobile_framework.mobile.pages.daily_events_screen import DailyEventsScreen
from mobile_framework.mobile.pages.dashboard_page import DashboardScreen
from mobile_framework.mobile.pages.digital_key.login_screen import LoginScreen
from mobile_framework.mobile.pages.digital_key.reservations_screen import ReservationScreen
from mobile_framework.mobile.pages.dining_screen import DiningScreen
from mobile_framework.mobile.pages.housekeeping_screen import RequestsScreen
from mobile_framework.mobile.pages.ice_screen import IceScreen
from mobile_framework.mobile.pages.maps_screen import MapsScreen
from mobile_framework.mobile.pages.recreaction_screen import RecreationScreen
from mobile_framework.mobile.pages.spa_screen import SpaScreen
from mobile_framework.mobile.pages.store_screen import StoreScreen
from mobile_framework.mobile.pages.transportation_screen import TransportationScreen
from tests.mobile import TestBase


class TestSuite(TestBase):

    @classmethod
    def setup_class(cls):
        test_class = cls.pytestmark[0].args[0]
        super(TestSuite, cls).setup_class(test_class)
        with step('Initialise class'):
            cls.test_screen = IceScreen(cls.driver)
            cls.comment_card_screen = CommentCardScreen(cls.driver)
            cls.login_screen = LoginScreen(cls.driver)
            cls.reservation_screen = ReservationScreen(cls.driver)
            cls.recreation_screen = RecreationScreen(cls.driver)
            cls.store_screen = StoreScreen(cls.driver)
            cls.services_screen = RequestsScreen(cls.driver)
            cls.custom_screen = CustomScreen(cls.driver)
            cls.advertising_screen = AdvertisingScreen(cls.driver)
            cls.transportation_screen = TransportationScreen(cls.driver)
            cls.dining_screen = DiningScreen(cls.driver)
            cls.maps_screen = MapsScreen(cls.driver)
            cls.daily_events_screen = DailyEventsScreen(cls.driver)
            cls.spa_screen = SpaScreen(cls.driver)
            cls.dashboard_screen = DashboardScreen(cls.driver)
            cls.ice_screen.wait_till_loader_disappear()
        if os.getenv('PLATFORM') == 'ios':
            cls.ice_screen.accept_alert()
            cls.ice_screen.open_and_close_profile_menu()
        with step('Change remote settings'):
            cls.ice_screen.change_remote_settings()

    def teardown_method(self):
        with step('Close app'):
            self.driver.close_app()
        with step('Open app'):
            self.driver.launch_app()
