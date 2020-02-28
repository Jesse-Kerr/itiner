from datetime import datetime

# Seconds from Jan 1 1970 to Jan 2 2021. This is used to get
# travel duration. It appears that Google changes every 15 minutes per week, 
# but to send a request the time has to be in the future. I use the 2nd so
# that it starts on a Saturday beginning of the week (it's a Monday)

# The google maps requests are in Greenwhich (UTC) time, which is 6 hours ahead.
# So if I get the seconds as total days, my time0 is really 6PM Texas. So we need to
# add 6 hours to get to Austin midnight

# time0 = datetime(1970, 1, 1, 7, 0, 0) # austin midnight
# sat = datetime(2021, 1, 2, 0, 0, 0)
# mon = datetime(2021, 1, 4, 0, 0, 0)

# sat0 = int((sat - time0).total_seconds())
# mon0 = int((mon - time0).total_seconds())

# The answer is below, but I keep the comment above for safekeeping
sat0 = 1609570800
mon0 = 1609743600 

# For directions requests
directions_url = "https://maps.googleapis.com/maps/api/directions/json?"

distance_matrix_url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
