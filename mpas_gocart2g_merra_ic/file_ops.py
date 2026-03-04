import struct

def subset_time(in_dir: str, out_dir: str, pattern: str = 'MERRA2_400.inst3_3d_ae*.nc4', hours = [0, 6, 12, 18]):
    import numpy as np
    from netCDF4 import Dataset, num2date
    import os, glob
    os.makedirs(out_dir, exist_ok=True)
    files = glob.glob(os.path.join(in_dir, pattern))
    for f in files:
        b = os.path.basename(f).replace('.nc4', '')
        with Dataset(f, 'r') as src:
            time_var = src.variables.get('time')
            if time_var is None:
                raise ValueError(f"No 'time' variable found in {f}")
            times = num2date(time_var[:], units=time_var.units)
            for hh in hours:
                idx = [i for i, t in enumerate(times) if t.hour == hh]
                if not idx:
                    continue
                hh2 = f"{hh:02d}"
                out_file = os.path.join(out_dir, f"{b}_{hh2}Z.nc4")
                if os.path.exists(out_file):
                    print(f"Skipping existing hourly file: {out_file}")
                    continue
                print(f"Creating hourly file: {out_file}")
                with Dataset(out_file, 'w') as dst:
                    for name, dim in src.dimensions.items():
                        if name == 'time':
                            dst.createDimension(name, len(idx))
                        else:
                            dst.createDimension(name, len(dim) if not dim.isunlimited() else None)
                    for name, var in src.variables.items():
                        out_var = dst.createVariable(name, var.datatype, var.dimensions)
                        out_var.setncatts({k: var.getncattr(k) for k in var.ncattrs()})
                        if 'lev' in var.dimensions:
                            for lev in range(var.shape[var.dimensions.index('lev')]):
                                print(f"Processing variable: {name}, level: {lev}")
                        if 'time' in var.dimensions:
                            out_var[:] = var[idx, ...]
                        else:
                            out_var[:] = var[:]
                    dst.setncatts({k: src.getncattr(k) for k in src.ncattrs()})

def combine_files(aer_files, ovp_file, out_files):
    import shutil
    for aer, out in zip(aer_files, out_files):
        with open(out, 'wb') as outfile:
            for fname in [aer, ovp_file]:
                with open(fname, 'rb') as infile:
                    shutil.copyfileobj(infile, outfile)

def write_mpas_binary(output_path, header, slab):
    with open(output_path, 'ab') as f:
        header_fmt = 'i24sf32s8s25s46sfiii8sfffffi'
        packed_header = struct.pack(
            header_fmt,
            header['ifv'],
            header['hdate'].encode('ascii'),
            header['xfcst'],
            header['map_source'].encode('ascii'),
            header['field'].encode('ascii'),
            header['units'].encode('ascii'),
            header['desc'].encode('ascii'),
            header['xlvl'],
            header['nlon'],
            header['nlat'],
            header['iproj'],
            header['startloc'].encode('ascii'),
            header['startlat'],
            header['startlon'],
            header['deltalat'],
            header['deltalon'],
            header['earth_radius'],
            int(header['is_wind_earth_rel'])
        )
        slab_flat = slab.astype('float32').flatten()
        packed_slab = struct.pack(f'{len(slab_flat)}f', *slab_flat)
        record = packed_header + packed_slab
        record_len = len(record)
        f.write(struct.pack('i', record_len))
        f.write(record)
        f.write(struct.pack('i', record_len))

# Example usage: Writing MPAS binary file for all variables/levels
def process_and_write_mpas_binary(nc_path, output_path):
    from netCDF4 import Dataset
    with Dataset(nc_path, 'r') as nc:
        for varname in nc.variables:
            var = nc.variables[varname]
            if varname in ('lat', 'lon', 'time', 'lev'):
                continue
            print(f"Processing variable: {varname}")
            dims = var.dimensions
            shape = var.shape
            if len(shape) == 4:
                for k in range(shape[1]):
                    slab = var[0, k, :, :]
                    fieldname = f"{varname}__{k+1:03d}"
                    nlon = slab.shape[1]
                    nlat = slab.shape[0]
                    header = {
                        'ifv': 5,
                        'hdate': '2026-03-04_00:00:00',
                        'xfcst': 0.0,
                        'map_source': 'From file ' + nc_path,
                        'field': fieldname[:8],
                        'units': getattr(var, 'units', 'unknown')[:25],
                        'desc': getattr(var, 'long_name', 'desc')[:46],
                        'xlvl': float(k+1),
                        'nlon': nlon,
                        'nlat': nlat,
                        'iproj': 0,
                        'startloc': 'SWCORNER',
                        'startlat': float(nc.variables['lat'][0]),
                        'startlon': float(nc.variables['lon'][0]),
                        'deltalat': float(nc.variables['lat'][1] - nc.variables['lat'][0]),
                        'deltalon': float(nc.variables['lon'][1] - nc.variables['lon'][0]),
                        'earth_radius': 6367470.0 * 0.001,
                        'is_wind_earth_rel': False
                    }
                    write_mpas_binary(output_path, header, slab)
            elif len(shape) == 3:
                for k in range(shape[0]):
                    slab = var[k, :, :]
                    fieldname = f"{varname}__{k+1:03d}"
                    nlon = slab.shape[1]
                    nlat = slab.shape[0]
                    header = {
                        'ifv': 5,
                        'hdate': '2026-03-04_00:00:00',
                        'xfcst': 0.0,
                        'map_source': 'From file ' + nc_path,
                        'field': fieldname[:8],
                        'units': getattr(var, 'units', 'unknown')[:25],
                        'desc': getattr(var, 'long_name', 'desc')[:46],
                        'xlvl': float(k+1),
                        'nlon': nlon,
                        'nlat': nlat,
                        'iproj': 0,
                        'startloc': 'SWCORNER',
                        'startlat': float(nc.variables['lat'][0]),
                        'startlon': float(nc.variables['lon'][0]),
                        'deltalat': float(nc.variables['lat'][1] - nc.variables['lat'][0]),
                        'deltalon': float(nc.variables['lon'][1] - nc.variables['lon'][0]),
                        'earth_radius': 6367470.0 * 0.001,
                        'is_wind_earth_rel': False
                    }
                    write_mpas_binary(output_path, header, slab)
            elif len(shape) == 2:
                slab = var[:, :]
                nlon = slab.shape[1]
                nlat = slab.shape[0]
                header = {
                    'ifv': 5,
                    'hdate': '2026-03-04_00:00:00',
                    'xfcst': 0.0,
                    'map_source': 'From file ' + nc_path,
                    'field': varname[:8],
                    'units': getattr(var, 'units', 'unknown')[:25],
                    'desc': getattr(var, 'long_name', 'desc')[:46],
                    'xlvl': 1.0,
                    'nlon': nlon,
                    'nlat': nlat,
                    'iproj': 0,
                    'startloc': 'SWCORNER',
                    'startlat': float(nc.variables['lat'][0]),
                    'startlon': float(nc.variables['lon'][0]),
                    'deltalat': float(nc.variables['lat'][1] - nc.variables['lat'][0]),
                    'deltalon': float(nc.variables['lon'][1] - nc.variables['lon'][0]),
                    'earth_radius': 6367470.0 * 0.001,
                    'is_wind_earth_rel': False
                }
                write_mpas_binary(output_path, header, slab)
            else:
                print(f"Skipping variable {varname} with unsupported shape {shape}")
