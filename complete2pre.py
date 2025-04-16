import xarray as xr
from tqdm import tqdm

#Complete.grib works?
#SOUTH.grib works?

# Open the NetCDF file
file_path = "/home/schuler/cds_api/2023-ERA5-Complete-SEA.nc"
output_file = "2023-ERA5-Complete-SEA_renamed.nc"  # Output file name
ds = xr.open_dataset(file_path)
print(ds)

dfgdfg


ds_renamed = ds.rename({
    'lat': 'latitude',
    'lon': 'longitude',
    'plev': 'level'
    # etc.
})

ds_renamed = ds_renamed.assign_coords(level=ds_renamed.level / 100)

#remap longtiude from 0/360 to -180/180
# Conditionally shift longitudes > 180
new_longitude = xr.where(ds_renamed.longitude > 180,
                         ds_renamed.longitude - 360,
                         ds_renamed.longitude)
ds_renamed = ds_renamed.assign_coords(longitude=new_longitude)


ds_renamed= ds_renamed.reindex(level=list(reversed(ds_renamed.level)))

print()
print()
print(ds_renamed)

#For matching size
#ds_renamed = ds_renamed.sel(latitude=slice(45,30),
#                            longitude = slice(-125,-100))

ds_renamed.to_netcdf(output_file)
#print()
#print()
#print(ds_renamed)

print(f"Filtered file saved to {output_file}")


'''This process converts the netcdf file from 64bit_offset back to netcdf4, and we want to convert it back for faster running'''

"""ncks -6 2023-ERA5-Complete-SEA_renamed.nc 2023-ERA5-Complete-SEA_renamed_64bit.nc"""
