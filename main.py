from wsgiref import headers
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import csv
start_url = 'https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars'
browser = webdriver.Chrome('chromedriver_win32/chromedriver')
browser.get(start_url)
time.sleep(10)
def scrape():
    starData = []
    #Creating header list and assigning the column names
    headers = ['name','distance','mass','radius']
    #Keeping planet data excluding header
    #Extraction and visiting in range 0-490
    for i in range(0,490):
        #Parsing html page 
        soup = BeautifulSoup(browser.page_source,'html.parser')
        #loop for finding the ul tags with the attributes class and exoplanet
        for tl_tag in soup.find_all('ul',attrs={'class','exoplanet'}):
            #finding all the li tags
            tl_tags = th_tag.find_all('li')
            #temp_list is an empty list for now
            temp_list = []
            #Enumerate provides index number to each item in the li_tag and checking if index number is 0
            for index,li_tag in enumerate(li_tags):
                if index==0:
                    #if each index number is 0 then the link is saved in tempList
                    temp_list.append(li_tag.find_all('a')[0].contents[0])
                    #if its not its appended to templist
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append('')
            starData.append(temp_list)
            #One page done and the next page is visited by the xpath and after this scrapper_2.csv
        browser.find_element('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    with open("scrapper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(starData)
scrape()