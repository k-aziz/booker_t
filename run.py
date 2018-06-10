import random
import time

import arrow
import clockwork
import logging
from selenium import webdriver

from settings import LICENCE_NUMBER, TEST_REF, CLOCKWORK_API_KEY, APP_NAME, PHONE_NUMBER, MIN_SECONDS, MAX_SECONDS

logging.basicConfig(filename='merchant_api.log')
logger = logging.getLogger('logger')

logger.setLevel(logging.INFO)

URL = 'https://driverpracticaltest.direct.gov.uk/login'
api = clockwork.API(CLOCKWORK_API_KEY, from_name=APP_NAME)


def main():
    # Date of the last booking that was sent most recently
    last_sent_date = None
    while True:
        options = webdriver.firefox.options.Options()
        options.add_argument('--headless')
        options.add_argument('--hide-scrollbars')
        options.add_argument('--disable-gpu')

        driver = webdriver.Firefox(firefox_options=options)

        login(driver)
        logger.info('logged in')

        logger.info('retrieving available dates')
        current_test_date, earliest_available_date = find_dates(driver)

        logger.info('Current test date is {}'.format(current_test_date))

        earliest = arrow.get(earliest_available_date)
        if earliest < arrow.get(current_test_date):
            logger.info('Earlier date available on {}'.format(earliest_available_date))
            if earliest != last_sent_date:
                last_sent_date = send_message(earliest_available_date)
        else:
            logger.info('No earlier dates available')

        driver.close()

        time_delay = random.randint(MIN_SECONDS, MAX_SECONDS)
        logger.info('Last checked at {}\n'
                    'Waiting {} minutes {} seconds before checking again.\n\n'.format(arrow.now('UTC+1').format('HH:mm'),
                                                                                      time_delay // 60,
                                                                                      time_delay % 60))
        time.sleep(time_delay)


def login(driver):
    driver.get(URL)
    licence_number_elem = driver.find_element_by_id('driving-licence-number')
    test_ref_num_elem = driver.find_element_by_id('application-reference-number')

    submit_btn = driver.find_element_by_id('booking-login')

    licence_number_elem.send_keys(LICENCE_NUMBER)
    test_ref_num_elem.send_keys(TEST_REF)

    submit_btn.click()
    time.sleep(2)


def find_dates(driver):
    driver.find_element_by_id('date-time-change').click()
    radio = driver.find_element_by_id('test-choice-earliest')
    radio.click()
    radio.submit()

    time.sleep(2)

    chosen_date_elem = driver.find_element_by_xpath('//a[@class="BookingCalendar-dateLink is-chosen"]')
    chosen_date = chosen_date_elem.get_attribute('data-date')

    available_dates = driver.find_elements_by_class_name('BookingCalendar-date--bookable')
    earliest_available = available_dates[0].find_element_by_xpath('.//a[1]').get_attribute('data-date')

    return chosen_date, earliest_available


def send_message(date):
    sms_balance = float(api.get_balance()['balance'])
    if sms_balance < 0.5:
        logger.info('Clockwork sms balance is low. £{}'.format(sms_balance))

    text = 'An earlier driving test is available on {}! Book that shit fam.'.format(date)
    message = clockwork.SMS(to=PHONE_NUMBER, message=text)

    response = api.send(message)

    if response.success:
        logger.info('Text notification has been sent to {}. Response ID: {}'.format(PHONE_NUMBER, response.id))
        return arrow.get(date)

    else:
        logger.info('There has been a fucksy wucksy in the sending process!'
              'Error code: {} \nMessage: {}'.format(response.error_code, response.error_message))

        raise RuntimeError('Failed to send message. Wtf is the point of this if sending doesn\'t work?'
                           'Fix that shit.')


if __name__ == '__main__':
    main()