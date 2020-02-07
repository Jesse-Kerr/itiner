import numpy as np
import pandas as pd
from pprint import pprint
from src.directions_functions import get_response_time
from src.credentials import pg_database, pg_hostname, pg_username
from sqlalchemy import create_engine
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

# Save a pandas dataframe with the info
# start off by getting seconds at every hour. Time 0 = Monday, midnight.
travel_times = pd.DataFrame(
    data = {
        "origin_place_id"     : fixed_locations[0],
        'origin_name'         : "crux",
        'destination_place_id': fixed_locations[1],
        'destination_name'    : "tillery",
        'departure_time'      : np.arange(
            start= 0,     
            stop = 86400,
            step = 3600)
    })

travel_times['time_in_traffic'] = travel_times.apply(
    lambda x: get_response_time(
        x.origin, 
        x.destination, 
        x.times),
    axis=1) 

# Add some more interesting information to the dataframe
travel_times = travel_times.assign(
    departure_time_hour = travel_times['departure_time_seconds'] / 3600,
    time_in_traffic_minutes = travel_times['time_in_traffic_seconds'] / 60,
    standard_hour = [str(int(x - 12)) + "PM" if x > 12 else str(int(x)) + "AM" for x in travel_times['departure_time_hour']])

travel_times = travel_times.assign(
    departure_time_hour_standardized = ["12AM" if x == "0AM" else x for x in travel_times['standard_hour']])

travel_times = travel_times.drop(columns=['standard_hour'])

# Save to postgres
engine = create_engine(
    'postgresql://{}@{}:5432/{}'.format(
        pg_username,
        pg_hostname,
        pg_database
    ))

travel_times.to_sql(
    "travel_durations", 
    engine,
    if_exists= "append", 
    index = False
    )