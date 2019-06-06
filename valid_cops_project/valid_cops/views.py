from django.shortcuts import render
from bs4 import BeautifulSoup
from PIL import Image
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .forms import ShoeForm

def home(request):
    return render(request,'valid_cops/home.html')

def base(request):
    hidden=True
    stockx_href=''
    stockx_price=''
    stadium_price=''
    stadiumgoods_href=''
    flightclub_href=''
    flightclub_price=''
    if request.method == 'POST':
        #goat
        form = ShoeForm(request.POST)

        #stockx
        stockx = 'https://stockx.com'
        #stockx_response = requests.get(stockx,timeout = 5)
        chrome_options = Options()
        chrome_options.headless = True
        driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=r"/Users/Harrison/Downloads/chromedriver")
        driver.get(stockx)
        test = wait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="home-search"]'))).send_keys(request.POST.get('shoe_name'))

        test = wait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="home-results"]/ul/li[1]/div[2]/div/div[2]'))).click()

        test = wait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[ @ id = "market-summary"]/div[1]/div/div/div[2]/ul')))
        stockx_href=driver.current_url
        page_response = requests.get(driver.current_url,timeout = 5)
        soup = BeautifulSoup(page_response.content, 'lxml')
        list =soup.find_all("div",attrs={"class":"inset"})
        for li in list:
            if li.contents[0].string == request.POST.get('shoe_size'):
                stockx_price=li.contents[1].string
                break
        hidden = False

        #stadium goods
        stadiumgoods_shoename=''
        for ch in request.POST.get('shoe_name'):
            if ch ==' ':
                stadiumgoods_shoename+='+'
            else:
                stadiumgoods_shoename+=ch
        stadiumgoods='https://www.stadiumgoods.com/search/go?w='+stadiumgoods_shoename
        driver.get(stadiumgoods)
        test = wait(driver, 3).until(
             EC.presence_of_element_located((By.XPATH, '//*[@id="mb-content"]/div/ul[1]/li[1]/div[2]/a/img'))).click()
        stadiumgoods_href=driver.current_url
        test = wait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '// *[ @ id = "product-options-wrapper"] / div[2] / div[1] / span'))).click()
        test = wait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="product-options-wrapper"]/div[2]/div[2]/label[10]/span'))).click()
        stadium_price = wait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="product-options-wrapper"]/div[2]/div[1]/span/span[2]'))).text


        #Flightclub

        flightclub='https://www.flightclub.com'
        driver.get(flightclub)
        flightclub_search=wait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="search"]'))).send_keys(request.POST.get('shoe_name')+Keys.ENTER)
        flightclub_search = wait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="instant-search-results-container"]/div/div[1]/div/a/div/div[2]/div[1]/div/div[2]/div/div/span')))
        flightclub_price=flightclub_search.get_attribute('innerHTML')
        #flightclub_search = wait(driver, 3).until(
            #EC.presence_of_element_located(
                #(By.XPATH, '// *[ @ id = "instant-search-results-container"] / div / div[1] / div / a / div / div[1] / img'))).click()
        flightclub_href=driver.current_url



    form = ShoeForm()
    context={'hidden':hidden,'form':form,'stockx_href':stockx_href, 'shoe_name':request.POST.get('shoe_name'),'shoe_size':request.POST.get('shoe_size'), 'stockx_shoe_price':stockx_price, 'stadium_price':stadium_price, 'stadiumgoods_href':stadiumgoods_href,'flightclub_href':flightclub_href, 'flightclub_price':flightclub_price}
    return render(request, 'valid_cops/base.html', context)


