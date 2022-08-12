import datetime
import logging
import azure.functions as func
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
import time
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd
import pyodbc
from urllib.parse import quote_plus
from sqlalchemy import create_engine, event, delete
from webdriver_manager.chrome import ChromeDriverManager
import os
import warnings


def main(mytimer: func.TimerRequest) -> None:
    #utc_timestamp = datetime.datetime.utcnow()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    #logging.info('Python timer trigger function ran at %s', utc_timestamp)
    chrome_path = "/usr/local/bin/chromedriver"

    logging.info(os.path.exists(chrome_path))
  
    service = Service(chrome_path)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(chrome_path, options=chrome_options)

    url = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    driver.get(url)
    driver.maximize_window()

    username = 'xxxxxxxxxx'
    password = 'xxxxxxxxxx'

    
    ### locate the username and password & send the login information
    driver.find_element(By.XPATH, '//*[@id="content"]/login-component/div/div/form/div/div[1]/input').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="content"]/login-component/div/div/form/div/div[2]/input').send_keys(password)
    
    driver.find_element(By.XPATH, '//*[@id="content"]/login-component/div/div/form/button').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="app-container"]/div[1]/div/div/nav/ul/app-nav-sub-list[2]/div/a/span[1]').click()
    driver.find_element(By.XPATH, '//*[@id="app-container"]/div[1]/div/div/nav/ul/app-nav-sub-list[2]/ng-transclude/app-nav-reporting/div/app-nav-item[4]/a/span').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="app-container"]/div[2]/div[2]/div/div[2]/list-control/div/div/div/div/div[3]/div[1]/input').send_keys('WSPerformanceSummary')
    time.sleep(5)
    cx_url = driver.find_element(By.XPATH, '//*[@id="app-container"]/div[2]/div[2]/div/div[2]/list-control/div/div/div/div/div[3]/table/tbody/tr[1]/td[3]/a').get_attribute('href')
    print(cx_url)


    server = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    database = 'xxxxxxxxxxxxxxxxxxxxxxx'
    username = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
    password = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
    driver= '{ODBC Driver 17 for SQL Server}'
    conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database +';UID=' + username + ';PWD=' + password)
    quoted = quote_plus('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database +';UID=' + username + ';PWD=' + password)
    engine=create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted), fast_executemany=True)

    logging.info('Successfully established connection to the database.....')

    today_date = date.today()

    pos_data = pd.read_csv(cx_url, skiprows=4)
    pos_data.drop(['Unnamed: 2', 'Unnamed: 3'], axis=1, inplace=True)
    pos_data.drop(pos_data.index[pos_data['Warteschleife'] == 'Gesamt:'], inplace=True)
    pos_data['Warteschleife'] = pos_data['Warteschleife'].fillna(method='ffill')
    pos_data.rename(columns={'Unnamed: 1':'PoS_Adviser'}, inplace=True)
    pos_data = pos_data[pos_data['PoS_Adviser'].notna()].reset_index(drop=True)

    if today_date.weekday() != 1:
        logging.info('appending the data to the existing table...')

        pos_data.to_sql('Phone_3CX_data',  con = engine, index=False, if_exists='append', chunksize=1000, method=None)
    else:
        logging.info('Its Tuesday so we replace the table with new data..')
        pos_data.to_sql('Phone_3CX_data',  con = engine, index=False, if_exists='replace', chunksize=1000, method=None)