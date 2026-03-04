"""
Nitrate data processing routines.
"""
import numpy as np
from netCDF4 import Dataset

def process_nitrate_data(nc_path: str):
    with Dataset(nc_path, 'r') as nc:
        pass
