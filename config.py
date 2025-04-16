# Configuration File

# Common metadata
cls = "ea"                  # DO NOT CHANGE
expver = "1"                # DO NOT CHANGE
levtype = "ml"              # DO NOT CHANGE
stream = "oper"             # DO NOT CHANGE

tp = "an"                   # type: Use "an" (analysis) unless you have a particular reason to use "fc" (forecast).
#date    = date             # date: Specify a single date as "2018-01-01" or a period as "2018-08-01/to/2018-01-31". For periods > 1 month see https://confluence.ecmwf.int/x/l7GqB
time = "00:00:00/12:00:00"  # time: ERA5 data is hourly. Specify a single time as "00:00:00", or a range as "00:00:00/01:00:00/02:00:00" or "00:00:00/to/23:00:00/by/1".
grid = [0.25, 0.25]         # lat/lon Degree resolution
area = [18, 98, -12, 131]   # [North, West, South, East]

# For Forward forecasts:
step = "0/to/18"

# North America
#extent = [-125 , -70, 20, 50]

# Western Hemisphere
#area = [50, -125, -40, -32]
#area = [75, -160, -55, -32]

# SEA (High Density of Radiosondes for Equatorial Region)
#area = [18, 98, -12, 131]

# Specific variable configs
zlnsp_config = {
    "levelist": "1",
    "param": "129/152"  # Geopotential, Log surface pressure
}

tq_config = {
    "levelist": "1/to/137",
    "param": "130/133/131/132"  # T, Q, U, V
}
