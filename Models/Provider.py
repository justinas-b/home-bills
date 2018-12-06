from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import os


class Provider:

    def __init__(self, username, password):

        self.provider = self.__class__.__name__
        self.month = None
        self.year = None
        self.bill = None
        self.services = None

        self._username = username
        self._password = password
        self._timeout = 15
        self._downloads_dir = "./Downloads"
        self._bill_file_name = None
        self._options = webdriver.ChromeOptions()
        self._options.add_argument('incognito')
        self._options.add_experimental_option(
            "prefs", {
                "download.default_directory": r"./Downloads",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
        )

        try:
            self._driver = webdriver.Chrome('./Drivers/chromedriver', chrome_options=self._options)
            self._retrieve_current_data()
        except Exception as e:
            print(e)
            # self.__exit__()
        finally:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._logout()
        self._cleanup_downloads_dir()
        self._driver.close()

    def _retrieve_current_data(self):
        self._login()
        self._bill_file_name = self._download_bill()
        self.bill = float(self._get_bill_total())
        self.services = self._get_services()
        self.year, self.month = self._get_bill_date()
        self._logout()
        return self.bill, self.services

    def _login(self):
        raise NotImplementedError

    def _download_bill(self):
        raise NotImplementedError

    def _get_bill_date(self):
        raise NotImplementedError

    def _get_bill_total(self):
        raise NotImplementedError

    def _calculate_bill_total(self):
        return sum([s.bill for s in self.services])

    def _get_services(self):
        raise NotImplementedError

    def _logout(self):
        raise NotImplementedError

    def _cleanup_downloads_dir(self):
        for file_name in os.listdir(self._downloads_dir):
            file_path = os.path.join(self._downloads_dir, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    def _get_download_progress(self):

        main_window_handle = self._driver.current_window_handle
        self._driver.execute_script('''window.open("about:blank");''')
        self._driver.switch_to.window(self._driver.window_handles[1])
        self._driver.get("chrome://downloads")
        WebDriverWait(self._driver, 15).until(expected_conditions.presence_of_element_located(
            (By.XPATH, '/html/body/downloads-manager')))
        progress = self._driver.execute_script('''
                            var tag = document.querySelector('downloads-manager').shadowRoot;
                            var intag = tag.querySelector('downloads-item').shadowRoot;
                            var progress_tag = intag.getElementById('progress');
                            if (progress_tag != null)
                            {
                                var progress = progress_tag.value
                            } else {
                                var progress = 100
                            }
                            return progress
                        ''')
        self._driver.close()
        self._driver.switch_to.window(main_window_handle)
        return progress
