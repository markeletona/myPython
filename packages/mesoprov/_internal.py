# -*- coding: utf-8 -*-
"""
Created on Thu Oct  2 13:40:23 2025

Internal functions for the mesoprov package.
        
@author: Markel
"""

import os
from pathlib import Path
from json import load
from shapely import from_geojson
from shapely.geometry import Point


#%% READ DATA

#%%% SUTTON

# Load province polygons from geojson files, and name dictionaries from json files
dpath = 'deriveddata/meso_prov/sutton/'
files = [x for x in os.listdir(dpath) if '.geojson' in x]

polys_sutton = {}
for f in files:
    fpath = Path(dpath + f)
    polys_sutton[f.replace(".geojson", "")] = from_geojson(fpath.read_text())
    

fpath = 'deriveddata/meso_prov/sutton/sutton_province_names.json'
with open(fpath, 'r') as f:
    provnames_sutton = load(f)
    

#%%% REYGONDEAU

dpath = 'deriveddata/meso_prov/reygondeau/'
files = [x for x in os.listdir(dpath) if '.geojson' in x]

polys_reygon = {}
for f in files:
    fpath = Path(dpath + f)
    polys_reygon[f.replace(".geojson", "")] = from_geojson(fpath.read_text())
    

fpath = 'deriveddata/meso_prov/reygondeau/reygondeau_province_names.json'
with open(fpath, 'r') as f:
    provnames_reygon = load(f)


#%% FUNCTIONS

def _list_provinces(reygondeau=True, sutton=True):
    """
    Displays the province codes and names of the mesopelagic province 
    classifications.

    Parameters
    ----------
    reygondeau : True/False, optional.
        List provinces from Reygondeau et al. (2018)? The default is True.
    sutton : True/False, optional.
        List provinces from Sutton et al. (2017)? The default is True.

    Returns
    -------
    None.

    """
    
    if reygondeau:
        print("\n----------------------------------------------------\n\n"
              "Reygondeau et al. (2018): \n")
        for p in provnames_reygon:
            print(p + ": " + provnames_reygon[p])
    
    if sutton:
        print("\n----------------------------------------------------\n\n"
              "Sutton et al (2017): \n")
        for p in provnames_sutton:
            print(p + ": " + provnames_sutton[p])



def _find_province_of_coord(x, y, prov_class='reygondeau', out_type='code'):   
    """
    Find the mesopelagic province to which a point of x,y coordinates belongs.
    
    Parameters
    ----------
    x : FLOAT
        LONGITUDE of point. Must be a float or coercible to float.
    y : FLOAT
        LATITUDE of point. Must be a float or coercible to float.
    prov_class: STRING, optional
        The province classification to use, either 'reygondeau' or 'sutton'.
        The default is 'reygondeau'.
    out_type : STRING, optional
        Output type, one of 'code' (province code) or 'name' (full name of 
        province). The default is 'code'.

    Returns
    -------
    The mesopelagic province code or full name for coordinates x,y. If a point
    happens to fall in a boundary between province, chained codes are returned.
    If a point does not belong to any province (e.g., to shallow) 'NOT_IN_PROV'
    is returned.

    """
    x = float(x)
    y = float(y)

    # Get coordinates of point
    scoords = (x, y)
    
    if prov_class=='reygondeau':
        prov_polys = list(polys_reygon.values())
        prov_codes = list(polys_reygon.keys())
        prov_names = provnames_reygon
    elif prov_class=='sutton':
        prov_polys = list(polys_sutton.values())
        prov_codes = list(polys_sutton.keys())
        prov_names = provnames_sutton
    else:
        ValueError("invalid prov_class. Should be either 'reygondeau' or 'sutton'")
        
    # Check if point is in province polygons (or touching over boundary)
    is_in_poly = (Point(scoords).within(prov_polys) |
                  Point(scoords).touches(prov_polys))
        
    # Get the province that returned True
    if sum(is_in_poly)==1:
        
        i = [i for i, boo in enumerate(is_in_poly) if boo][0]
        pc = prov_codes[i]
        out = {'code': pc, 'name': prov_names[pc]}
        
    elif sum(is_in_poly)==0:
        
        out = {'code': 'NOT_IN_PROV', 
               'name': 'Point not in any province. Likely land, or unassigned area (e.g. too shallow).'}
        
    else:
        i = [i for i, boo in enumerate(is_in_poly) if boo]
        pc = [prov_codes[j] for j in i]
        pn = [prov_names[c] for c in pc]
        out = {'code': '_and_'.join(pc),
               'name': ' and '.join(pn)}
        print(str(scoords) + ": MULTIPLE MATCHES. Edge case, likely point over boundary.")
    return(out[out_type])



def _get_mesopelagic_province_polygon(prov_code=None, prov_class='reygondeau'):
    """
    Returns the MultiPolygon of an specific mesopelagic province. If no input 
    is provided, MultiPolygons of all provinces are returned.

    Parameters
    ----------
    prov_code : STRING, optional
        Mesopelagic province code for which the polygon is to be retrieved. The
        default is None, i.e., returns a dictionary with shapes of all 
        provinces.
    prov_class: STRING, optional
        The province classification to use, either 'reygondeau' or 'sutton'.
        The default is 'reygondeau'.

    Returns
    -------
    Multypoligon object for requested province, or dict with all of them.

    """
    
    if not prov_class in ['reygondeau', 'sutton']:
        ValueError("invalid prov_class. Should be either 'reygondeau' or 'sutton'")
    
    # If no input, return all shapes
    if prov_code==None:
        if prov_class=='reygondeau':
            prov_poly = polys_reygon
        elif prov_class=='sutton':
            prov_poly = polys_sutton
            
    else:
        # Return shape for specified province
        if prov_class=='reygondeau':
            if not prov_code in polys_reygon.keys():
                raise ValueError("invalid prov_code.")
            else:
                prov_poly = polys_reygon[prov_code]
                
        elif prov_class=='sutton':
            if not prov_code in polys_sutton.keys():
                raise ValueError("invalid prov_code.")
            else:
                prov_poly = polys_sutton[prov_code]

    return prov_poly