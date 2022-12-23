# -*- coding: utf-8 -*-


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from functions import *
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

driver_path = config.driver_path

driver = webdriver.Chrome(driver_path, chrome_options=options)

# Screen
driver.set_window_position(2000, 0)
driver.maximize_window()
time.sleep(1)


# Variables
seasons = config.seasons
first_page = True
initial_pages = config.initial_pages
wait_time_drivers = config.wait_time_drivers

# through all inital pages
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
    
    #through all seasons
    for current_season in seasons:
        
        #get year of current season to get the age
        year_of_current_season = current_season.split('/')[1]
        
        #get league classification
        league_df = get_league_df(driver)
        
        
        # get summary stats
        summary_player = get_summary_df(driver,year_of_current_season)
        
        # get defensive stats
        defensive_player = get_defensive_df(driver)
        
        # get offensive stats
        offensive_player = get_offensive_df(driver)
        
        # get passing stats
        pasing_player = get_passing_df(driver)        
        
        # merge all dataframes in one        
        final = merge_all_dfs(summary_player, defensive_player, offensive_player, passing_player)
        
        # get league and season scrapped
        league = driver.find_element_by_xpath('//*[@id="tournaments"]//option[@selected="selected"]').text
        season = driver.find_element_by_xpath('//*[@id="seasons"]//option[@selected="selected"]').text
        season1 = season.split("/")[0]
        season2 = season.split("/")[1]
        
        
        # add league and season to dataframe
        final['league'] = league
        final['season'] = season
        
        # add league and season to dataframe
        league_df['league'] = league
        league_df['season'] = season
        
        # create folder and csv of stats
        outname_stats = league+season1+"-"+season2+".csv"
        
        
        outdir = './data_stats'
        if not os.path.exists(outdir):
            os.mkdir(outdir)
    
        fullname = os.path.join(outdir, outname_stats)   
        final.to_csv(fullname)
        
        
        
        # create folder and csv of league classification
        outname_class = "classification_"+league+season1+"-"+season2+".csv"
        outdir = './data_classification'
        if not os.path.exists(outdir):
            os.mkdir(outdir)
    
        fullname = os.path.join(outdir, outname_class)   
        league_df.to_csv(fullname)
        
        
        
        # get next season if is not the last one
        if (seasons.index(current_season) + 1 != len(seasons)):
            next_season = seasons[seasons.index(current_season) + 1]
        # next league and season to scrap
        if (seasons.index(current_season) + 1 != len(seasons)):
            select_element = driver.find_element(By.XPATH, '//*[@id="seasons"]')
            select = Select(select_element)
            select.select_by_visible_text(next_season)
       


# merge all dataframes generated into one single dataframe
merge_all_csv_and_delete("./data_stats","players_stats.csv")
merge_all_csv_and_delete("./data_classification","leagues_classification.csv")
