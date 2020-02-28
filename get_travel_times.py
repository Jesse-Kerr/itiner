import numpy as np
import pandas as pd
from pprint import pprint
from src.google_api import GoogleAPI
# Read in the placeIDs we are interested in

googleAPI = GoogleAPI()

cursor = googleAPI.create_psycopg_cursor()
cursor.execute("""SELECT place_id FROM place_ids""")
places = cursor.fetchall()
places = [place[0] for place in places]

hours_to_get = np.arange(0, 12)

travel_durations = googleAPI.get_duration_using_distance_matrix(
    origins = places[0:2], 
    destinations = places[0:2], 
    hours = hours_to_get
)

travel_durations = pd.DataFrame(travel_durations)

googleAPI.save_table_to_postgres(travel_durations, "travel_durations")
# Add some more interesting information to the dataframe
# travel_times = travel_times.assign(
#     time_in_traffic_minutes = travel_times['time_in_traffic_seconds'] / 60,
#     standard_hour = [str(int(x - 12)) + "PM" if x > 12 else str(int(x)) + "AM" for x in travel_times['departure_time_hour']])

# travel_times = travel_times.assign(
#     departure_time_hour_standardized = ["12AM" if x == "0AM" else x for x in travel_times['standard_hour']])

# travel_times = travel_times.drop(columns=['standard_hour'])

