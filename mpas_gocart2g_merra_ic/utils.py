"""
Utility functions and data structures for satellite data processing.
"""
import datetime
from typing import List, Optional

class SpeciesMap:
    def __init__(self, goc_cnt: int, wrf_wght: float, wrf_name: str,
                 goc_wght: Optional[List[float]] = None,
                 goc_names: Optional[List[str]] = None,
                 goc_ext: Optional[List[bool]] = None):
        self.goc_cnt = goc_cnt
        self.wrf_wght = wrf_wght
        self.wrf_name = wrf_name
        self.goc_wght = goc_wght or []
        self.goc_names = goc_names or []
        self.goc_ext = goc_ext or []

def wrf2mz_time(wrf_time: str):
    try:
        dt = datetime.datetime.strptime(wrf_time, "%Y-%m-%d_%H:%M:%S")
        ncdate = int(dt.strftime("%Y%m%d"))
        ncsec = dt.hour * 3600 + dt.minute * 60 + dt.second
        ncmonth = dt.month
        return ncdate, ncsec, ncmonth
    except Exception as e:
        raise ValueError(f"Invalid WRF time format: {wrf_time}") from e
