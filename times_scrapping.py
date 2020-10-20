# Thanks to https://stackoverflow.com/questions/44431730/how-to-replace-accented-characters-in-python for the workaround on accents in university names

import pandas as pd
import numpy as np
import time
import bs4
from bs4 import BeautifulSoup
from selenium.common.exceptions import *
from selenium import webdriver

def get_uni_information(unilist, page=62):
    url = r"https://www.timeshighereducation.com/world-university-rankings/2021/world-ranking#!/page/0/length/25/sort_by/rank/sort_order/asc/cols/stats"
    ff_driver_path = r"C:\Users\jchen148.UR\Downloads\chromedriver_win32\chromedriver.exe"
    ff_driver = webdriver.Chrome(ff_driver_path)
    time.sleep(2)
    ff_driver.get(url)
    time.sleep(5)
    
    # click "Scores" button
    
    button = ff_driver.find_element_by_xpath('//*[@id="block-system-main"]/div/div[3]/div/div[1]/div[1]/div/div[1]/ul/li[2]/label/span')

    ff_driver.execute_script("arguments[0].click();", button)

    ff_driver.implicitly_wait(10) 
    
    # Crawl all the pages (max page is 40)
    if page <= 62: 
        for _ in range(int(page)):
            # Use BeautifulSoup to parse every page
            soup = BeautifulSoup(ff_driver.page_source, "html.parser")
            # Find the table which contains the information I want
            x = soup.find(name="table", attrs={"class": "table wur-hash-processed wur-cols-processed wur-pagelen-processed dataTable no-footer rank-only usr-processed scores"})
            # Use 'for' loop to catch every rows in the table, and append the rows into the list
            for tr in x.find(name="tbody"):
                try: 
                    tds = tr('td')
                    if tds[0].find(attrs={"class": "rank.sorting_1.sorting_2"}) is not None:
                        rank = tds[0].find(attrs={"class": "rank.sorting_1.sorting_2"}).string
                    else: 
                        rank = None
                    if tds[1].find(name="a") is not None:
                        uni = tds[1].find(name="a").string
                    else: 
                        uni = None
                    if tds[1].find(name = "span") is not None:
                        location = tds[1].find(name = "span").get_text()
                    else:
                        location = None
                    if tds[2] is not None:
                        overall_score = tds[2].get_text()
                    else: 
                        overall_score = None
                    if tds[3] is not None:
                        teaching_score = tds[3].get_text()
                    else: 
                        teaching_score = None
                    if tds[4] is not None:
                        research_score = tds[4].get_text()
                    else: 
                        research_score = None
                    if tds[5] is not None:
                        citation_score = tds[5].get_text()
                    else: 
                        citation_score = None
                    if tds[6] is not None:
                        industry_score = tds[6].get_text()
                    else: 
                        industry_score = None
                    if tds[7] is not None:
                        outlook_score = tds[7].get_text()
                    else: 
                        outlook_score = None
                except (RuntimeError, TypeError, NameError):
                    pass
                unilist.append([rank, uni, location, overall_score, teaching_score, research_score, citation_score, \
                               industry_score, outlook_score])
            # Click next page button
            element = ff_driver.find_element_by_xpath('//*[@id="datatable-1_next"]/a/span')
            ff_driver.execute_script("arguments[0].click();", element)
            time.sleep(5)
    else:
        print("Max page is 40.")
    
    ff_driver.quit()
    return unilist
    
    
import unicodedata

# formating accents in the university names

def strip_accents(text):

    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)
    
    
def get_the_ranking_dataframe(page=62):
    unilist = []
    unilist = get_uni_information(unilist, page)
    df = pd.DataFrame(unilist)
    df.columns = ["ranking", "uni", "location", "scores overall-score", "scores teaching-score", "scores research-score", \
                 "scores citations-score", "scores industry_income-score", "scores international_outlook-score"]
    df.reset_index(drop=True)
   
    # Dataframe preprocessing
    df["ranking"] = [int(x)+1 for x in range(len(df))]
    df["uni"] = df["uni"].map(str).apply(lambda x: strip_accents(x))
    df["location"] = df["location"].map(str)
    df["scores overall-score"] = df["scores overall-score"].apply(lambda x: x.encode('latin-1', 'replace')).map(str)
    
    
    return df
    
the_2021_data = get_the_ranking_dataframe(page = 62)


the_2021_data.to_csv("the_file_name.csv", index= False)


