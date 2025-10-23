# -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 12:45:51 2025

Public API of the mesoprov package. It has utility functions to work with the 
mesopelagic biogeochemical/biogeographic provinces defined in:
    
    - Sutton et al. (2017). A global biogeographic classification of the 
    mesopelagic zone. Deep Sea Research Part I, 126: 85-102. 
    doi:10.1016/j.dsr.2017.05.006
    - Reygondeau et al. (2018). Global biogeochemical provinces of the 
    mesopelagic zone. J Biogeogr., 45: 500–514. doi:10.1111/jbi.13149 

    Internally depends on:
        - os
        - pathlib
        - json
        - shapely
        - (plus also 'typing' here)

@author: Markel
"""

# Import internal functions to use in the public API
from scripts.modules.mesoprov import _internal
from typing import Union, Dict
from shapely.geometry import MultiPolygon

#------------------------------------------------------------------------------

def list_provinces(reygondeau: bool = True, sutton: bool = True) -> None:
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
    
    return _internal._list_provinces(reygondeau=reygondeau, sutton=sutton)


#------------------------------------------------------------------------------

def find_province_of_coord(
        x: float, 
        y: float, 
        prov_class: str = 'reygondeau', 
        out_type: str = 'code') -> str:
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
    return _internal._find_province_of_coord(
        x,
        y,
        prov_class=prov_class,
        out_type=out_type
        )

#------------------------------------------------------------------------------

def get_mesopelagic_province_polygon(
        prov_code: str = None,
        prov_class: str = 'reygondeau') -> Union[Dict[str, MultiPolygon], MultiPolygon]:
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
    MultiPolygon object for requested province, or dict with all of them.

    """
    return _internal._get_mesopelagic_province_polygon(
        prov_code=prov_code, 
        prov_class=prov_class
        )