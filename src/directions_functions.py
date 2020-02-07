import urllib
import json
from src.constants import service_url
from src.constants import time0

from src.credentials import api_key


def get_response_time(origin, destination, time):

    '''
    You can specify the time as an integer in seconds 
    since midnight, January 1, 1970 UTC
    '''

    # Add time0

    time_to_get = str(time + time0)
    print("Getting travel time between ", origin, " and ", destination, " at ", time)
    url = "".join([
        service_url,
        "origin=place_id:",
        origin,
        "&destination=place_id:", 
        destination,
        "&key=",
        api_key,
        "&mode=driving",
        "&departure_time=",
        time_to_get
        ])

    response = json.loads(urllib.request.urlopen(url).read())
    traffic_time = response['routes'][0]['legs'][0]['duration_in_traffic']
    traffic_time_in_seconds = traffic_time['value']
    return traffic_time_in_seconds

    