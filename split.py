import xarray as xr
from tqdm import tqdm

# Open the NetCDF file
file_path = "2023-ERA5-Complete.nc"  # Replace with the path to your NetCDF file
output_north = "2023-ERA5-Complete-WH-North.nc" 
output_south = "2023-ERA5-Complete-WH-South.nc"  
ds = xr.open_dataset(file_path)
print(ds)

#print(ds.lat.values)


# Filter the dataset for latitudes >= 0
ds_north = ds.sel(lat=slice(None, 0))  # Select latitudes from 0 upwards

ds_south = ds.sel(lat=slice(0, None))  #ds.sel(lat=ds.lat < 0)

print(ds_north)
print(ds_south) 
sdfsdf

ds_north.to_netcdf(output_north)
ds_south.to_netcdf(output_south)

print(f"SPlit into North and SOuth for Download")
