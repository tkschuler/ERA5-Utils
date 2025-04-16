# **************************** LICENSE START ***********************************
#
# Copyright 2022 ECMWF. This software is distributed under the terms
# of the Apache License version 2.0. In applying this license, ECMWF does not
# waive the privileges and immunities granted to it by virtue of its status as
# an Intergovernmental Organization or submit itself to any jurisdiction.
#
# ***************************** LICENSE END ************************************


#Mandatory Pressure levels:
#100000 97500 95000 92500 90000 87500 85000 82500 80000 77500 75000 70000 65000 60000 55000 50000 45000 40000 35000 30000 25000 22500 20000 17500 15000 12000 10000 7000 5000 3000 2000 1000 700 500 300 200 100

#100000, 97500, 95000, 92500, 90000 87500 85000 82500 80000 77500 75000 70000 65000 60000 55000 50000 45000 40000 35000 30000 25000 22500 20000 17500 15000 12000 10000 7000 5000 3000 2000 1000 700 500 300 200 100

import cfgrib
import xarray as xr
import numpy as np
from eccodes import *
import matplotlib.pyplot as plt
import argparse
import sys
import os
from tqdm import tqdm, trange

def parse_args():
    ''' Parse program arguments using ArgumentParser'''
    parser = argparse.ArgumentParser(description ="Python tool to calculate the model level variable at a given pressure level and write data to a netCDF file")
    parser.add_argument('-p', '--pressure', required=True, nargs='+',type=float,
                        help='Pressure levels (Pa) to calculate the variable')
    parser.add_argument('-o', '--output', required=False, help='name of the output file (default "output.nc"')
    parser.add_argument('-i', '--input', required=True, metavar='input.grib', type=str,
                        help=('grib file with required variable(s) on model level and surface pressure fields',
                              'the model levels'))
    args = parser.parse_args()
    if not args.output:
        args.output = 'output.nc'
    return args

def get_input_variable_list(fin):
    f = open(fin)
    var_list = []
    while 1:
        gid = codes_grib_new_from_file(f)
        if gid is None:
            break
        keys = ('dataDate', 'dataTime', 'shortName')
        for key in keys:
            if key == 'shortName':
              var_list.append(codes_get(gid, key))
        codes_release(gid)
    var_list_unique = list(set(var_list))
    f.close()
    if 'lnsp' not in var_list_unique:
      print("Error - lnsp variable missing from input file -exiting")
      sys.exit()
    if len(var_list_unique) < 2:
      print("Error - Data variable missing from input file -exiting")
      sys.exit()
    return var_list_unique

def check_requested_levels(plevs):
    check_lev = True
    if len(plevs) > 1:
        error_msg = "Error - only specify 1 input pressure level to interpolate to"
    else:
        for lev in plevs:
           if lev < 0 or lev > 110000 :
              check_lev = False
              error_msg = "Error - negative values and large positive values for pressure are not allowed -exiting"
    if check_lev == False:
        print(error_msg)
        sys.exit()
    return check_lev

def check_in_range(data_array,requested_levels):
    amin = data_array.minimum()
    amax = data_array.maximum()
    print("min max ",amin,amax)

def vertical_interpolate(vcoord_data, interp_var, interp_level):
    """A function to interpolate sounding data from each station to
    every millibar. Assumes a log-linear relationship.

    Input
    -----
    vcoord_data : A 1D array of vertical level values (e.g. from ERA5 pressure at model levels at a point)
    interp_var : A 1D array of the variable to be interpolated to the  pressure level
    interp_level : A 1D array containing the vertical level to interpolate to

    Return
    ------
    interp_data : A 1D array that contains the interpolated variable on the interp_level
    """

    l_count = 0
    for l in interp_level:
      if l < np.min(vcoord_data) or l > np.max(vcoord_data):
        ip = [np.NAN]
      else:
    # Make vertical coordinate data and grid level log variables
        lnp = np.log(vcoord_data)
        lnp_interval = [np.log(x) for x in interp_level]
    # Use numpy to interpolate from observed levels to grid levels
        ip = np.interp(lnp_interval, lnp, interp_var)
    return ip[0]

def calculate_pressure_on_model_levels(ds_var,ds_lnsp):
    # Get the number of model levels in the input variable
    nlevs=ds_var.sizes['hybrid']
    # Get the a and b coefficients from the pv array to calculate the model level pressure
    pv_coeff = np.array(ds_var.GRIB_pv)
    pv_coeff=pv_coeff.reshape(2,nlevs+1)
    a_coeff=pv_coeff[0,:]
    b_coeff=pv_coeff[1,:]
    # get the surface pressure in hPa
    sp = np.exp(ds_lnsp)
    p_half=[]
    for i in range(len(a_coeff)):
        p_half.append(a_coeff[i] + b_coeff[i] * sp)
    p_ml=[]
    for hybrid in range(len(p_half) - 1):
        p_ml.append((p_half[hybrid + 1] + p_half[hybrid]) / 2.0)
    ds_p_ml = xr.concat(p_ml, 'hybrid')
    return ds_p_ml

def plot_profile(var_ml,press_ml, var_int_press,var_int_plevs,tstep,lat,lon):

    var_v= var_ml.sel(time = var_ml.time[tstep],longitude=lon, latitude=lat, method='nearest')
    var_v_values = var_v.values
    var_p= press_ml.sel(time = var_ml.time[tstep],longitude=lon, latitude=lat, method='nearest')
    var_p_values = var_p.values
    var_ip= var_int_press.sel(time = var_ml.time[tstep],longitude=lon, latitude=lat, method='nearest')
    var_ip_values = var_ip.values
    var_ip_p = var_ip.pressure
    var_ip_p_values = var_ip_p.values
    plt.axis([min(var_v_values), max(var_v_values), max(var_p_values), min(var_p_values)])
    plt.plot(var_v_values,var_p_values, 'o', color = 'black')
    plt.plot(var_ip_values,var_ip_p_values,'o', color = 'red')
    plt.show()
    return

def calculate_interpolated_pressure_field(data_var_on_ml, data_p_on_ml,plevs):
    nlevs = len(data_var_on_ml.hybrid)
    p_array = np.stack(data_p_on_ml, axis=2).flatten()
    # Flatten the data array to enable faster processing
    var_array = np.stack(data_var_on_ml, axis=2).flatten()
    no_grid_points =  int(len(var_array)/nlevs)

    #interpolated_var = [] #np.empty((len(plevs), no_grid_points))
    ds_shape = data_var_on_ml.shape
    nlats_values = data_var_on_ml.coords['latitude']
    nlons_values = data_var_on_ml.coords['longitude']
    nlats = len(nlats_values)
    nlons = len(nlons_values)

#     Iterate over the data, selecting one vertical profile at a time
    count = 0
    #profile_count = 0
    interpolated_values=[]
    for point in trange(no_grid_points, desc="Processing Profiles"):
        offset =  count*nlevs
        var_profile = var_array[offset:offset+nlevs]
        p_profile = p_array[offset:offset+nlevs]

        # Interpolate to each pressure level in plevs
        for plev in plevs:
            interpolated_values.append(vertical_interpolate(p_profile, var_profile, plevs))
            #profile_count += len(p_profile)
        count = count + 1

    # Reshape the interpolated values into the required shape
    interpolated_field=np.asarray(interpolated_values).reshape(len(plevs),nlats,nlons)
    return interpolated_field

def check_data_cube(dc):
    checks = True
    for var_name in dc.variables:
        if var_name in ['time','step','hybrid','latitude','longitude','valid_time']:
            continue
        if var_name == 'lnsp':
            lnsp_dims = ['time','latitude','longitude']
            if all(value in lnsp_dims for value in dc.variables[var_name].dims):
                continue
            else:
                print("Not all required lnsp dimensions found -exiting ", dc.variables[var_name].dims)
                checks = False
        else:
            var_dims = ['time','hybrid','latitude','longitude']
            if all(value in var_dims for value in dc.variables[var_name].dims):
                continue
            else:
                print("Not all required variable dimensions found -exiting ",dc.variables[var_name].dims)
                checks = False
            continue
    return checks

def main():
    '''Main function'''
    print("-p <pressure level (Pa) > -o <output_file> -i <input grib file>")
    print("e.g. to process a grib file containing 6 hours of lnsp and temperature data to the 500 hPa level:")
    print("python3 script.py -o output_press.nc -p 50000  -i output_00_06_130_152_1x1.grib`n")
    args = parse_args()

    print('Arguments: %s' % ", ".join(
        ['%s: %s' % (k, v) for k, v in vars(args).items()]))

    plevels = args.pressure
    plevels.sort(reverse = True)

    check_requested_levels(plevels)

    input_fname = args.input
    output_fname = args.output
    if not os.path.isfile(input_fname):
        print("Input file does not exist - exiting")
        sys.exit()
    variable_list = get_input_variable_list(input_fname)
    # Create a data object to hold the input and derived data
    data_cube = xr.merge(cfgrib.open_datasets(input_fname, backend_kwargs={'read_keys': ['pv']}), combine_attrs='override')
    if not check_data_cube(data_cube):
        sys.exit()
   # Get the ln surface pressure
    lnsp = data_cube['lnsp']
    for var in variable_list:
      if var == 'lnsp':
          continue
      else:
          data_cube['pml']=data_cube[var].copy()
          break
    for var in variable_list:
        if var == 'lnsp' :
            continue
        data_pressure_on_model_levels_list =[]
        for time_step in tqdm(range(len(data_cube[var].time)), desc=f"Processing {var} (Time Steps)"):
            data_slice_var=data_cube[var][time_step,:,:,:]
            data_slice_lnsp=data_cube['lnsp'][time_step,:,:]
            #   Get the pressure field on model levels for each timestep
            data_cube['pml'][time_step,:,:,:] = calculate_pressure_on_model_levels(data_slice_var,data_slice_lnsp)
    data_cube['pml'].attrs = {'units' : 'Pa','long_name':'pressure','standard_name':'air_pressure','positive':'down'}
    all_interpolated_var_fields_list = []
    for var in variable_list:
        if var == 'lnsp' or var == 'pml':
            continue
        interpolated_var_field = data_cube[var].copy()
        interpolated_var_field = interpolated_var_field[:,0:len(plevels),:,:]
        interpolated_var_field = interpolated_var_field.rename({'hybrid':'pressure'})
        interpolated_var_field['pressure'] = plevels
        for time_step in tqdm(range(len(data_cube[var].time)), desc=f"Interpolating {var}"):
            var_on_ml = data_cube[var][time_step,:,:,:]
            p_on_ml = data_cube['pml'][time_step,:,:,:]
            interpolated_var_field[time_step,:,:,:] = calculate_interpolated_pressure_field(var_on_ml,p_on_ml,plevels)
        all_interpolated_var_fields_list.append(interpolated_var_field)
    all_interpolated_var_fields = xr.merge(all_interpolated_var_fields_list)
    all_interpolated_var_fields['pressure'].attrs = {'units' : 'Pa','long_name':'pressure','standard_name':'air_pressure','positive':'down'}
    all_interpolated_var_fields.to_netcdf(output_fname)
#   Write interpolated data variable to output filename
    PLOT_DATA = False
    if PLOT_DATA:
        latitude = 45.0
        longitude = 0
        tstep =0
        plot_profile(data_cube[var],data_cube['pml'],interpolated_var_field,plevels,tstep,latitude,longitude)
    print("Finished interpolation of variables to pressure level")

if __name__ == '__main__':
    main()
