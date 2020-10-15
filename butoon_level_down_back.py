## line 17-27 was contributed by Aliaksandr

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import bs4
from bs4 import BeautifulSoup

ff_driver = webdriver.Chrome()
ff_driver.maximize_window()
ff_driver.get("https://www.topuniversities.com/university-rankings/world-university-rankings/2021")
btn_more = "#qs-rankings a.more"

links = []

for page in range(8):
    WebDriverWait(ff_driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, btn_more)))
    buttons = ff_driver.find_elements_by_css_selector(btn_more)

    for button in buttons:
        links.append(button.get_attribute("href"))

    elements = WebDriverWait(ff_driver, 30).until(EC.element_to_be_clickable((By.ID, "qs-rankings_next")))
    ff_driver.execute_script("arguments[0].click();", elements)

for idx, link in enumerate(links):
    ff_driver.get(link)
    index = []
    name = []
    cri = []
    values = []
    dic = {}
    
    try:
        WebDriverWait(ff_driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'criteria')))
        results = ff_driver.find_elements_by_class_name('criteria')
        header = str(str(link).split('/')[-1])
        
        name.append(header)
        index.append(int(idx) + 1)

        for quote in results:
            quoteArr = quote.text.split('\n')
            for line in quoteArr:
                if line is not None:
                    cri.append(str(line).split(':')[0])
                    values.append(str(line).split(':')[1])
                else:
                    cri.append('')
                    values.append('')
                dic['ranking'] = index
                dic['name'] = name
                dic['criteria'] = cri
                dic['values'] = values
        print(dic)
        
        with open(r'test_output_6.csv', 'a', newline='') as csvfile: ## have to create an empty csv file in the repo beforehand
            fieldnames = ['ranking', 'name','criteria', 'values']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'ranking':index,'name':name, 'criteria':[x for x in cri], 'values': [x for x in values]})
    
    except(TimeoutException):
        pass
        print("Exception has been thrown. " + header) 

ff_driver.close()


    

       
		
		
