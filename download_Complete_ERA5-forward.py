#!/usr/bin/env python
import cdsapi
import argparse
from datetime import datetime, timedelta
import config as cfg

c = cdsapi.Client()

area = [50, -125, -40, -32]
grid = [0.25, 0.25]

# Example date:
date = "2023-01-03"
output = "Jan-3-forward.grib"

c.retrieve("reanalysis-era5-complete", {
    "class": cfg.cls,
    "date": date,
    "expver": cfg.expver,
    "levelist": cfg.zlnsp_config["levelist"],
    "levtype": cfg.levtype,

    "param": cfg.zlnsp_config["param"],
    "step": cfg.step,
    "stream": cfg.stream,
    "time": "06:00:00/18:00:00",
    "type": "fc",
    
    'grid': cfg.grid, # Latitude/longitude grid: east-west (longitude) and north-south resolution (latitude). Default: 0.25 x 0.25
    'area': cfg.area,
}, output)
