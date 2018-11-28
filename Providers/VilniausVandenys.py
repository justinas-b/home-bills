from Providers.Provider import Provider
from Providers.Meter import Meter
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import  expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class VilniausVandenys(Provider):

    def retrieve_historic_data(self):
        pass

    def _login(self):

        try:
            # Open home page
            self._driver.get('https://savitarna.vv.lt/login.html')
            WebDriverWait(self._driver, 15).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="gwt-placeholder"]/div/div/div[3]/div/button')))

            # Enter username
            username_field = self._driver.find_element_by_xpath('//*[@id="gwt-placeholder"]/div/div/div[2]/div/div[1]/div/div/div[1]/input')
            username_field.click()
            username_field.send_keys(self._username)

            # Enter password
            password_field = self._driver.find_element_by_xpath('//*[@id="gwt-placeholder"]/div/div/div[2]/div/div[2]/div/div/div[1]/input')
            password_field.click()
            password_field.send_keys(self._password)

            # Login
            password_field.send_keys(Keys.ENTER)
            WebDriverWait(self._driver, 15).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="gwt-placeholder"]/div/div/div[2]/div/div[2]/div[2]/div/div[4]/a/span')))
        except Exception as e:
            print(type(e), e.args)

    def _get_bill(self):
        # Retrieve amount of money
        try:
            self._driver \
                .find_element_by_xpath('//*[@id="menu_payments"]') \
                .click()
            WebDriverWait(self._driver, 15).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="gwt-placeholder"]/div/div/div[4]/div/table/tbody/tr[1]/td[5]')))
            bill = self._driver.find_element_by_xpath('//*[@id="gwt-placeholder"]/div/div/div[4]/div/table/tbody/tr[1]/td[5]').text
            return bill
        except Exception as e:
            print(type(e), e.args)

    def _get_meters_data(self):
        try:
            # Retrieve device statistics
            self._driver.find_element_by_xpath('//*[@id="menu_dekl"]/span').click()
            WebDriverWait(self._driver, 15).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="gwt-placeholder"]/div/div/div[4]/div/table/tbody/tr/td[2]')))

            current_reading = self._driver.find_element_by_xpath('//*[@id="gwt-placeholder"]/div/div/div[4]/div/table/tbody/tr/td[6]').text
            previous_reading = self._driver.find_element_by_xpath('//*[@id="gwt-placeholder"]/div/div/div[4]/div/table/tbody/tr/td[2]').text
            difference = self._driver.find_element_by_xpath('//*[@id="gwt-placeholder"]/div/div/div[4]/div/table/tbody/tr/td[7]').text

            meter_water = Meter(provider=self.__class__.__name__ + " (Šaltas vanduo)",
                                current_reading=float(current_reading),
                                previous_reading=float(previous_reading),
                                difference=float(difference),)

            return meter_water,

        except Exception as e:
            print(type(e), e.args)

    def _logout(self):
        pass
