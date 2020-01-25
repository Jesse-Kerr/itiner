
import json
import urllib

# Using Maps API key to get info on businesses
# I need "Place Details"
place_id = 'ChIJC5k9QO-1RIYRiNYXYcYTUFQ'
service_url = "https://maps.googleapis.com/maps/api/place/details/json"

params = {
    'key': api_key,
    'place_id': place_id
}

url = service_url + '?' + urllib.parse.urlencode(params)
response = json.loads(urllib.request.urlopen(url).read())

# I can get opening_hours, rating, price_level
response['result']