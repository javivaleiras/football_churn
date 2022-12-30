# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import config
import shutil
import time 
import pandas as pd
import pathlib 
import math
import os
import glob
import datetime
import re

year_today = datetime.date.today().year
wait_time_drivers = config.wait_time_drivers


def get_passing_df(driver):
        all_passing = []
        
        # get to passing page
        webdrivermanage(driver, '//li[@class="in-squad-detailed-view"]//a[@href="#stage-top-player-stats-passing"]',True)

        # all players page
        webdrivermanage(driver, '(//*[@id="apps"]/dd[2]/a)[4]',True)
                
        all_passing = get_tables(driver,'//div[@id="statistics-table-passing"]',
                                    '//div[@id="statistics-paging-passing"]//a[@id="next"]',
                                    '//div[@id="statistics-paging-passing"]//dl[@class="listbox right"]//b')
        
        #get last player
        table = get_table_last_player(driver, '//div[@id="statistics-table-passing"]')
        all_passing.append(table)
        
        passing_player = create_df_passing(all_passing)
        
        return passing_player


def get_offensive_df(driver):
        all_offensive = []
        
       #get to offensive page
        webdrivermanage(driver, '//li[@class="in-squad-detailed-view"]//a[@href="#stage-top-player-stats-offensive"]',True)

       
       # all players page
        webdrivermanage(driver, '(//*[@id="apps"]/dd[2]/a)[3]',True)
       
        all_offensive = get_tables(driver,'//div[@id="statistics-table-offensive"]',
                                   '//div[@id="statistics-paging-offensive"]//a[@id="next"]',
                                   '//div[@id="statistics-paging-offensive"]//dl[@class="listbox right"]//b')
       
       #get last player
        table = get_table_last_player(driver, '//div[@id="statistics-table-offensive"]')
        all_offensive.append(table)
       
       # trasnform table into dataframe
        offensive_player = create_df_offensive(all_offensive)
       
        return offensive_player

def get_defensive_df(driver):
        all_defensive = []
        
        #get to defensive page
        webdrivermanage(driver, '//li[@class="in-squad-detailed-view"]//a[@href="#stage-top-player-stats-defensive"]',True)
        
        # all players page
        webdrivermanage(driver, '(//*[@id="apps"]/dd[2]/a)[2]',True)
        
    
        all_defensive = get_tables(driver,'//div[@id="statistics-table-defensive"]',
                                    '//div[@id="statistics-paging-defensive"]//a[@id="next"]',
                                    '//div[@id="statistics-paging-defensive"]//dl[@class="listbox right"]//b')
        
        #get last player
        table = get_table_last_player(driver, '//div[@id="statistics-table-defensive"]')
        all_defensive.append(table)
        
        # trasnform table into dataframe
        defensive_player = create_df_defensive(all_defensive)
        
        return defensive_player
        
        
        

def get_summary_df(driver,year_of_current_season):
        all_summary = []
        #get to players statistics page
        webdrivermanage(driver, '//*[@id="sub-navigation"]/ul/li[4]/a',True)
        
        # all players page
        webdrivermanage(driver, '//*[@id="apps"]/dd[2]/a',True)
                
        # players table
        all_summary = get_tables(driver,'//div[@id="statistics-table-summary"]','//div[@id="statistics-paging-summary"]//a[@id="next"]')
        webdrivermanage(driver, '//div[@id="statistics-table-summary"]')

        #get last player
        table = get_table_last_player(driver, '//div[@id="statistics-table-summary"]')
        all_summary.append(table)
        
        # trasnform table into dataframe
        summary_player = create_df_summary(all_summary,year_of_current_season)
        
        return summary_player
    

def get_league_df(driver):
        webdrivermanage(driver,'//div[@class="ml12-lg-3 ml12-m-3 ml12-s-4 ml12-xs-5 semi-attached-table"]')
        league_df = get_league(driver,'//div[@class="ml12-lg-3 ml12-m-3 ml12-s-4 ml12-xs-5 semi-attached-table"]')
        
        return league_df
    
        
def get_league(driver,xpath_table):
    time.sleep(config.sleep_time)
    league_class = pd.DataFrame(columns=['position', 'club'])
    count = 0
    table_columns = driver.find_element_by_xpath(xpath_table)
    table_league = table_columns.text
    table_league = table_league.split('\n')
   
    for x in table_league:
        if count < 2:
            count+= 1
        else:
          club = re.split("[^a-zA-Z]*", x)
          del club[len(club) - 8:]
          club = ' '.join(club)
          club = club.strip()
          club = club.replace(" ", "")
          league_p = {'position': count - 1, 'club': club}
          league_class = league_class.append(league_p, ignore_index=True)
          count += 1
          
    return league_class   
          
          
          
def get_tables(driver,xpath_table,to_click='//a[@id="next"]',listbox='//dl[@class="listbox right"]//b'):
    all_table = []
    next_page = True
    while next_page:
       
        time.sleep(config.sleep_time)
        WebDriverWait(driver, config.wait_time_drivers)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                                xpath_table)))
        
        
        table_columns = driver.find_element_by_xpath(xpath_table)
        table = table_columns.text
        all_table.append(table)
        
        try:
            WebDriverWait(driver, config.wait_time_drivers)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                       to_click.replace(' ', '.'))))\
                    .click()
        except:
          
            WebDriverWait(driver, config.wait_time_drivers)\
                        .until(EC.element_to_be_clickable((By.XPATH,
                                                           to_click.replace(' ', '.'))))\
                        .click()
        try:  
            is_next = driver.find_element_by_xpath(listbox).text
            is_next = is_next.split('|')[0]
            page1 = is_next.split('/')[0].split(' ')[1]
            page2 = is_next.split('/')[1]
            if(int(page1) == int(page2)):
                next_page = False
        except:
            print("Warning - error reading page number")

    return all_table


def create_df_summary(all_summary,year_of_current_season):
       summary_player = pd.DataFrame(columns=['name', 'club','age','position', 'apps', 'mins',
                                     'goals', 'assists', 'yel', 'red', 'shots', 'ps%', 'aerials_won', 'motm', 'rating'])
       for x in all_summary:
             try:
                  players = x.split('\n')
                  players_num = int(len(players))
                  players_num = math.floor((players_num / 4))
                  name_index = 3
                  for i in range(0, players_num):
                      name = players[name_index].strip()
                      club = players[name_index + 1].split(',')[0].strip()
                      
                      # In the web appears the acutal age instead of the one that the player had during that season
                      age_now = players[name_index + 1].split(',')[1].strip()
                      years_to_substract = int(year_today) - int(year_of_current_season)
                      age_season = int(age_now) - int(years_to_substract)
                      
                      position = players[name_index + 1].split(',')[-1].strip()
                      stats = players[name_index + 2].split(' ')
                      apps = stats[0].strip()
                      mins = stats[1].strip()
                      goals = stats[2].strip()
                      assists = stats[3].strip()
                      yel = stats[4].strip()
                      red = stats[5].strip()
                      spg = stats[6].strip()
                      ps = stats[7].strip()
                      aerials = stats[8].strip()
                      motm = stats[9].strip()
                      rating = stats[10].strip()

                      summary_p = {'name': name, 'club': club,'age':age_season ,'position': position, 'apps': apps, 'mins': mins, 'goals': goals,
                          'assists': assists, 'yel': yel, 'red': red, 'shots': spg, 'ps%': ps, 'aerials_won': aerials, 'motm': motm, 'rating': rating}
                      summary_player = summary_player.append(summary_p, ignore_index=True)

                      name_index += 4

             except Exception as e:
                  print(e)

       return summary_player
   
def create_df_defensive(all_defensive):
    defensive_player = pd.DataFrame(columns=['name','club','position','mins','tackles','interceptions','fouls','offsides_won','clearances','dribbled','blocks','own_goals'])
    for x in all_defensive:
        try:
            players = x.split('\n')
            players_num = int(len(players))
            players_num = math.floor((players_num / 4))
            name_index = 3
            for i in range(0,players_num):
                name = players[name_index].strip()
                club = players[name_index + 1].split(',')[0].strip()
                position = players[name_index + 1].split(',')[-1].strip()
                stats = players[name_index + 2].split(' ')
                mins = stats[1].strip()
                tackles = stats[2].strip()
                inter = stats[3].strip()
                fouls = stats[4].strip()
                offsides = stats[5].strip()
                clear = stats[6].strip()
                drb = stats[7].strip()
                blocks = stats[8].strip()
                owng = stats[9].strip()
                
                
                defensive_p = {'name':name,'club':club,'position':position,'mins':mins,'tackles':tackles,'interceptions':inter,'fouls':fouls,'offsides_won':offsides,'clearances':clear,'dribbled':drb,'blocks':blocks,'own_goals':owng}
                defensive_player = defensive_player.append(defensive_p,ignore_index=True)
                
                name_index += 4 
            
            
        except Exception as e:
            print(e)
    
    return defensive_player

def create_df_offensive(all_offensive):
    offensive_player = pd.DataFrame(columns=['name','club','position','mins','key_passes','dribblings','fouled','offsides','dispossed','bad_controls'])
    for x in all_offensive:
        try:
            players = x.split('\n')
            players_num = int(len(players))
            players_num = math.floor((players_num / 4))
            name_index = 3
            for i in range(0,players_num):
                name = players[name_index].strip()
                club = players[name_index + 1].split(',')[0].strip()
                position = players[name_index + 1].split(',')[-1].strip()
                stats = players[name_index + 2].split(' ')
                mins = stats[1].strip()
                keyp = stats[5].strip()
                drb = stats[6].strip()
                fouled = stats[7].strip()
                off = stats[8].strip()
                disp = stats[9].strip()
                unstch = stats[10].strip()
                
                
                offensive_p = {'name':name,'club':club,'position':position,'mins':mins,'key_passes':keyp,'dribblings':drb,'fouled':fouled,'offsides':off,'dispossed':disp,'bad_controls':unstch}
                offensive_player = offensive_player.append(offensive_p,ignore_index=True)
                
                name_index += 4 
            
            
        except Exception as e:
            print(e)
    
    return offensive_player


def create_df_passing(all_passing):
    passing_player = pd.DataFrame(columns=['name','club','position','mins','avg_passes','crosses','long_passes','through_passes'])
    for x in all_passing:
        try:
            players = x.split('\n')
            players_num = int(len(players))
            players_num = math.floor((players_num / 4))
            name_index = 3
            for i in range(0,players_num):
                name = players[name_index].strip()
                club = players[name_index + 1].split(',')[0].strip()
                position = players[name_index + 1].split(',')[-1].strip()
                stats = players[name_index + 2].split(' ')
                mins = stats[1].strip()
                avgp = stats[4].strip()
                crosses = stats[6].strip()
                longb = stats[7].strip()
                thrb = stats[8].strip()
              
                
                
                passing_p = {'name':name,'club':club,'position':position,'mins':mins,'avg_passes':avgp,'crosses':crosses,'long_passes':longb,'through_passes':thrb}
                passing_player = passing_player.append(passing_p,ignore_index=True)
                
                name_index += 4 
            
            
        except Exception as e:
            print(e)
    
    return passing_player


def webdrivermanage(driver,xpath,click=False):
    if click:
        WebDriverWait(driver, wait_time_drivers)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                              xpath.replace(' ', '.'))))\
            .click()
    else:
        WebDriverWait(driver, wait_time_drivers)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                        xpath)))
                    

def get_table_last_player(driver,xpath):
        table_columns = driver.find_element_by_xpath('//div[@id="statistics-table-summary"]')
        table = table_columns.text
        return table


def merge_all_dfs(summary,defensive,offensive,passing):
    a = pd.merge(summary,defensive,left_on=['name','club','position','mins'], right_on=['name','club','position','mins'], how='left')
    b = pd.merge(offensive,passing,left_on=['name','club','position','mins'], right_on=['name','club','position','mins'], how='left')
    final = pd.merge(a,b,left_on=['name','club','position','mins'], right_on=['name','club','position','mins'], how='left')
    final = final.drop_duplicates()
    return final


def merge_all_csv_and_delete(csv_route,csv_output_name):
    os.chdir(csv_route)
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    combined_csv.to_csv(csv_output_name, index=False, encoding='utf-8-sig')
    


