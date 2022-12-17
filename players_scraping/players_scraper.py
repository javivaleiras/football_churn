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
from functions import get_tables,create_df_summary,create_df_defensive,create_df_offensive,create_df_passing,merge_all_dfs,merge_all_csvs_and_delete
from selenium.webdriver.support.select import Select
import time
import math
import pandas as pd
import config
import os



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
seasons = config.seasons
first_page = True
initial_pages = config.initial_pages

wait_time_drivers = config.wait_time_drivers

for initial_page in initial_pages:
    # browser
    driver.get(initial_page)


    # accept cookies
    if first_page:
        WebDriverWait(driver, wait_time_drivers)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                              'button.css-1wc0q5e'.replace(' ', '.'))))\
            .click()
        first_page = False
        
    for current_season in seasons:
        if (seasons.index(current_season) + 1 != len(seasons)):
            next_season = seasons[seasons.index(current_season) + 1]
        
        # all players
        WebDriverWait(driver, wait_time_drivers)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                              '//*[@id="apps"]/dd[2]/a'.replace(' ', '.'))))\
            .click()
        
        
        
        # players table
        all_summary = get_tables(driver,'//div[@id="statistics-table-summary"]','//div[@id="statistics-paging-summary"]//a[@id="next"]')
        WebDriverWait(driver, wait_time_drivers)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                        '//div[@id="statistics-table-summary"]')))
                    
        
        
        #get last player
        table_columns = driver.find_element_by_xpath('//div[@id="statistics-table-summary"]')
        table = table_columns.text
        all_summary.append(table)
        
        #defensive
        WebDriverWait(driver, wait_time_drivers)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                              '//li[@class="in-squad-detailed-view"]//a[@href="#stage-top-player-stats-defensive"]'.replace(' ', '.'))))\
            .click()
        
        # all players
        
        WebDriverWait(driver, wait_time_drivers)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                              '(//*[@id="apps"]/dd[2]/a)[2]'.replace(' ', '.'))))\
                .click()
     
        
        
        all_defensive = get_tables(driver,'//div[@id="statistics-table-defensive"]',
                                    '//div[@id="statistics-paging-defensive"]//a[@id="next"]',
                                    '//div[@id="statistics-paging-defensive"]//dl[@class="listbox right"]//b')
        
        #get last player
        table_columns = driver.find_element_by_xpath('//div[@id="statistics-table-defensive"]')
        table = table_columns.text
        all_defensive.append(table)
        
        
        #offensive
        WebDriverWait(driver, wait_time_drivers)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                              '//li[@class="in-squad-detailed-view"]//a[@href="#stage-top-player-stats-offensive"]'.replace(' ', '.'))))\
            .click()
        
        # all players
        WebDriverWait(driver, wait_time_drivers)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                              '(//*[@id="apps"]/dd[2]/a)[3]'.replace(' ', '.'))))\
            .click()
        
        all_offensive = get_tables(driver,'//div[@id="statistics-table-offensive"]',
                                    '//div[@id="statistics-paging-offensive"]//a[@id="next"]',
                                    '//div[@id="statistics-paging-offensive"]//dl[@class="listbox right"]//b')
        
        #get last player
        table_columns = driver.find_element_by_xpath('//div[@id="statistics-table-offensive"]')
        table = table_columns.text
        all_offensive.append(table)
        
        #passing
        WebDriverWait(driver, wait_time_drivers)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                              '//li[@class="in-squad-detailed-view"]//a[@href="#stage-top-player-stats-passing"]'.replace(' ', '.'))))\
            .click()
            
        # all players
        WebDriverWait(driver, wait_time_drivers)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                              '(//*[@id="apps"]/dd[2]/a)[4]'.replace(' ', '.'))))\
            .click()
        
        
        all_passing = get_tables(driver,'//div[@id="statistics-table-passing"]',
                                    '//div[@id="statistics-paging-passing"]//a[@id="next"]',
                                    '//div[@id="statistics-paging-passing"]//dl[@class="listbox right"]//b')
        
        #get last player
        table_columns = driver.find_element_by_xpath('//div[@id="statistics-table-passing"]')
        table = table_columns.text
        all_passing.append(table)
        
        
        
        
        ## Player creation
        
        summary_player = create_df_summary(all_summary)
        defensive_player = create_df_defensive(all_defensive)
        offensive_player = create_df_offensive(all_offensive)
        passing_player = create_df_passing(all_passing)
                
        final = merge_all_dfs(summary_player, defensive_player, offensive_player, passing_player)
        
        # get league and season
        league = driver.find_element_by_xpath('//*[@id="tournaments"]//option[@selected="selected"]').text
        season = driver.find_element_by_xpath('//*[@id="seasons"]//option[@selected="selected"]').text
        season1 = season.split("/")[0]
        season2 = season.split("/")[1]
        
        
        # add league and season to dataframe
        final['league'] = league
        final['season'] = season
        
        # create folder and csv
        outname = league+season1+"-"+season2+".csv"
    
        outdir = './tmp'
        if not os.path.exists(outdir):
            os.mkdir(outdir)
    
        fullname = os.path.join(outdir, outname)   
        final.to_csv(fullname)
        
        
        # next league and season to scrap
        if (seasons.index(current_season) + 1 != len(seasons)):
            select_element = driver.find_element(By.XPATH, '//*[@id="seasons"]')
            select = Select(select_element)
            select.select_by_visible_text(next_season)
            WebDriverWait(driver, wait_time_drivers)\
                .until(EC.element_to_be_clickable((By.XPATH,
                                                  '//*[@id="sub-navigation"]/ul/li[4]/a'.replace(' ', '.'))))\
                .click()



merge_all_csvs_and_delete()