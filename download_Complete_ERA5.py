#!/usr/bin/env python
import cdsapi
import argparse
from datetime import datetime, timedelta
import config as cfg

# Parse arguments for year and month
parser = argparse.ArgumentParser(description="Download ERA5 data for a specific year and month.")
parser.add_argument("--year", required=True, type=int, help="Year for data download (e.g., 2022).")
parser.add_argument("--month", required=True, type=int, help="Month for data download (e.g., 1 for January).")
parser.add_argument("--output_dir", required=True, type=str, default=".", help="Output directory for data download and processing.")
#parser.add_argument("--output-tq", required=True, type=str, help="Output file for temperature and specific humidity.")
#parser.add_argument("--output-zlnsp", required=True, type=str, help="Output file for geopotential and lnsp.")
args = parser.parse_args()


# Extract year and month from arguments
year = args.year
month = args.month
output_dir = args.output_dir
#output_tq = args.output_tq
#output_zlnsp = args.output_zlnsp

# Ensure month is two digits
month_str = f"{month:02d}"

# Compute the start and end dates of the month
start_date = f"{year}-{month_str}-01"
end_date = (datetime(year, month + 1, 1) - timedelta(days=1)).strftime("%Y-%m-%d") if month < 12 else f"{year}-12-31"
date = f"{start_date}/to/{end_date}"
print("Downloading... for " + date)


# Define output file names based on year and month
output_tq = f"{output_dir}/{month_str}-{year}-tq_ml.grib"
output_zlnsp = f"{output_dir}/{month_str}-{year}-zlnsp_ml.grib"

c = cdsapi.Client()


# zlnsp request
c.retrieve("reanalysis-era5-complete", {
    "class": cfg.cls,
    "date": date,
    "expver": cfg.expver,
    "levelist": cfg.zlnsp_config["levelist"],
    "levtype": cfg.levtype,
    "param": cfg.zlnsp_config["param"],
    "stream": cfg.stream,
    "time": cfg.time,
    "type": cfg.tp,
    "grid": cfg.grid,
    "area": cfg.area,
}, output_zlnsp)

# tq request
c.retrieve("reanalysis-era5-complete", {
    "class": cfg.cls,
    "date": date,
    "expver": cfg.expver,
    "levelist": cfg.tq_config["levelist"],
    "levtype": cfg.levtype,
    "param": cfg.tq_config["param"],
    "stream": cfg.stream,
    "time": cfg.time,
    "type": cfg.tp,
    "grid": cfg.grid,
    "area": cfg.area,
}, output_tq)

'''
c.retrieve('reanalysis-era5-complete', {
    'class'   : cls,
    'date'    : date,
    'expver'  : expver,
    'levelist': '1/to/137',       # Geopotential (z) and Logarithm of surface pressure (lnsp) are 2D fields, archived as model level 1
    'levtype' : levtype,
    'param'   : '129/152/130/133', # Geopotential (z) and Logarithm of surface pressure (lnsp)
    'stream'  : stream,
    'time'    : time,
    'type'    : tp,
    'grid'    : [1.0, 1.0], # Latitude/longitude grid: east-west (longitude) and north-south resolution (latitude). Default: 0.25 x 0.25
    'area'    : area, #example: [60, -10, 50, 2], # North, West, South, East. Default: global
}, 'gribby.grib')
'''
