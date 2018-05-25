from unittest import TestCase

from selenium import webdriver

from run import send_message, login, find_dates


class TestBookerT(TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def test_login(self):
        login(self.driver)

        self.assertNotIn('Access your booking', self.driver.title)
        self.assertIn('Booking details', self.driver.title)

    def test_find_dates(self):
        chosen_date, earliest_date = find_dates(self.driver)

        self.assertIsNotNone(chosen_date)
        self.assertIsNotNone(earliest_date)

    def test_send_message(self):
        send_message('2018-05-22')
