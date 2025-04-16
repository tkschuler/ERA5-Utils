import xarray as xr
import matplotlib.pyplot as plt

#cdo ml2pl,1000,975,950,925,900,875,850,825,800,775,750,700,650,600,550,500,450,400,350,300,250,225,200,175,150,120,100,70,50,30,20,10,7,5,3,2,1 tq_ml.grib cdo_output2.grib

# Open the datasets
#ds1 = xr.open_dataset("../FLOW2D/forecasts/ERA5-H2-2023-SEA.nc")
ds1 = xr.open_dataset("/home/schuler/cds_api/complete_era5_data/2023-ERA5-NORTH_renamed.nc")
#ds1 = xr.open_dataset("reanalysis_data/2023-1-ERA5-Forecast.grib", engine='cfgrib')
#ds1 = xr.open_dataset("/home/schuler/cds_api/complete_era5_data/2023-ERA5-Complete-renamed.nc")
#ds1 = xr.open_dataset("/home/schuler/cds_api/2023-ERA5-Complete-SEA.nc")
#ds1 = xr.open_dataset("Jan-2-forward.nc")

#ds1 = xr.open_dataset("Jan-2-forward.grib", engine="cfgrib", backend_kwargs={'filter_by_keys': {'shortName': 'q'}})
print(ds1)

sdfsdf

print(ds1.valid_time)

#print(ds1.valid_time.values)




# Open the datasets
ds1 = xr.open_dataset("output_pres2.nc")
#print(ds1)
#sdfsdf
#ds2 = xr.open_dataset("output.nc")  #converted pressure
#ds2 = xr.open_dataset("tq_ml.grib", engine='cfgrib')
#ds3 = xr.open_dataset("cdo_output3.grib", engine='cfgrib', filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
#ds3 = xr.open_dataset("Jan-2022.grib", engine='cfgrib', filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
ds3 = xr.open_dataset("01-2022_pres.grib", engine='cfgrib')
#ds3 = xr.open_dataset("Jan-2022.grib", engine='cfgrib', filter_by_keys={'typeOfLevel': 'isobaricInhPa'})
#ds4 = xr.open_dataset("Jan-2022_pres.grib", engine='cfgrib')
#ds5 = xr.open_dataset("z.grib", engine='cfgrib')
#ds4 = xr.open_dataset("tq_ml2.grib", engine='cfgrib')

#ds5 = xr.open_dataset("output_00_06_130_152_1x1.grib", engine='cfgrib')

print(ds1)
#print(ds2)
print(ds3)
#print(ds4)
#print(ds4)
#print(ds5)

# Extract temperature and altitude data
# Assuming temperature ('t') and altitude ('z') are the variables of interest
temp1 = ds1.u.values[34, :, 90, 90]  # Adjust indexing as per dataset structure
alt1 = ds1.coords['pressure_level'].values  # Assuming 'level' or similar for altitude levels

#temp2 = ds2.t.values[0, :, 0, 0]
#alt2 = ds2.coords['pressure'].values/100

temp3 = ds3.u.values[34, :, 90,90]
alt3 = ds3.coords['isobaricInhPa'].values

#temp4 = ds4.u.values[2, 15:, 0,90]
#alt4 = ds4.coords['hybrid'].values[15:]

#temp5 = ds5.t.values[0, 15:, 0,90]
#alt5= ds5.coords['hybrid'].values[15:]

# Create the main plot
fig, ax1 = plt.subplots(figsize=(8, 6))

# Plot temperature vs. pressure for ds1, ds2, and ds3
ax1.plot(temp1, alt1, label="ERA5 Pressure", marker="o")
#ax1.plot(temp2, alt2, label="Converted Pressure ML2PL", marker="s")
ax1.plot(temp3, alt3, label="Converted Pressure CDO", marker="^")

# Customize the first y-axis
ax1.set_xlabel("U-Wind (m/s)")
ax1.set_ylabel("Pressure Levels (hPa)")
ax1.set_yscale('log')  # Set y-axis to logarithmic scale
ax1.invert_yaxis()  # Optional: if pressure decreases with altitude
ax1.grid(which="both", linestyle="--", linewidth=0.5)
ax1.legend(loc="upper left")
ax1.set_title("Temperature vs. Pressure/Model Levels Comparison")

# Create a secondary y-axis for model levels (ds4)
ax2 = ax1.twinx()
#ax2.plot(temp4, alt4, label="ERA5 Model Levels", marker="*", color="red")
#ax2.plot(temp5, alt5, label="ERA5 Model Levels", marker="*", color="black")
ax2.set_ylabel("Model Levels")
ax2.set_yscale('log')  # Set y-axis to logarithmic scale
ax2.invert_yaxis()  # Reverse the y-axis for model levels
ax2.legend(loc="upper right")

# Show the plot
plt.show()
