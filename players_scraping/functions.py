# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 23:46:07 2022

@author: javic
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import time

def get_tables(driver,xpath_table,to_click='//a[@id="next"]',listbox='//dl[@class="listbox right"]//b'):
    all_table = []
    next_page = True
    while next_page:
       
        try:
            WebDriverWait(driver, 10)\
              .until(EC.element_to_be_clickable((By.XPATH,
                                                  xpath_table)))  

            table_columns = driver.find_element_by_xpath(xpath_table)
            table = table_columns.text
            all_table.append(table)
  
            try:
                WebDriverWait(driver, 10)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                              to_click.replace(' ', '.'))))\
                        .click()
            except:
                WebDriverWait(driver, 10)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                              to_click.replace(' ', '.'))))\
                        .click()
            
            
            is_next = driver.find_element_by_xpath(listbox).text
            is_next = is_next.split('|')[0]
            page1 = is_next.split('/')[0].split(' ')[1]
            page2 = is_next.split('/')[1]
            if(int(page1) == int(page2)):
                next_page=False
        except NoSuchElementException:
            next_page = False

    return all_table


