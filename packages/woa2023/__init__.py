# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 15:42:06 2025

Public API of the woa2023 package.

Functions to work with WOA.2023 data.

https://www.ncei.noaa.gov/access/world-ocean-atlas-2023/
https://www.ncei.noaa.gov/data/oceans/woa/WOA23/DOCUMENTATION/WOA23_Product_Documentation.pdf


Depends on:
    - urllib.request
    - os
    - pandas
    - numpy

@author: Markel
"""

from packages.woa2023 import _internal


def download_woa_file(variable='temperature',
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
    
    Options for `variable` are:
    temperature - Temperature (°C)
    salinity    - Salinity (unitless)
    oxygen      - Dissolved Oxygen (µmol/kg)
    o2sat       - Percent Oxygen Saturation (%)
    AOU         - Apparent Oxygen Utilization (µmol/kg)
    silicate    - Silicate (µmol/kg)
    phosphate   - Phosphate (µmol/kg)
    nitrate     - Nitrate (µmol/kg)

    Options for `grid_res` (grid resolution, in degrees) are:
    0.25
    1.00
    5.00
    
    Options for `field` are:
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
    
    `time_span` refers to the years represented in the climatological mean and 
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
    
    `time_period` refers to divisions of a calendar year. Options are:
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
    
    Options for `file_format` are:
    csv    - Comma-separated value (csv) format
    netcdf - Climate and Forecast (CF) compliant Network Common Data Format (NetCDF)
    arcgis - ArcGIS-compatible shapefiles
    ascii  - Compact grid format (a legacy WOA ASCII format)
    Note: for netcdf, a file contains all fields.
    
    `output_path`: where to download files to. If =None, present working 
    directory is selected.
    
    `force_overwrite`: if True, overwrites requested file if already downloaded
    
    Returns tuple of:
        - requested url
        - headers returned by request
        - resulting local filename (path) 

    """
    
    return _internal._download_woa_file(variable=variable,
                                        grid_res=grid_res,
                                        field=field,
                                        time_span=time_span,
                                        time_period=time_period,
                                        file_format=file_format,
                                        output_path=output_path,
                                        force_overwrite=force_overwrite)


#------------------------------------------------------------------------------

def read_woa_csv(csv_path):
    
    """
    Read a csv file with the WOA format. Returns 1-D arrays for lat, lon and
    depth, an a 2-D array for the values of the variable: (lat, lon, z, v)
    """
    
    return _internal._read_woa_csv(csv_path)


#------------------------------------------------------------------------------

def create_woa_array(lat, lon, z, v):
    """
    Arrange lat, lon, z and values (as given by read_woa_csv()) into a unique 
    2-D array analogous to the csv file format:
        - 1st column: latitude, lat -> dimension = (M,)
        - 2nd column: longitude, lon -> dimension = (M,)
        - 1st row: depth, z (with two NaN in the 1st and 2nd column) -> dimension = (N, )
        - rest: values (v) -> dimension = (M, N)
        
    Resulting 2-D array is of dimension (M+1, N+2)

    """
    return _internal._create_woa_array(lat, lon, z, v)
    
#------------------------------------------------------------------------------

def woa_csv_to_npz(csv_path, output_path=None):
    """
    Convert WOA csv file into a Numpy compressed npz file. Contains a 2-D array 
    analogous to the csv file format:
        - 1st column: latitude, lat -> dimension = (M,)
        - 2nd column: longitude, lon -> dimension = (M,)
        - 1st row: depth, z (with two NaN in the 1st and 2nd column) -> dimension = (N, )
        - rest: values (v) -> dimension = (M, N)
        
    Resulting 2-D array is of dimension (M+1, N+2)
    """
    return _internal._woa_csv_to_npz(csv_path, output_path=output_path)


#------------------------------------------------------------------------------

def read_woa_npz(npz_path):
    """
    Reads WOA array from Numpy npz file created with woa_csv_to_npz(). Returns 
    1-D arrays for lat, lon and depth, an a 2-D array for the values of the 
    variable: (lat, lon, z, v)
    """
    return _internal._read_woa_npz(npz_path)
