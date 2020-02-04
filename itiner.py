
import numpy as np
import pandas as pd
from pprint import pprint
from src.directions_functions import get_response_time
# Try with 10 Austin locations
crux            = "ChIJA7CVXZW0RIYR7HqbXj7pcmw"
tillery         = "ChIJfzQBjy20RIYRMMohcj4xWvw"
barton          = "ChIJXVdJjDq1RIYRuahMgBpqoeQ"
sculpture_falls = "ChIJ656QhmBKW4YRXNS33chcFhs"
jester_king     = "ChIJkexlLlRGW4YRCXbXqNo7G_8"
spider_house    = "ChIJC7LFfX-1RIYRChAPNFanTEE"
alamo_mueller   = "ChIJ595f4vi1RIYRiOMsgjtJDlk"
genuine_joe     = "ChIJMX0PA7HLRIYRzLknsCCBHf8"
wonder_bar      = "ChIJl9essuLNRIYRBPEV9sPVDtU"
super_burrito   = "ChIJNYVN_xG1RIYRKHd-AoGPxds"

locations = [
    crux, tillery, barton, sculpture_falls, jester_king
    #spider_house, alamo_mueller, genuine_joe, wonder_bar, super_burrito
]

# Add place_id to all locations

fixed_locations = [] 
for loc in locations:
    fixed_locations.append('place_id:' + loc)

# Save a pandas dataframe with the info
# start off by getting seconds at every hour. Time 0 = Monday, midnight.
travel_times = pd.DataFrame(
    data = {
        'origin'      : fixed_locations[0],
        'origin_name' : "crux",
        'destination' : fixed_locations[1],
        'dest_name'   : "tillery",
        'times'       : np.arange(
            start= 0,     
            stop = 86400,
            step = 3600)
    })

travel_times['travel_time'] = travel_times.apply(
    lambda x: get_response_time(
        x.origin, 
        x.destination, 
        x.times),
    axis=1) 

travel_times.to_csv('./data/travel_times.csv')