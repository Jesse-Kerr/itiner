import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from pprint import pprint
import re
from selenium.webdriver.chrome.options import Options

# For each city, figure out what guides are available on visitacity.com
# Save them in a dict structure
city_links = dict()

class VisitACity():

    def __init__(self):
        '''
        Initializes an instance of the Selenium scraper with options inherited
        from an instance of the Options class.  
        '''
        # Initialize an instance of Options, with the below arguments added.
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")  # not sure why
        chrome_options.add_argument("--disable-gpu")  # not sure why
        # So that you don't have to see the chrome browser.
        chrome_options.add_argument("--headless")

        # Initialize the webdriver with the above options.
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        # The implicitly_wait parameter means when you search for an element,
        # Selenium will wait this long before failing and saying that it's not
        # there. This is good when you want it to wait while a website loads, but
        # bad when you put it in a Try, Except and you want it to fail- then it
        # takes 60 seconds to fail.
        self.driver.implicitly_wait(60)

    def get_all_guides_for_a_city(self, city: str):
        
        '''
        This method takes a city, inputs it into visit_a_city's search bar, and gets
        all the guides associated with it
        '''

        print("Currently on", city)

        # Go to the original page
        self.driver.get("https://www.visitacity.com/")

        # Get the search bar
        search_bar = self.driver.find_element_by_xpath('//*[@id="homeSearchField"]')

        # Send the city to the search bar -- make sure it's cleared first
        search_bar.clear()
        search_bar.send_keys(city)

        # Need to wait until it loads the thing
        # Should do so explicitly but easier for now
        self.driver.implicitly_wait(np.random.randint(low=4, high=8, size=1))

        # Get the dropdown that pops up
        dropdown = self.driver.find_element_by_xpath("//*[@class='dropdown-menu ng-isolate-scope']")

        # Figure out if any of the links are to guides
        this_city_guides = []
        for row in dropdown.find_elements_by_tag_name('li'):
            a = row.find_element_by_tag_name('a')
            p = a.find_element_by_tag_name('p')
            if 'Guides' in p.text:
                this_city_guides.append(p.text)
                print(p.text, "appended to the dict entry for", city)
        
        return this_city_guides
    
    def split_dupes_into_own_entry(self, city_links: dict):

        '''
        When a keyword I searched for has more than one city that matches,
        i.e., Porto matches Porto and Porto Venere, I retrieved both of them. Now I want to
        separate them into their own list elements
        '''

        dupes_removed_city_links = dict()
        for city in city_links.keys():
            if (len(city_links[city]) > 1):
                for dupe_record in city_links[city]:
                    # Get the actual city name, the part that appears before the comma
                    actual_city = dupe_record.split(",", 1)[0]
                    dupes_removed_city_links[actual_city] = dupe_record
            else:
                dupes_removed_city_links[city] = city_links[city]
        
        return dupes_removed_city_links

    def clean_guide_dict(self, city_links: dict):

        '''
        Here, I just take the max digit, knowing that the website has guides that are shorter
        Replace all spaces with -
        '''

        just_days = dict()
        for city in city_links.keys():
            fixed_city = city.replace(" ", "-")
            just_digits = [int(i) for i in city_links[city][0].split() if i.isdigit()]
            if len(just_digits) > 0:
                max_digit = max(just_digits)
                just_days[fixed_city] = max_digit
            else:
                just_days[fixed_city] = "None"
        return just_days
