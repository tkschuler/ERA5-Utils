'''
Script to match the format of Post Sep 2024 ERA5 Reanalysis on pressure levels to Pre Sep 2024 format

Note: This script will change whatever backend netcdf engine to netcdf4.  Converting back to offbit_64 is reccomended for speed using ncks
'''

'''
# Compression Example.  Didn't find this to have a big impact.
nccopy -d1 -c valid_time/100,pressure_level/10,latitude/50,longitude/50 ERA5-H2-2023-SEA.nc optimized_ERA5-H2-2023-SEA.nc
# -d1: Applies light compression (adjust for balance between speed and size).
# -c: Defines chunk sizes optimized for your analysis patterns.
'''

#Next we will change the types:

import xarray as xr

# Open the slow file
ds = xr.open_dataset('FORECASTS/ERA5-H2-2023-USA.nc')

if 'expver' in ds.data_vars:
    ds = ds.drop_vars('expver')
    ds = ds.drop_vars('number')

'''
# Re-encode variables. Didn't find this to have much of an impact either.
encoding = {}
for var in ['z', 'u', 'v']:
    encoding[var] = {'dtype': 'int16', 'scale_factor': ds[var].std().values / 32767,
                     'add_offset': ds[var].mean().values, '_FillValue': -32767}
'''

ds = ds.rename({'valid_time': 'time', 'pressure_level': 'level'})
ds = ds.reindex(level=ds.level[::-1])

# Save to a new file
#ds.to_netcdf('FORECASTS/optimized_ERA5-H2-2023-USA-updated.nc', encoding=encoding)
ds.to_netcdf('FORECASTS/optimized_ERA5-H2-2023-USA.nc')


print(ds)

# Finally run to convert back to offbit_64
"""ncks -6 FORECASTS/optimized_ERA5-H2-2023-SEA.nc FORECASTS/optimized_ERA5-H2-2023-SEA.nc"""
