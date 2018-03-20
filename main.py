from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
import time
import os
import Tkinter as tk




def get_page(url):
    images=[]

    global driver
    driver = webdriver.Chrome()
    driver.get(url)
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        else:
            last_height = new_height


#This function uses BeautifulSoup to parse through the page source and find images.
    def get_img():

        sp = bs(driver.page_source, 'html.parser')
        for image in sp.find_all('img'):
            images.append(image)
    get_img()

    #Create folder which will contain downloaded images.
    def make_dir():
        if not os.path.exists('Downloaded images'):
            os.mkdir('Downloaded images')
        os.chdir('Downloaded images')
    make_dir()

    #Function which saves images.
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

class App(tk.Frame):
    def __init__(self,master=None,**kw):
        tk.Frame.__init__(self,master=master,**kw)
        self.txtURL = tk.StringVar()
        self.entryURL = tk.Entry(self,textvariable=self.txtURL)
        self.entryURL.grid(row=0,column=0)
        self.btnGet = tk.Button(self,text="SCRAPE",command=self.getImgs)
        self.btnGet.grid(row=0,column=2)

    def getImgs(self):
        get_page(self.txtURL.get())


root = tk.Tk()
root.title('Image Scraper 1.0')
tk.Label(root, text='Enter URL:').grid(row=0)
App(root).grid()
root.mainloop()


