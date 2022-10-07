from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException 
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import random
from random import randint
import secrets
PATH = './chromedriver.exe'
chromeArgs = [
    '--disable-infobars',
    '--ignore-ssl-errors=yes',    
    '--ignore-certificate-errors'
]

loop_tags = [
    'thetugisthedrug',
    'fishinglife',
    'bassfishing',
    'kayakfishing',
    'oceankayakfishing',
    'sportfishing',
    'socal_kayakanglers',
    'socalkayakanglers',
    'socalfisherman',
    'fishingislife',
    'socalfishing',
    'fishinglife🎣',
    'fishing',
]

class Bot():
    links = []
    total_likes = 0
    total_errors = 0
    def __init__(self):
        self.login(secrets.username,secrets.password)
        self.like_by_hashtag()

    def login(self, username, password):
        options = webdriver.ChromeOptions()
        for arg in chromeArgs:
            options.add_argument(arg)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
        self.driver.get('https://instagram.com/')
        sleep(3)
        username_input = self.driver.find_element(By.XPATH, value='//*[@id="loginForm"]/div/div[1]/div/label/input')
        username_input.send_keys(username)
        pass_input = self.driver.find_element(By.XPATH, value='//*[@id="loginForm"]/div/div[2]/div/label/input')
        pass_input.send_keys(password)
        sleep(1)
        pass_input.send_keys(Keys.ENTER)
        sleep(5)
        self.driver.find_element(By.XPATH, value='//*[contains(text(),"Not Now")]').click()
        sleep(5)
        self.driver.find_element(By.XPATH, value='//*[contains(text(),"Not Now")]').click()

    def like_by_hashtag(self):
        tag_links = []
        for tag in loop_tags:
            self.driver.get('https://www.instagram.com/explore/tags/{}/'.format(tag))
            sleep(4)
            links_by_tag = self.driver.find_elements(By.TAG_NAME, value='a')

            def condition(link):
                return '.com/p/' in link.get_attribute('href')

            valid_links = list(filter(condition, links_by_tag))
            for i in range(len(valid_links)):
                link = valid_links[i].get_attribute('href')
                tag_links.append(link)
        self.links = list(set(tag_links)) # remove duplicate links from list
        del tag_links
        with open(r'./links.txt','w') as file:
            for link in self.links:
                file.write(str(link) + "/n") 
            
        try:
            sleep(5)
            for link in self.links:
                if self.total_likes >= 199 or self.total_errors >= 3:
                    break
                self.driver.get(link)
                rng_sleep()
                try:
                    def check_if_liked():
                        try:
                            self.driver.find_element(By.CSS_SELECTOR, value="[aria-label='Unlike']")
                            print("already liked")
                        except NoSuchElementException:
                            print("we can like this")
                            return True
                        return False
                    if check_if_liked():
                        try:
                            self.driver.find_element(By.XPATH, value="//span/div/button[*[local-name()='svg']/@aria-label='Like']").click()
                            #self.driver.find_element(By.XPATH, value="//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button").click()
                        except:
                            try:
                                self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                            except:
                                print("failed to like")
                        self.total_likes += 1
                        print(str(self.total_likes))
                except:
                    rng_sleep()
                    print('like operation failed')
                rng_sleep()
        except:
            print('error in like operation')
            self.total_errors += 1


def rng_sleep():
    random_time = (random.random() * 5) + 1
    sleep(random_time)
    print('sleeping for ' + str(random_time) + ' seconds')

def main():
    while True:
        my_bot = Bot()
        print('sleeping for an hour')
        sleep(60 * 60 + randint(10,100)) # sleep for a little over hour randomized

if __name__ == '__main__':
    main()