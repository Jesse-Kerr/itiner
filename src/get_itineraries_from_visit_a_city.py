import pandas as pd
import numpy as np
from selenium import webdriver

# Load list of 140 cities
top_cities = pd.read_csv("data/top_cities.csv")

# initialize the headless driver
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options = options)

# For each city, figure out what guides are available on visitacity.com
# Save them in a dict structure
city_links = dict()

for city in top_cities.cities: 
    
    print("Currently on", city)
    city_links[city] = list()

    # Go to the original page
    driver.get("https://www.visitacity.com/")

    # Get the search bar
    search_bar = driver.find_element_by_xpath('//*[@id="homeSearchField"]')
    
    # Send the city to the search bar -- make sure it's cleared first
    search_bar.clear()
    search_bar.send_keys(city)

    # Need to wait until it loads the thing
    # Should do so explicitly but easier for now
    driver.implicitly_wait(np.random.randint(low = 4, high = 8, size=1))

    # Get the dropdown that pops up
    dropdown = driver.find_element_by_xpath("//*[@class='dropdown-menu ng-isolate-scope']")

    # Figure out if any of the links are to guides
    for row in dropdown.find_elements_by_tag_name('li'):
        a = row.find_element_by_tag_name('a')
        p= a.find_element_by_tag_name('p')
        if 'Guides' in p.text:
            city_links[city].append(p.text)
            print(p.text, "appended to the dict entry for", city)

driver.close()