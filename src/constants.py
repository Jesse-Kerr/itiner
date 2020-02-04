from datetime import datetime

# Seconds from Jan 1 1970 to Jan 4 2021. This is used to get
# travel duration. It appears that Google changes every 15 minutes per week, 
# but to send a request the time has to be in the future. I use the 4th so
# that it starts the beginning of the week (it's a Monday)

# The google maps requests are in Greenwhich (UTC) time, which is 6 hours ahead.
# So if I get the seconds as total days, my time0 is really 6PM Texas. So we need to
# add 6 hours to get to Austin midnight
d0 = datetime(1970, 1, 1, 0, 0, 0)
d1 = datetime(2021, 1, 4, 6, 0, 0)

delta = d1 - d0
time0 = int(delta.total_seconds())

# For directions requests
service_url = "https://maps.googleapis.com/maps/api/directions/json?"

