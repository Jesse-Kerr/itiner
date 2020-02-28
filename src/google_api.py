import numpy as np
from src.credentials import pg_database, pg_hostname, pg_username, api_key
from sqlalchemy import create_engine
import psycopg2
import urllib
import json
from src.constants import directions_url, distance_matrix_url, sat0, mon0


class GoogleAPI():

    def __init__(self):
        '''

        '''
        self.sat0 = sat0
        self.mon0 = mon0
        self.api_key = api_key
        self.distance_matrix_url = distance_matrix_url

    def create_psycopg_cursor(self):
        con = psycopg2.connect(
            host = pg_hostname,
            database = pg_database, 
            user = pg_username
        )

        cursor = con.cursor()

        return(cursor)
    
    def create_sql_alchemy_engine(self):
        self.engine = create_engine(
            'postgresql://{}@{}:5432/{}'.format(
                pg_username,
                pg_hostname,
                pg_database
                ))

    def save_table_to_postgres(self, obj_to_save, table_to_save_to):

        self.create_sql_alchemy_engine()

        obj_to_save.to_sql(
            table_to_save_to, 
            self.engine,
            if_exists= "replace", 
            index = False
            )

    def get_duration_using_distance_matrix(self, origins, destinations, hours):

        '''
        For each origin-destination pair, travel duration is calculated
        at different times throughout the day for a Saturday and a Monday.
        
        hours are a list of hours to calculate travel time at (in military time).

        '''

        # Convert hours to seconds
        seconds_to_get = hours * 3600

        sat_seconds_to_get = seconds_to_get + self.sat0
        mon_seconds_t0_get = seconds_to_get + self.mon0

        all_seconds_to_get = np.concatenate([
            sat_seconds_to_get,
            mon_seconds_t0_get
        ])
        # add placeID to front of all origins and destinations, and turn to array
        origins = np.asarray(["place_id:" + origin for origin in origins])
        destinations = np.asarray(["place_id:" + destination for destination in destinations])
        
        # Initialize empty dict to save 
        travel_durations = list()

        # for each origin, we will get the time to all destinations at a specific departure
        # time. 
        for origin in origins:

            # Remove the origin from the destinations. 
            these_destinations = destinations[destinations != origin]

            # Turn destination into a str with |'s between each element
            these_destinations_str = "|".join(these_destinations)

            # For each time provided
            for time in all_seconds_to_get:

                # Use most pessimistic travel time to get 
                print("Getting travel time for ", origin, " and ", destinations, " at ", time)
                url = "".join([
                    self.distance_matrix_url,
                    "origins=",
                    origin,
                    "&destinations=", 
                    these_destinations_str,
                    "&key=",
                    self.api_key,
                    "&mode=driving",
                    "&departure_time=",
                    str(time),
                    "&traffic_model=pessimistic"
                    ])

                response = json.loads(urllib.request.urlopen(url).read())
                all_elements = response['rows'][0]['elements']
                all_dest_addresses = response['destination_addresses']
                all_durs_in_traf = [element['duration_in_traffic']['value'] for element in all_elements]

                for ind in range(len(all_durs_in_traf)):

                    # Save this in the dict
                    travel_durations.append(
                        {
                            'origin' : str(origin),
                            'origin_address' : response['origin_addresses'][0],
                            'destination' : str(these_destinations[ind]),
                            'destination_address' : all_dest_addresses[ind],
                            'duration_in_traffic' : all_durs_in_traf[ind],
                            'departure_time_seconds_from_sat0' : time - sat0
                            })
        
        return(travel_durations)

        