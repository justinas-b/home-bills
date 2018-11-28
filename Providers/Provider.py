from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import datetime
import os


class Provider:

    def __init__(self, username, password):

        self.provider = self.__class__.__name__
        self.month = datetime.datetime.now().month
        self.bill = None
        self.meters = None

        self._username = username
        self._password = password
        self._downloads_dir = "./Downloads"
        self._options = webdriver.ChromeOptions()
        self._options.add_argument('incognito')
        # self._options.add_argument("--headless")
        # self._options.add_argument("download.default_directory=./Downloads")
        self._options.add_experimental_option(
            "prefs", {
                "download.default_directory": r"./Downloads",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
        )
        self._driver = webdriver.Chrome('./Drivers/chromedriver', chrome_options=self._options)

        return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._logout()
        self._driver.close()

    def retrieve_historic_data(self):
        raise NotImplementedError

    def retrieve_current_data(self):
        self._login()
        self.bill = self._get_bill()
        self.meters = self._get_meters_data()
        self._logout()
        return self.bill, self.meters

    def _login(self):
        raise NotImplementedError

    def _get_bill(self):
        raise NotImplementedError

    def _get_meters_data(self):
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


