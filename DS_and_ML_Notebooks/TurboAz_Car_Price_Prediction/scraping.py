from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

class TurboScrape:
    def __init__(self, driver : webdriver.Chrome):
        self.driver = driver
        self.city = []
        self.brand = []
        self.model = []
        self.released_at = []
        self.ban = []
        self.color = []
        self.engine = []
        self.distance = []
        self.gearbox = []
        self.transmitter = []
        self.is_new = []
        self.price = []

    def quit(self):
        self.driver.quit()

    def BS_Scrape(self, content):
        sp = BeautifulSoup(content, "html.parser")
        price = sp.find(class_ = "product-sidebar__box").find(class_ = "product-price__i product-price__i--bold").text
        others = sp.find(class_ = "product-section product-section--wide")
        info = [i.text for i in others.find_all(class_ = "product-properties__i-value")]

        self.price.append(price)
        self.city.append(info[0])
        self.brand.append(info[1])
        self.model.append(info[2])
        self.released_at.append(info[3])
        self.ban.append(info[4])
        self.color.append(info[5])
        self.engine.append(info[6])
        self.distance.append(info[7])
        self.gearbox.append(info[8])
        self.transmitter.append(info[9])
        self.is_new.append(info[10])

    def set_url(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)
        if url == "https://turbo.az":
            self.driver.find_element(By.XPATH, './/button[@class="main-search__btn tz-btn tz-btn--primary"][text()="Elanları göstər"]').click()
            self.driver.implicitly_wait(5)
            
    def page_cars(self):
        for i in self.driver.find_elements(By.CLASS_NAME, 'products-i'):
            i.click()
            self.driver.implicitly_wait(5)
            window_after = self.driver.window_handles[1]
            self.driver.switch_to.window(window_after)

            self.BS_Scrape(self.driver.page_source)
            self.driver.close()

            window_after = self.driver.window_handles[0]
            self.driver.switch_to.window(window_after)

    def change_page(self, loop_count = 25):
        for i in range(loop_count):
            try:
                self.driver.implicitly_wait(10)
                self.driver.find_element(By.XPATH, './/span[@class="next"]').click()
                self.page_cars()
            except:
                break

t = TurboScrape(webdriver.Chrome("chromedriver_win32"))
url = "https://turbo.az"

# url = "https://turbo.az/autos?page=345&q%5Bbarter%5D=0&q%5Bcrashed%5D=1&q%5Bcurrency%5D=azn&q%5Bengine_volume_from%5D=&q%5Bengine_volume_to%5D=&q%5Bfor_spare_parts%5D=0&q%5Bloan%5D=0&q%5Bmake%5D%5B%5D=&q%5Bmileage_from%5D=&q%5Bmileage_to%5D=&q%5Bonly_shops%5D=&q%5Bpainted%5D=1&q%5Bpower_from%5D=&q%5Bpower_to%5D=&q%5Bprice_from%5D=&q%5Bprice_to%5D=&q%5Bsort%5D=&q%5Bused%5D=&q%5Byear_from%5D=&q%5Byear_to%5D="

try:
    t.set_url(url)
    t.page_cars()
    t.change_page()
except:
    df_cars = pd.DataFrame(list(zip(t.price, t.brand, t.model, t.released_at, t.city, t.ban, 
                t.color, t.engine, t.distance, t.gearbox, t.transmitter, t.is_new)),
               columns =["price", "brand", "model", "released_at", "city", "ban", "color", "engine", "distance", "gearbox", 
                        "transmitter", "is_new"])

    df_cars.to_excel("turbo_az.xlsx")


print(len(t.city))
df_cars = pd.DataFrame(list(zip(t.price, t.brand, t.model, t.released_at, t.city, t.ban, 
                t.color, t.engine, t.distance, t.gearbox, t.transmitter, t.is_new)),
               columns =["price", "brand", "model", "released_at", "city", "ban", "color", "engine", "distance", "gearbox", 
                        "transmitter", "is_new"])

df_cars.to_excel("turbo_az.xlsx")