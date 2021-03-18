from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class TwitterBot:
    def __init__(self, chrome_driver_path, user_name, password, loading_time=5):
        self.user = user_name
        self.password = password
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path)
        self.lag = loading_time
        self.log_in()

    def log_in(self):
        self.driver.get('https://twitter.com/login')
        time.sleep(self.lag)
        email_input = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
        email_input.send_keys(self.user)
        password_input = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(self.lag)

    def tweet(self, message):
        tweet = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]'
                                                  '/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div'
                                                  '/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div')
        for letter in message:
            tweet.send_keys(letter)
            time.sleep(0.1)
        tweet.send_keys(Keys.RETURN)
        send_tweet = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/'
            'div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]')
        send_tweet.click()
        time.sleep(self.lag)

    def close(self):
        self.driver.close()
