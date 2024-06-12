"""
Scrape the NYT Best Sellers List for the Best Sellers in the relevant categories.
"""

import os

# Imports
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import requests
import time

search_url = 'https://www.nytimes.com/books/best-sellers/business-books/'
today = date.today()
outfile = 'nytBestSellers' + str(today) + '.csv'


# To be clear, render is a string. This just opens the page and returns the HTML as a string. Cool.
def rendering(url):
        driver = webdriver.Chrome()
        driver.get(url)     # load the web page from the URL

        time.sleep(3)                                            # wait for the web page to load
        render = driver.page_source                              # get the page source HTML
        driver.quit()                                            # quit ChromeDriver
        return render                                            # return the page source HTML

# Request the page
sellersHTMLText = rendering(search_url)
# Parse the HTML page as a beautiful soup object
sellers_soup = BeautifulSoup(sellersHTMLText, 'html.parser')
# Find the ordered list with the best sellers, use that text to search through
soup_container = sellers_soup.find('ol')
# Find, within that container, the list of elements with the data we want
soup_data = soup_container.find_all('li', 'css-1m0jikr')

with open(outfile, 'w') as f:
    # write column headers for each parameter into the file for later use
    f.write('Title,'
            'Author,'
            'Publisher\n')
    
    row = []
    # Loop through all of the best sellers.
    for i, dat in enumerate(soup_data):
        # print(str(i))
        # Loop through the item properties of the best seller.
        for j, d in enumerate(dat.find_all(itemprop=True)):
            if j < 1 or j > 3:
                continue
            # curStr = None
            if j == 2:
                row.append("\"" + d.text.title()[3:] + "\"")
            else:
                row.append("\"" + d.text.title() + "\"")
            
            """
            print("////////////START////////////")
            print(d.prettify())
            print("/////////////END/////////////")
            # Note that this is a tag type, not a raw string.
            curStr = d.find(itemprop="name")
            if (curStr != None):
                print(curStr.text)
                # print("I'm here!")
                row.append(curStr.text.title())
            """
            
            """
            for k in d.find_all('td', class_='ng-star-inserted'):
                tmp = k.text
                tmp = tmp.strip('  ') # remove any extra spaces
                        
                row.append(tmp)
            """
    # f.write('2020-12-31,') # write the date of the recorded data into the file
    print(row)
    
    for i in range(len(row)):
        if (i+1)%3==0:
            f.write(str(row[i]) + '\n')
        else:
            f.write(str(row[i]) + ',')
    """
    for i, value in row:
        if (i+1)%3==0:
            f.write(str(value) + '\n')
        else:
            f.write(str(value) + ',')
    """
    
    #f.write(','.join(row)) # write just the temperature and precipitation data into the file
    f.write('\n') # new line, in case you want to append more rows to the same file later on