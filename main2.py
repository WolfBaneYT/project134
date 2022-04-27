from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import csv
import pandas as pd
import matplotlib as plt 
START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("./chromedriver")
browser.get(START_URL)
time.sleep(10)
headers = ['name','distance','mass','radius']
starData = []
new_starData = []   
def scrape():
    for i in range(1,2):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))
            if current_page_num < i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://en.wikepidea.gov"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            starData.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i} page done 1")
def scrape_more_data(hyperlink):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        star_table = soup.find_all('table')
        table_rows = star_table[7].find_all('tr')
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_starData.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
scrape()
for index, data in enumerate(starData):
    scrape_more_data(data[5])
    print(f"{index+1} page done 2")
final_starData = []
for index, data in enumerate(starData):
    new_starData_element = new_starData[index]
    new_starData_element = [elem.replace("\n", "") for elem in new_starData_element]
    new_starData_element = new_starData_element[:7]
    final_starData.append(data + new_starData_element)
with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_starData)
final_dict = {}
for index,data in enumerate(starData):
    gravity = (float(starData[3])*5.972e+24)/(float(starData[7])*float(starData[7])*6371000*6371000)*6.674e-11
    features_list = []

    try:
        if starData<=100:
            features_list.append('star')
    except:
        pass
    try:
        if gravity>150 and gravity<300:
            features_list.append('gravity')
    except:
        pass
    final_dict[index] = features_list
    print(final_dict)