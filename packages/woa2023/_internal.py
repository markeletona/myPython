# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 13:38:04 2025

Internal file of the WOA package.

Functions to work with WOA.2023 data.

@author: Markel
"""

import urllib.request
import os
import pandas as pd
import numpy as np

# Create function to download data
def _download_woa_file(variable='temperature',
                       grid_res='1.00',
                       field='an',
                       time_span='decav',
                       time_period='annual',
                       file_format='csv',
                       output_path=None,
                       force_overwrite=False):
    
    """
    Available input parameters are listed below. Note that not all
    combinations of variable-grid_res-time_span-time_period are available.
    Resulting depth ranges can also vary.
    See details in: https://www.ncei.noaa.gov/data/oceans/woa/WOA23/DOCUMENTATION/WOA23_Product_Documentation.pdf
    
    Options for variable are:
    temperature - Temperature (°C)
    salinity    - Salinity (unitless)
    oxygen      - Dissolved Oxygen (µmol/kg)
    o2sat       - Percent Oxygen Saturation (%)
    AOU         - Apparent Oxygen Utilization (µmol/kg)
    silicate    - Silicate (µmol/kg)
    phosphate   - Phosphate (µmol/kg)
    nitrate     - Nitrate (µmol/kg)

    Options for grid_res (grid resolution, in degrees) are:
    0.25
    1.00
    5.00
    
    Options for field are:
    an - Objectively analyzed climatology
    mn - Statistical mean
    dd - Number of observations
    ma - Seasonal or monthly climatology minus annual climatology
    sd - Standard deviation from statistical mean
    se - Standard error of the statistical mean
    oa - Statistical mean minus objectively analyzed climatology
    gp - Number of mean values within radius of influence
    sdo - Objectively analyzed standard deviation
    sea - Standard error of the analysis
    
    time_span refers to the years represented in the climatological mean and 
    statistical fields. Options are:
    1955_1964 - 1955–1964, first decade with sufficient data for climatological mean fields
    1965_1974 - 1965–1974
    1975_1984 - 1975–1984
    1985_1994 - 1985–1994
    1995_2004 - 1995–2004
    2005_2014 - 2005–2014, global coverage of Argo floats from 2005
    2015_2022 - 2015–2022, 8 year “decade”
    1971_2000 - 1971–2000, 30-year climate normal for 1971-2000
    1981_2010 - 1981–2010, 30-year climate normal for 1981-2010
    1991_2020 - 1991–2020, 30-year climate normal for 1991-2020
    decav     - 1955-2022, averaged decades, average of seven decadal means from 1955 to 2022
    all       - Average of all available data. Refers to the 1965-2022 time span for dissolved oxygen (and related fields) and nutrients.
    
    time_period refers to divisions of a calendar year. Options are:
    Annual
    January
    February
    March
    April
    May
    June
    July
    August
    September
    October
    November
    December
    Winter
    Spring
    Summer
    Autumn
    Note: accepts first 3 letters, any upper/lower case.
    
    Options for file_format are:
    csv    - Comma-separated value (csv) format
    netcdf - Climate and Forecast (CF) compliant Network Common Data Format (NetCDF)
    arcgis - ArcGIS-compatible shapefiles
    ascii  - Compact grid format (a legacy WOA ASCII format)
    Note: for netcdf, a file contains all fields.
    
    output_path: where to download files to. If =None, present working 
    directory is selected.
    
    force_overwrite: if True, overwrites requested file if already downloaded
    
    Returns tuple of:
        - requested url
        - headers returned by request
        - resulting local filename (path) 

    """
    
       
    variable_dict = {'temperature': 't',
                     'salinity': 's',
                     'oxygen': 'o',
                     'o2sat': 'O',
                     'AOU': 'A',
                     'silicate': 'i',
                     'phosphate': 'p',
                     'nitrate': 'n'}
    
    grid_res_dict = {'0.25': '04',
                     '1.00': '01',
                     '5.00': '5d'}

    ts_dict = {'1955_1964': '5564',
               '1965_1974': '6574',
               '1975_1984': '7584',
               '1985_1994': '8594',
               '1995_2004': '95A4',
               '2005_2014': 'A5B4',
               '2015_2022': 'B5C2',
               '1971_2000': 'decav71A0',
               '1981_2010': 'decav81B0',
               '1991_2020': 'decav91C0',
               'decav': 'decav',
               'all': 'all'}
    
    tp_dict = {'ann': '00',
               'jan': '01',
               'feb': '02',
               'mar': '03',
               'apr': '04',
               'may': '05',
               'jun': '06',
               'jul': '07',
               'aug': '08',
               'sep': '09',
               'oct': '10',
               'nov': '11',
               'dec': '12',
               'win': '13',
               'spr': '14',
               'sum': '15',
               'aut': '16'}
    
    file_format_dict = {
        'csv': '.csv.gz',
        'netcdf': '.nc',
        'arcgis': '_shape.tar.gz',
        'ascii': '.dat.gz'}
    
    # Based on the codes, prepare file name:
    ts = ts_dict[time_span]
    v = variable_dict[variable]
    time_period = time_period.lower()[:3]
    tp = tp_dict[time_period]
    ff = file_format_dict[file_format]
    grid_res = str(grid_res)
    gr = grid_res_dict[grid_res]

    if not file_format=='netcdf':
        file_name = 'woa23_' + ts + '_' + v + tp + field + gr + ff
    else:
        file_name = 'woa23_' + ts + '_' + v + tp + '_' + gr + ff
    
    # Construct specific part of url:
    spec_url = variable + '/' + file_format + '/' + ts + '/' + grid_res + '/'
    
    # Root URL of the data repository
    root_url = 'https://www.ncei.noaa.gov/data/oceans/woa/WOA23/DATA/'
    
    # Complete url:
    url = root_url + spec_url + file_name
    
    # Set local path to place download (create folder if not present):
    if output_path is None:
        # If output_path not provided, set it as present working directory
        pwd = os.getcwd().replace('\\', '/')
        output_path = pwd + '/WOA/data/'
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_path = output_path + file_name
    else:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        if not output_path[-1]=='/':
            output_path = output_path + '/'
        output_path = output_path + file_name
        
        
        
    # Download if does not exist, or if exists and forced to overwrite
    download = ((not os.path.exists(output_path)) |
                (os.path.exists(output_path) & force_overwrite))
    if download:
        
        # Download file from server
        try:
            fname, headers = urllib.request.urlretrieve(url, output_path)
            
            # Check if file exists
            if os.path.exists(fname) and (os.path.getsize(fname) > 0):
                print(f"{file_name}: \u2705")
                return (url, headers, fname)
            else:
                print(f"{file_name}: \u274C (download failed)")
                return (url, headers, fname)
        
        except Exception as e:
            print(f"{file_name}: \u274C (download failed) -> {e}")
            return (url, None, None)
            
    else:
        print(f"{file_name}: already exists, not overwriting.")
        return (url, None, output_path)
    

#------------------------------------------------------------------------------

def _read_woa_csv(csv_path):
    
    """
    Read a csv file with the WOA format. Returns 1-D arrays for lat, lon and
    depth, an a 2-D array for the values of the variable: (lat, lon, z, v)
    """
    
    # Read compressed csv
    df = pd.read_csv(csv_path, compression='gzip', sep=',', skiprows=1)

    # In the table, each row is a pair of lat-lon, and each column a depth.
    # But the depth array has comments in the first three places (columns),
    # the third one including the 0 depth in it.

    # Extract latitudes, longitudes, depths, and variable values
    lat = np.array(df.iloc[:, 0])
    lon = np.array(df.iloc[:, 1])
    z = np.array([0] + [int(x) for x in df.columns[3:]])
    v = np.array(df.iloc[:, 2:])
    
    return (lat, lon, z, v)


#------------------------------------------------------------------------------

def _create_woa_array(lat, lon, z, v):
    """
    Arrange lat, lon, z and values (as given by read_woa_csv()) into a unique 
    2-D array analogous to the csv file format:
        - 1st column: latitude, lat -> dimension = (M,)
        - 2nd column: longitude, lon -> dimension = (M,)
        - 1st row: depth, z (with two NaN in the 1st and 2nd column) -> dimension = (N, )
        - rest: values (v) -> dimension = (M, N)
        
    Resulting 2-D array is of dimension (M, N+2)

    """
    if not isinstance(lat, np.ndarray):
        lat = np.array(lat)
    if not isinstance(lon, np.ndarray):
        lon = np.array(lon)
    if not isinstance(z, np.ndarray):
        z = np.array(z)
    if not isinstance(v, np.ndarray):
        v = np.array(v)
        
    a = np.column_stack((lat, lon, v))
    z2 = np.append([np.nan, np.nan], z)
    a = np.row_stack((z2, a))
    
    return a

#------------------------------------------------------------------------------

def _woa_csv_to_npz(csv_path, output_path=None):
    """
    Convert WOA csv file into a Numpy compressed npz file.
    """
    # Read file
    lat, lon, z, v = _read_woa_csv(csv_path)
    
    # Arrange a unique 2-D array with lat, lon, z and values, analogous to the
    # csv file format
    a = _create_woa_array(lat, lon, z, v)
    
    # If output_path not provided, do the same as input csv
    if output_path is None:
        output_path = csv_path.replace(".csv", ".npz").replace(".gz", "")
        
    # Save to compressed npz
    np.savez_compressed(output_path, woa_array=a)


#------------------------------------------------------------------------------

def _read_woa_npz(npz_path):
    """
    Reads WOA array from Numpy npz file created with _woa_csv_to_npz(). Returns
    tuple of arrays: ()
    """
    f = np.load(npz_path)['woa_array']
    
    lat = f[1:, 0]
    lon = f[1:, 1]
    z = f[0, 2:]
    v = f[1:, 2:]
    
    return (lat, lon, z, v)