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


driver.close()
