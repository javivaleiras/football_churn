# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import time
from functions import get_tables
import pandas as pd




# Nav options
options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

driver_path = 'C:\\Users\\javic\\Downloads\\chromedriver.exe'

driver = webdriver.Chrome(driver_path, chrome_options=options)

# Screen
driver.set_window_position(2000, 0)
driver.maximize_window()
time.sleep(1)

all_summary=[]
all_defensive=[]
all_offensive=[]
all_passing=[]


# browser
driver.get('https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/1929/Stages/3218/PlayerStatistics/Spain-LaLiga-2009-2010')


# accept cookies
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'button.css-1wc0q5e'.replace(' ', '.'))))\
    .click()

# players table
all_summary = get_tables(driver,'//div[@id="statistics-table-summary"]')

#defensive
WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '//li[@class="in-squad-detailed-view"]//a[@href="#stage-top-player-stats-defensive"]'.replace(' ', '.'))))\
    .click()


all_defensive = get_tables(driver,'//div[@id="statistics-table-defensive"]',
                           '//div[@id="statistics-paging-defensive"]//a[@id="next"]',
                           '//div[@id="statistics-paging-defensive"]//dl[@class="listbox right"]//b')

#offensive
WebDriverWait(driver, 10)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '//li[@class="in-squad-detailed-view"]//a[@href="#stage-top-player-stats-offensive"]'.replace(' ', '.'))))\
    .click()
    

all_offensive = get_tables(driver,'//div[@id="statistics-table-offensive"]',
                           '//div[@id="statistics-paging-offensive"]//a[@id="next"]',
                           '//div[@id="statistics-paging-offensive"]//dl[@class="listbox right"]//b')

#passing
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '//li[@class="in-squad-detailed-view"]//a[@href="#stage-top-player-stats-passing"]'.replace(' ', '.'))))\
    .click()
    
all_passing = get_tables(driver,'//div[@id="statistics-table-passing"]',
                           '//div[@id="statistics-paging-passing"]//a[@id="next"]',
                           '//div[@id="statistics-paging-passing"]//dl[@class="listbox right"]//b')






    
    