from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd
driver = webdriver.Chrome()

driver.get("https://en.wikipedia.org/wiki/List_of_cities_by_international_visitors")

# Get the main table on the page (there's actually 140 cities on there,
# because they are ranked by different sites. )
city_table = driver.find_element_by_xpath('//*[@id="mw-content-text"]/div/table')
body = city_table.find_element_by_tag_name('tbody')

# Iterate through the table, extracting the city name out
city_list = list()
for row in body.find_elements_by_tag_name('tr'):
    td = row.find_elements_by_tag_name('td')
    city_name = td[2].text
    city_list.append(city_name)

# Save city_list
df = pd.DataFrame(
    data = {"cities" : city_list}
    )

df.to_csv("./top_cities.csv")