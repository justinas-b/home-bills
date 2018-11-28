from Providers.Provider import Provider
from Providers.Meter import Meter
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import  expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import os
import tabula


class CHC(Provider):

    def retrieve_historic_data(self):
        pass

    # def __init__(self, **kwargs):
    #     super(self.__class__, self).__init__(**kwargs)

    def _login(self):

        try:
            # Open home page
            self._driver.get('https://savitarna.chc.lt/saskaitos/')
            WebDriverWait(self._driver, 15).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="btn"]')))

            # Enter username
            username_field = self._driver.find_element_by_xpath('//*[@id="txt1"]')
            username_field.click()
            username_field.send_keys(self._username)

            # Enter password
            password_field = self._driver.find_element_by_xpath('//*[@id="txt2"]')
            password_field.click()
            password_field.send_keys(self._password)

            # Login
            password_field.send_keys(Keys.ENTER)
            WebDriverWait(self._driver, 15).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="form1"]/div[3]/div[4]/a[2]')))
        except Exception as e:
            print(type(e), e.args)

    def _get_bill(self):
        # Retrieve amount of money
        try:
            self._driver.find_element_by_xpath("/html/body").send_keys(Keys.ESCAPE)
            self._driver \
                .find_element_by_xpath('//*[@id="form1"]/div[3]/div[4]/a[2]/span[1]') \
                .click()
            WebDriverWait(self._driver, 15).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="gv"]/tbody/tr[2]/td[2]')))
            bill = self._driver.find_element_by_xpath('//*[@id="gv"]/tbody/tr[2]/td[2]').text
            return bill
        except Exception as e:
            print(type(e), e.args)

    def _get_meters_data(self):
        try:
            self._driver.find_element_by_xpath("/html/body").send_keys(Keys.ESCAPE)
            self._driver \
                .find_element_by_xpath('//*[@id="form1"]/div[3]/div[4]/a[2]/span[1]') \
                .click()
            WebDriverWait(self._driver, 15).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="gv"]/tbody/tr[2]/td[2]')))

            # Download bill
            self._driver.execute_script("javascript:__doPostBack('gv','Saskaita$0')")
            _ = self._get_download_progress() # Wait for bill to be downloaded
            files = [os.path.join(self._downloads_dir, file)
                     for file
                     in os.listdir(self._downloads_dir)
                     if file.endswith(".pdf")]
            file = files.pop()

            # Process PDF
            left, top, width, height, page = 19.26, 329, 248.44, 33.37, 1
            java_options = ["-Djava.awt.headless=true", "-Dfile.encoding=UTF8",
                            "-Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider",]

            water = tabula.read_pdf(file, area=(top, left, top + height, left + width), pages=page, lattice=True,
                                    java_options=java_options)

            left, top, width, height, page = 19.11, 565.35, 343.06, 43.41, 2
            heating = tabula.read_pdf(file, area=(top, left, top + height, left + width), pages=page, lattice=True,
                                      java_options=java_options)

            # Cleanup downloaded files
            self._cleanup_downloads_dir()

            meter_water = Meter(provider=self.__class__.__name__ + " (Karštas vanduo)",
                                difference=float(water.Skirtumas[0].replace(',', '.')),
                                previous_reading=float(water.Nuo[0].replace(',', '.')),
                                current_reading=float(water.Iki[0].replace(',', '.')),)

            meter_heating = Meter(provider=self.__class__.__name__ + " (Šildymas)",
                                  difference=float(heating['Skirtumas\r(Suvartotas kiekis)'][0].replace(',', '.')),
                                  previous_reading=float(heating.Nuo[0].replace(',', '.')),
                                  current_reading=float(heating.Iki[0].replace(',', '.')),)

            return meter_water, meter_heating

        except Exception as e:
            print(type(e), e.args)

    def _logout(self):
        pass
