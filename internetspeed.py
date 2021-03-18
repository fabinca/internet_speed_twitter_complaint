from selenium import webdriver
import time


class SpeedTest:
    def __init__(self, chrome_driver_path, loading_time=5):
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path)
        self.lag = loading_time
        self.tested_up = None
        self.tested_down = None

    def start_test(self):
        self.driver.get("https://breitbandmessung.de/test")
        time.sleep(self.lag)
        accept_cookies = self.driver.find_element_by_xpath('//*[@id="allowNecessary"]')
        accept_cookies.click()
        time.sleep(self.lag)
        start_test = self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/div/button')
        start_test.click()
        time.sleep(self.lag)
        accept_data_guidelines = self.driver.find_element_by_xpath(
            '//*[@id="root"]/div/div[3]/div/div/div[3]/button[2]')
        accept_data_guidelines.click()

    def get_results(self):
        while True:
            try:
                header = self.driver.find_element_by_css_selector(
                    '#root > div > div > div > div > div:nth-child(1) > h1')
                print(header.text)
                if header.text == "Die Browsermessung ist abgeschlossen.":
                    tested_down_element = self.driver.find_element_by_xpath(
                        '//*[@id="root"]/div/div/div/div/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/span')
                    tested_up_element = self.driver.find_element_by_xpath(
                        '//*[@id="root"]/div/div/div/div/div[1]/div/div/div[3]/div/div[1]/div[1]/div[2]/span')
                    # format to float
                    self.tested_down = float(tested_down_element.text.replace(',', '.'))
                    self.tested_up = float(tested_up_element.text.replace(',', '.'))
                    print("Download: ", self.tested_down)
                    print("Upload: ", self.tested_up)
                    break
            finally:
                time.sleep(self.lag)

    def close(self):
        self.driver.close()
