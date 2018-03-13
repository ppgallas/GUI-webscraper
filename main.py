from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
import time
import os

users_url = str(raw_input('Enter URL:'))
images = []

#This function will get the address of website and scroll it automatically
def get_page():
    global driver
    driver = webdriver.Chrome('E:\piotrulu\Scripts\chromedriver.exe')
    driver.get(users_url)
    last_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        else:
            last_height = new_height
get_page()


def get_img():

    sp = bs(driver.page_source, 'html.parser')
    for image in sp.find_all('img'):
        images.append(image)
get_img()

def make_dir():
    if not os.path.exists('Downloaded images'):
        os.mkdir('Downloaded images')
    os.chdir('Downloaded images')
make_dir()

def save_img():

    x = 0

    for image in images:
        try:
            url = image['src']
            source = requests.get(url)
            with open('img-{}.jpg'.format(x), 'wb') as f:
                f.write(requests.get(url).content)
                x += 1
        except:
            print 'Error while saving image.'
save_img()




