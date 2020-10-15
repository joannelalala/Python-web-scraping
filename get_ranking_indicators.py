import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import requests

def getUniDetails(unilist, year = 2020, page = 40):
    url = r"https://www.topuniversities.com/university-rankings/world-university-rankings/{}".format(year)
    ff_driver_path = r"C:\Users\jchen148.UR\Desktop\selenium_project\chromedriver.exe"
    ff_driver = webdriver.Chrome(ff_driver_path)
    time.sleep(2)
    ff_driver.get(url)
    time.sleep(5)
    
    button = ff_driver.find_element_by_class_name("quicktabs-tab-rankings_tabs-1")
    ff_driver.execute_script("arguments[0].click();", button)
    ff_driver.implicitly_wait(10)    
    
    if page <= 40:    
        for _ in range(int(page)):
    
            soup = BeautifulSoup(ff_driver.page_source, "html.parser")
            x = soup.find(attrs={"id" : "qs-rankings-indicators_wrapper"})
            for tr in x.find(name = 'tbody'):
                try:
                    tds = tr('td')
                    
                    if tds[0].find(name = 'span') is not None:
                        rank = tds[0].find(name = 'span').string
                    else:
                        rank = None
                    if tds[1].find(name = 'a') is not None:
                        unis = tds[1].find(name = 'a').string
                    else:
                        unis = None
                    if tds[2].find(name = 'div') is not None:
                        o_score = tds[2].find(name = 'div').string
                    else:
                        o_score = None
                    if tds[3].find(name = 'div') is not None:
                        cit_fac = tds[3].find(name = 'div').string
                    else:
                        cit_fac = None
                    if tds[4].find(name = 'div') is not None:
                        intl_students = tds[4].find(name = 'div').string
                    else:
                        intl_students = None  
                    if tds[5].find(name = 'div') is not None:
                        intl_faculty = tds[5].find(name = 'div').string
                    else:
                        intl_faculty = None
                    if tds[6].find(name = 'div') is not None:
                        fac_student = tds[6].find(name = 'div').string
                    else:
                        fac_student = None
                    if tds[7].find(name = 'div') is not None:
                        employer_rep = tds[7].find(name = 'div').string
                    else:
                        employer_rep = None
                    if tds[8].find(name = 'div') is not None:
                        ac_reputation = tds[8].find(name = 'div').string
                    else:
                        ac_reputation = None                      
                        
                except(RuntimeError, TypeError, NameError):
                    pass
                print([rank, unis, o_score, cit_fac, intl_students, intl_faculty, fac_student, employer_rep, ac_reputation])    
                unilist.append([rank, unis, o_score, cit_fac, intl_students, intl_faculty, fac_student, employer_rep, ac_reputation])                           
                
            element = ff_driver.find_element_by_xpath('//*[@id="qs-rankings-indicators_next"]')
            ff_driver.execute_script("arguments[0].click();", element)
            time.sleep(5)
                
    else:
        print("Max Page is 40. ")
        
    ff_driver.quit()
    return unilist

def get_uni_details_dataframe(year=2020, page=40):
    unilist = []
    unilist = getUniDetails(unilist, year, page)
    df = pd.DataFrame(unilist)
    df.columns = ["ranking", "uni", "overall_score", "citations_faculty", "international_students", "international_faculty", "faculty_student", "employer_reputation", \
    "academic_reputation"]
    df.reset_index(drop=True)
    
    # Dataframe preprocessing
    df["ranking"] = [int(x)+1 for x in range(len(df))]
    df["uni"] = df["uni"].map(str)
#    df["location"] = df["location"].map(str)
    
    return df


qs_2020_data = get_uni_details_dataframe(year=2020, page = 8)
qs_2020_data.to_csv("the_file_name.csv", index= False)
