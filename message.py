from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os

class Message:
    def __init__(self, delay=3):
        self.delay = delay
        
    def initialize_browser(self):
        options = Options()
        options.headless = False  # Set to True for headless mode
        service = Service(executable_path=GeckoDriverManager().install())
        self.browser = webdriver.Firefox(service=service, options=options)

    def login(self, email, password):
        
        self.browser.get("https://www.facebook.com")
        self.browser.maximize_window()
        time.sleep(self.delay)
        try:
            # filling the form
            self.browser.find_element('name','email').send_keys(email)
            self.browser.find_element('name','pass').send_keys(password)
            # clicking on login button
            self.browser.find_element('name','login').click()
            print("Logged in successfully!")
        except TimeoutException:
            print("Login timed out. Unable to locate login form or input fields.")
        except Exception as e:
            print("Error occurred while logging in:", e)
    def send_message(self, profile_link, msg):
        self.browser.get(profile_link)
        time.sleep(self.delay)

        try:
            headline = self.browser.find_element(By.XPATH,'.//div[@class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf xeuugli x1r8uery x1iyjqo2 xs83m0k x1swvt13 x1pi30zi xqdwrps x16i7wwg x1y5dvz6"]')
            message_button = headline.find_element(By.XPATH, './/div[@class="x78zum5 x1a02dak x139jcc6 xcud41i x9otpla x1ke80iy"]')
            message_button = message_button.find_element(By.XPATH,'.//*[contains(@class, "xsgj6o6 xw3qccf x1xmf6yo x1w6jkce xusnbm3")][2]')
            message_button = message_button.find_element(By.XPATH, './/div[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3"]').click()
            time.sleep(self.delay)
            message_display = self.browser.find_element(By.XPATH, './/div[@class="x9f619 x1n2onr6 x1ja2u2z __fb-light-mode x78zum5 xdt5ytf x1iyjqo2 xs83m0k x193iq5w"]')
            time.sleep(self.delay)
            message_display1 = message_display.find_element(By.XPATH, './/div[@class="x78zum5 xdt5ytf x1iyjqo2 x193iq5w x2lwn1j x1n2onr6"]')
            message_display2 = message_display1.find_element(By.XPATH, './/div[@class="xuk3077 x57kliw x78zum5 x6prxxf xz9dl7a xsag5q8"]')
            message_display3 = message_display2.find_element(By.XPATH, './/div[@class="x1iyjqo2 xw2csxc x1n2onr6"]')
            message_display4 = message_display3.find_element(By.XPATH, './/div[@class="x16sw7j7 x107yiy2 xv8uw2v x1tfwpuw x2g32xy x9f619 xlai7qp x1iyjqo2 xeuugli"]')
            message_display5 = message_display4.find_element(By.XPATH, './/div[@class="xzsf02u x1a2a7pz x1n2onr6 x14wi4xw x1iyjqo2 x1gh3ibb xisnujt xeuugli x1odjw0f notranslate"]')
            for char in msg:
                message_display5.send_keys(char)
            send_button = self.browser.find_element(By.XPATH, './/div[@class="x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 xe8uvvx xdj266r xat24cr x2lwn1j xeuugli x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1c4vz4f x2lah0s xsgj6o6 xw3qccf x1y1aw1k x1sxyh0 xwib8y2 xurb0ha"]')
            send_button.click()
            time.sleep(self.delay)
            close_chathead = self.browser.find_element(By.XPATH, './/div[@aria-label="Close chat"]')
            
            close_chathead.click()
            time.sleep(self.delay)
        except:
            pass



    def send_messages(self, email, password, profile_links, message):
        self.initialize_browser()
        self.login(email, password)
        for link in profile_links:
            self.send_message(link, message)
        self.browser.quit()

if __name__ == "__main__":
    load_dotenv()
    email = os.getenv('EMAIL')  # Your Facebook email
    password = os.getenv('PASSWORD') #Your facebook password
    profile_links=['https://www.facebook.com/ahmedumersiddiqi', 'https://www.facebook.com/hamzahtariq11']
    scraper = Message()
    message = "Hello! This is an automated from Ottomaters."
    scraper.send_messages(email, password, profile_links, message)