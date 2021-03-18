from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

PROMISED_DOWN = 54
PROMISED_UP = 20
CHROME_DRIVER_PATH = "C:/development/chromedriver_win32/chromedriver.exe"  # your chrome driver location
TWITTER_USER = " your phone number or user name to log in"
TWITTER_PASSWORD = "your password"
LOADING_TIME = 5

# Tasks
# go to test page (breitbandmessung)
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get("https://breitbandmessung.de/test")
time.sleep(LOADING_TIME)

# accept necessary cookies
accept_cookies = driver.find_element_by_xpath('//*[@id="allowNecessary"]')
accept_cookies.click()
time.sleep(LOADING_TIME)

# start test (button: browsermessung starten)
start_test = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/div/button')
start_test.click()
time.sleep(LOADING_TIME)

# accept data guidelines
accept_data_guidelines = driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div/div[3]/button[2]')
accept_data_guidelines.click()

# is test finished? - if not: wait 5s then: # get test results
while True:
    try:
        header = driver.find_element_by_css_selector('#root > div > div > div > div > div:nth-child(1) > h1')
        print(header.text)
        if header.text == "Die Browsermessung ist abgeschlossen.":
            tested_down_element = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/span')
            tested_up_element = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/div[1]/div/div/div[3]/div/div[1]/div[1]/div[2]/span')
            # format to float
            tested_down = float(tested_down_element.text.replace(',', '.'))
            tested_up = float(tested_up_element.text.replace(',', '.'))
            print("Download: ", tested_down)  # [Mbit/s]
            print("Upload: ", tested_up)  # [Mbit/s]
            break
    finally:
        time.sleep(LOADING_TIME)

# compare test results to promised speed
if tested_up >= PROMISED_UP and tested_down >= PROMISED_DOWN:
    internet_to_slow = False
else:
    internet_to_slow = True

if internet_to_slow:
    # log in to twitter
    driver.get('https://twitter.com/login')
    time.sleep(5)
    email_input = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
    email_input.send_keys(TWITTER_USER)
    password_input = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
    password_input.send_keys(TWITTER_PASSWORD)
    password_input.send_keys(Keys.RETURN)
    # complain
    time.sleep(LOADING_TIME)
    tweet = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/'
                                         'div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/'
                                         'div[1]/div/div/div/div[2]/div/div/div/div')

    message = f"Hey @Telekom_hilft, mein Internet ist schlecht: 59.17down/19.77up, obwohl ich für {PROMISED_DOWN}" \
              f"down/{PROMISED_UP} up zahle. (Magenta L Zuhause; Berlin Neukölln) #DeutscheTelekom #speedtest"
    for letter in message:
        tweet.send_keys(letter)
        time.sleep(0.1)

    tweet.send_keys(Keys.RETURN)
    send_tweet = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/'
                                              'div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]')
    send_tweet.click()
driver.close()


