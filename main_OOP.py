from internetspeed import SpeedTest
from twitterbot import TwitterBot

# -------constants------
PROMISED_DOWN = 54
PROMISED_UP = 20
CHROME_DRIVER_PATH = "C:/development/chromedriver_win32/chromedriver.exe"  # your chrome driver location
TWITTER_USER = " your phone number or user name to log in"
TWITTER_PASSWORD = "your password"
LOADING_TIME = 5

# ----SCRIPT--------
speed_test = SpeedTest(CHROME_DRIVER_PATH, LOADING_TIME)
speed_test.start_test()
speed_test.get_results()
speed_test.close()

if speed_test.tested_up >= PROMISED_UP and speed_test.tested_down >= PROMISED_DOWN:
    internet_to_slow = False
else:
    internet_to_slow = True

if internet_to_slow:
    twitter_bot = TwitterBot(chrome_driver_path=CHROME_DRIVER_PATH, user_name=TWITTER_USER, password=TWITTER_PASSWORD,
                             loading_time=LOADING_TIME)
    complaint = f"Hey @Telekom_hilft, mein Internet ist schlecht: {speed_test.tested_down}down/" \
                f"{speed_test.tested_up}up, obwohl ich für {PROMISED_DOWN}down/{PROMISED_UP} up zahle. " \
                f"(Magenta L Zuhause; Berlin Neukölln) #DeutscheTelekom #speedtest"
    twitter_bot.tweet(complaint)
    twitter_bot.close()
