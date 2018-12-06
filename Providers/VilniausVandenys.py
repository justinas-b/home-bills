from Models.Provider import Provider
from Models.Meter import Meter
from Models.Service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import camelot
import os
from datetime import datetime


class VilniausVandenys(Provider):

    def _login(self):

        try:
            # Open home page
            self._driver.get('https://savitarna.vv.lt/login.html')
            WebDriverWait(self._driver, self._timeout).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="gwt-placeholder"]/div/div/div[3]/div/button')))

            # Enter username
            username_field = self._driver.find_element_by_xpath('//*[@id="gwt-placeholder"]/div/div/div[2]/'
                                                                'div/div[1]/div/div/div[1]/input')
            username_field.click()
            username_field.send_keys(self._username)

            # Enter password
            password_field = self._driver.find_element_by_xpath('//*[@id="gwt-placeholder"]/div/div/div[2]/'
                                                                'div/div[2]/div/div/div[1]/input')
            password_field.click()
            password_field.send_keys(self._password)

            # Login
            password_field.send_keys(Keys.ENTER)
            WebDriverWait(self._driver, self._timeout).until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="gwt-placeholder"]/div/div/div[2]/div/div[2]/div[2]/div/div[4]/a/span')))
        except Exception as e:
            print(type(e), e.args)

    def _download_bill(self):
        self._driver.find_element_by_id("menu_payments").click()  # Open bills page
        WebDriverWait(self._driver, self._timeout).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'icon-file')))

        self._driver.find_element_by_class_name("icon-file").click()  # Download latest bill
        self._get_download_progress()  # Wait for bill to be downloaded

        # Get file name
        files = [os.path.join(self._downloads_dir, file)
                 for file
                 in os.listdir(self._downloads_dir)
                 if file.endswith(".pdf")]
        return files.pop()

    def _get_bill_date(self):
        download_icon = self._driver.find_element_by_class_name("icon-file")
        tr = download_icon.find_element_by_xpath("..//..")
        str_date = tr.find_element_by_tag_name("td").text
        date = datetime.strptime(str_date, "%Y-%m-%d")
        return date.year, date.month

    def _get_bill_total(self):
        download_icon = self._driver.find_element_by_class_name("icon-file")
        tr = download_icon.find_element_by_xpath("..//..")
        total = tr.find_element_by_xpath("td[5]").text
        return float(total)

    def _get_services(self):
        bill_table = camelot.read_pdf(filepath=self._bill_file_name, pages="1", flavor="stream",
                                      table_areas=["80,680,555,635"])

        cold_water_meter = Meter(current_reading=float(bill_table[0].df[2][1].replace(",", ".")),
                                 previous_reading=float(bill_table[0].df[1][1].replace(",", ".")),
                                 units="m3")
        cold_water_svc = Service(name="Geriamas vanduo ir nuotekų tvarkymas",
                                 bill=float(bill_table[0].df[5][1].replace(",", ".")),
                                 meter=cold_water_meter)

        selling_svc = Service(name="Mėnesinė pardavimo kaina",
                              bill=float(bill_table[0].df[5][2].replace(",", ".")))

        return cold_water_svc, selling_svc

    def _logout(self):
        pass
