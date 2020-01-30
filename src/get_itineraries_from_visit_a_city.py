import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

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

class Scraping():
    
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

# For cities that have no Guide entries, append "None" so that we don't lose the information

for city in city_links.keys():
    if city_links[city] == []:
        city_links[city].append("No Guides Exist For This City")


# When a keyword I searched for has more than one city that matches,
# i.e., Porto matches Porto and Porto Venere, I retrieved both of them. Now I want to 
# separate them into their own list elements

dupes_removed_city_links = dict()
for city in city_links.keys():
    if (len(city_links[city]) > 1):
        for dupe_record in city_links[city]:
            # Get the actual city name, the part that appears before the comma
            actual_city = dupe_record.split(",", 1)[0]
            dupes_removed_city_links[actual_city] = dupe_record
    else:
        dupes_removed_city_links[city] = city_links[city]

# Here, I just take the max digit, knowing that the website has guides that are shorter
# Replace all spaces with -
just_days = dict()
for city in city_links.keys():
    fixed_city = city.replace(" ", "-")
    just_digits = [int(i) for i in city_links[city][0].split() if i.isdigit()]
    if len(just_digits) > 0:   
        max_digit = max(just_digits)     
        just_days[fixed_city] = max_digit
    else:
        just_days[fixed_city] = "None"
    
# Save the dict
df = pd.Series(just_days).to_frame()
df.to_csv("data/visit_a_city_guides_by_city.csv")

# Now go through the dict and get the information from the website
website = "https://www.visitacity.com/en"

for city in just_days.keys():
    day = just_days[city]
    if (day != "None"):
        this_website = "/".join([website, city, "itinerary-by-day", str(day)])
        print(this_website)

driver.get("https://www.visitacity.com/en/Colombo/itinerary-by-day/4")
itineraries = driver.find_elements_by_xpath("//div[contains(@title, 'Click to see Itinerary')]")
itineraries[1].text
itineraries[0].click()
# The link to the URL with the itineraries is like this:
"https://www.visitacity.com/en/"
"colombo/"
"itineraries/"
"colombo-four-day-easy-going-itinerary-day-1"
"#tab=tripOverview"
# So we just need to get the names of the itineraries they have, combine with the city
# name, and can start to scrape.
# Then, if we just add #tab=tripOverview to the end we get the entire thing in one

driver.get("https://www.visitacity.com/en/colombo/itineraries/colombo-four-day-easy-going-itinerary-day-1#tab=tripOverview")

itins_ul = driver.find_element_by_xpath("//ul[contains(@id, 'itineraryDrawersList')]")
itins_li = itins_ul.find_elements_by_xpath("//li[contains(@id, 'divDrawerActionIcon')]")

builder = ActionChains(driver)
builder.move_to_element(itins_li[0]).perform()

for itin in itins_li:
    print(itin.text)