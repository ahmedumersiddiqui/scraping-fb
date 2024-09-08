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
from selenium.webdriver.common.action_chains import ActionChains

class FacebookScraper:
    def __init__(self, file_path="posts.csv", depth=1, delay=5):
        self.file_path = file_path
        self.depth = depth
        self.delay = delay
        self.browser = None

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

    def collect_page(self, page_url):
        action = ActionChains(self.browser)

        columns = ['Page_Name', 'Poster_Name', 'Post_Content', 'Poster_Link', 'Post_Link']
        # page_name = page_names[page_url]
        page_url = page_url + "?sorting_setting=CHRONOLOGICAL"; #for new posts
        self.browser.get(page_url)
        time.sleep(self.delay)
        try:
            page_name = self.browser.find_element(By.XPATH, './/a[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 xggy1nq x1a2a7pz x1heor9g xt0b8zv x1hl2dhg x1xlr1w8"]')
            page_name = page_name.text
        except:
            page_name = ""
        time.sleep(self.delay)

        for _ in range(self.depth):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.delay)
        time.sleep(self.delay)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        feed = self.browser.find_element(By.XPATH,'.//div[@class="x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv"]')
        posts = feed.find_elements(By.XPATH,'.//div[@class="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"]')

        # print(posts,"These are the posts")

        with open(self.file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            for post in posts:
                try:
                    poster_name = post.find_element(By.XPATH,'.//a[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 xggy1nq x1a2a7pz xt0b8zv x1hl2dhg xzsf02u x1s688f"]')
                    poster_link =  poster_name.get_attribute('href')
                    poster_name = poster_name.text
                except:
                    poster_name = "Anonymous member"
                    poster_link = ""
                try:
                    time_element = post.find_element(By.XPATH, './/span[@class="x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j"]')
                    print("1")
                    action.move_to_element(time_element)
                    action.perform()
                    # time_element = post.execute_script("const mouseoverEvent = new Event('mouseover');arguments[0].dispatchEvent(mouseoverEvent)", time_element)
                    print("2")
                    time_element =time_element.get_attribute('aria-describedby')
                    print(time_element)

                except:
                    pass
                # try:
                    # time_element = post.find_element(By.XPATH, './/span[@class="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs"]')
                    # time_element =  post.find_element(By.XPATH, './/div[@class="xu06os2 x1ok221b"]')
                    # print("1")
                    # time_element = time_element.find_element(By.XPATH, './/span[@class="x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j"]')
                    # print("2")
                    # time_element = time_element.find_element(By.XPATH, '/span[2]')
                    # # time_element = time_element.find_element(By.XPATH, './/span[@class="x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j"]')
                    # # print("3")
                    # # time_element = time_element.find_element(By.XPATH, './/span[@aria-hidden="True"]')
                    # print("2")
                    # time_element = post.find_element(By.XPATH, '//span[@class="x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j"]')
                    # print("1")
                #     time_element = post.find_element(By.XPATH, '//a[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 xggy1nq x1a2a7pz xt0b8zv x1hl2dhg xi81zsa xo1l8bm"]')
                    
                #     print("4")
                #     post_href = time_element.get_attribute('href')
                #     print("5")
                # except:
                #     post_href = ""
                try:
                    try:
                        content = post.find_element(By.XPATH, './/div[@class="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a"]')
                        content = content.find_element(By.XPATH, './/div[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 xggy1nq x1a2a7pz xt0b8zv x1hl2dhg xzsf02u x1s688f"]').click() #see more button
                    except:
                        pass
                    finally:
                        content = post.find_element(By.XPATH, './/div[@class="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a"]')
                        content = content.find_elements(By.XPATH, './/div[@dir="auto"]')
                        post_content = ""
                        for content in content:
                            post_content += content.text
                        try:
                            more_content = post.find_elements(By.XPATH, './/div[@class="x11i5rnm xat24cr x1mh8g0r x1vvkbs xtlvy1s x126k92a"]')
                            for content in more_content:
                                try:
                                    content.find_element(By.XPATH, './/div[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 xggy1nq x1a2a7pz xt0b8zv x1hl2dhg xzsf02u x1s688f"]').click() #see more button
                                except:
                                    pass
                            more_content = post.find_elements(By.XPATH, './/div[@class="x11i5rnm xat24cr x1mh8g0r x1vvkbs xtlvy1s x126k92a"]')
                            for content in more_content:
                                more_text = content.find_elements(By.XPATH, './/div[@dir="auto"]')
                                for text in more_text:
                                    post_content += text.text
                        except:
                            pass
                except:
                    try:
                        bold_text = post.find_element(By.XPATH, './/span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1603h9y x1u7k74 xo1l8bm xzsf02u"]')
                        bold_text = bold_text.text
                        try:
                            normal_text = post.find_element(By.XPATH, './/span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x6prxxf xvq8zen xo1l8bm xzsf02u"]')
                            normal_text = normal_text.text
                            post_content = bold_text
                            post_content += normal_text
                            try:
                                post.find_element(By.XPATH, './/div[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 xggy1nq x1a2a7pz xt0b8zv x1hl2dhg xzsf02u x1s688f"]').click() #see more button
                                more_text = post.find_elements(By.XPATH, './/div[@class="x1e56ztr"]')
                                for text in more_text:
                                    post_content += text.text
                            except:
                                post_content += ""

                        except:
                            post_content = bold_text
                    except:
                        try:
                            image_content = post.find_element(By.XPATH, './/div[@class="x6s0dn4 x78zum5 xdt5ytf x1a7vs8u xl56j7k x10l6tqk x17qophe x13vifvy xh8yej3"]')
                            content = image_content.find_element(By.XPATH, './/div[@class="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs"]')
                            post_content = content.text
                        except:
                            try:
                                image_content = post.find_element(By.XPATH, './/div[@class="x6s0dn4 x78zum5 xdt5ytf x5yr21d xl56j7k x10l6tqk x17qophe x13vifvy xh8yej3"]')
                                content = image_content.find_element(By.XPATH, './/div[@class="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs"]')
                                post_content = content.text
                            except:
                                post_content = ""
                post_href = ""
                if post_content != "":
                    writer.writerow([page_name,poster_name,post_content,poster_link, post_href])

    def collect(self, page_urls, email, password):
        self.initialize_browser()
        self.login(email, password)

        for page_url in page_urls:
            self.collect_page(page_url)

        self.browser.quit()

if __name__ == "__main__":
    load_dotenv()
    scraper = FacebookScraper()
    pages = ['https://www.facebook.com/groups/3440987846125640']  # Add more page URLs as needed
    email = os.getenv('EMAIL')  # Your Facebook email
    password = os.getenv('PASSWORD')  # Your Facebook password
    scraper.collect(pages, email, password)

