import json
from selenium import webdriver
import time


class Download:
    def __init__(self, url, email, password):
        self.url = url
        self.email = email
        self.password = password

    def download_as_pdf(self):
        appState = {
            "recentDestinations": [
                {
                    "id": "Save as PDF",
                    "origin": "local",
                    "account": ""
                }
            ],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }

        profile = {
            'printing.print_preview_sticky_settings.appState': json.dumps(
                appState)}

        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=1400,1500")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("enable-automation")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_experimental_option('prefs', profile)
        chrome_options.add_argument('--kiosk-printing')
        driver = webdriver.Chrome(options=chrome_options)

        driver.get('http://www.evcharge.ie/login')
        driver.find_element_by_id('email').send_keys(self.email)
        driver.find_element_by_id('password').send_keys(self.password)
        driver.find_element_by_id('submit').click()
        driver.get('http://www.evcharge.ie/login')
        driver.get(self.url)
        time.sleep(4)
        driver.execute_script('window.print();')
        driver.quit()
