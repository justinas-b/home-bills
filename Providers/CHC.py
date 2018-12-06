from Models.Provider import Provider
from Models.Meter import Meter
from Models.DateTranslator import DateTranslator
from Models.Service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import os
import camelot

class CHC(Provider):

    def _login(self):

        try:
            # Open home page
            self._driver.get('https://savitarna.chc.lt/saskaitos/')
            WebDriverWait(self._driver, self._timeout).until(expected_conditions.presence_of_element_located(
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
            WebDriverWait(self._driver, self._timeout).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="form1"]/div[3]/div[4]/a[2]')))

            self._driver.find_element_by_xpath("/html/body").send_keys(Keys.ESCAPE)

        except Exception as e:
            print(type(e), e.args)

    def _download_bill(self):
        self._driver \
            .find_element_by_xpath('//*[@id="form1"]/div[3]/div[4]/a[2]/span[1]') \
            .click()
        WebDriverWait(self._driver, self._timeout).until(expected_conditions.presence_of_element_located(
            (By.XPATH, '//*[@id="gv"]/tbody/tr[2]/td[2]')))

        self._driver.execute_script("javascript:__doPostBack('gv','Saskaita$0')")
        self._get_download_progress()  # Wait for bill to be downloaded
        files = [os.path.join(self._downloads_dir, file)
                 for file
                 in os.listdir(self._downloads_dir)
                 if file.endswith(".pdf")]
        return files.pop()

    def _get_bill_date(self):
        date = self._driver.find_element_by_xpath('//*[@id="gv"]/tbody/tr[2]/td[1]').text
        year, _, month, _ = date.split()
        month = DateTranslator.translate_month_name(month)
        return year, month

    def _get_bill_total(self):
        # Retrieve amount of money
        try:
            self._driver.find_element_by_xpath("/html/body").send_keys(Keys.ESCAPE)
            self._driver \
                .find_element_by_xpath('//*[@id="form1"]/div[3]/div[4]/a[2]/span[1]') \
                .click()
            WebDriverWait(self._driver, self._timeout).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="gv"]/tbody/tr[2]/td[2]')))
            bill = self._driver.find_element_by_xpath('//*[@id="gv"]/tbody/tr[2]/td[2]').text.split()
            return bill[0]
        except Exception as e:
            print(type(e), e.args)

    def _get_services(self):
        try:
            # Process PDF
            water_table = camelot.read_pdf(
                filepath=self._bill_file_name, pages="1", flavor="stream", table_areas=["19,516,268,488"])
            heating_table = camelot.read_pdf(
                filepath=self._bill_file_name, pages="2", flavor="stream", table_areas=["19,275,363,233"])
            bill_table = camelot.read_pdf(
                filepath=self._bill_file_name, pages="1", flavor="stream", table_areas=["19,663,575,574"])

            water_meter = Meter(previous_reading=float(water_table[0].df[1][1].replace(",", ".")),
                                current_reading=float(water_table[0].df[2][1].replace(",", ".")),
                                units="m3")
            water_svc = Service(
                name=bill_table[0].df[0][5], bill=float(bill_table[0].df[8][5].replace(",", ".")),
                meter=water_meter)

            flat_heating_meter = Meter(
                previous_reading=float(heating_table[0].df[2][2].replace(',', '.')),
                current_reading=float(heating_table[0].df[4][2].replace(',', '.')),
                units="kWh")
            flat_heating_svc = Service(
                name=bill_table[0].df[0][4], bill=float(bill_table[0].df[8][5].replace(",", ".")),
                meter=flat_heating_meter)

            building_heating_meter = Meter(
                difference=float(bill_table[0].df[2][3].replace(',', '.')) * 1000, units="kWh")
            building_heating_svc = Service(
                name=bill_table[0].df[0][3], bill=float(bill_table[0].df[8][3].replace(",", ".")),
                meter=building_heating_meter)

            return water_svc, flat_heating_svc, building_heating_svc

        except Exception as e:
            print(type(e), e.args)

    def _logout(self):
        pass
