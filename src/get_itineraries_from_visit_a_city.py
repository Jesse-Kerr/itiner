import pandas as pd
import numpy as np
from selenium import webdriver
from pprint import pprint
import re
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

# For cities that have no Guide entries, append "None" so that we don't lose the information

for city in city_links.keys():
    if city_links[city] == []:
        city_links[city].append("No Guides Exist For This City")

# Save the dict
df = pd.DataFrame(data = city_links)
df.to_csv("data/visit_a_city_guides_by_city", index=False)

# A happy accident -- When a keyword I searched for has more than one city that matches,
# i.e., Porto matches Porto and Porto Venere, I retrieved both of them. Now I want to 
# separate them into their own list elements

for city in city_links.keys():
    if (len(city_links[city]) > 1):
        for dupe_record in city_links[city]:
            # Get the actual city name, the part that appears before the comma
            actual_city = re.search("^[^,]*", dupe_record).group(0)
            city_links[actual_city] = dupe_record
        # lastly, need to drop the previous crap one
        city_links.pop(city)
