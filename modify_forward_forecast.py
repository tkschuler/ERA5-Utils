import xarray as xr
import numpy as np

# Open the NetCDF dataset
ds = xr.open_dataset("reanalysis_data/2023-1-ERA5-Forecast.grib", engine='cfgrib')
print(ds)

# Select only the steps that are 06:00:00 and 18:00:00 (index 6 and 18)
valid_steps = [6, 18]
ds_filtered = ds.isel(step=valid_steps)

# Adjust the time based on the selected steps (only 06:00 and 18:00)
# For 06:00, use the original time. For 18:00, add 12 hours to the time
adjusted_time = ds_filtered["time"].copy()


# For step 18, add 12 hours to the time
adjusted_time.values[0::] += np.timedelta64(6, 'h')


# Replace the old time variable with the adjusted time
ds_filtered.coords["time"] = ("time", adjusted_time.values)

# Now drop the step dimension, as it is no longer needed
ds_new = ds_filtered.drop_vars("step")

print(ds_new)
sdfsdf

# Save the new dataset
ds_new.to_netcdf("new_forecast.nc")

print(ds_new)