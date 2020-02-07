import pandas as pd
import numpy as np
from selenium import webdriver
from pprint import pprint
import re
# Load list of 140 cities
top_cities = pd.read_csv("data/guides_by_city.csv")


# initialize the headless driver
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome()

# Navigate to the guide page




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

driver.close()
