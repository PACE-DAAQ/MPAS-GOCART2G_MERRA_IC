

# MPAS-GOCART2G_MERRA_IC Python Workflow

This package provides modernized Python routines for processing satellite data, replacing legacy Fortran scripts. It supports flexible configuration via YAML and outputs MPAS-compatible binary files.

## Environment Setup (Derecho)
Activate the NCAR Python environment before running:
```
conda activate npl-2025b
```

## Usage: Full Processing Workflow
1. Edit `config.yaml` to specify input/output directories, file patterns, and desired output names.
2. Run the main processing script:
```
python3 run_processing.py
```
This will:
- Subset NetCDF files by hour
- Combine files as needed
- Write MPAS binary files for all variables and levels

## Example: Direct MPAS Binary Output
You can also write MPAS binary files directly from a NetCDF file:
```
python3 -c "from mpas_gocart2g_merra_ic.file_ops import process_and_write_mpas_binary; process_and_write_mpas_binary('input.nc4', 'output.mpasbin')"
```
This will extract all variables and write them in MPAS binary format, matching the legacy Fortran output.

## Configuration
Edit `config.yaml` to control all input/output paths and processing options. Example:
```
in_dir: /path/to/input
out_dir: /path/to/output
pattern: MERRA2_400.inst3_3d_ae*.nc4
hours: [0, 6, 12, 18]
ovp_file: /path/to/ovp.nc4
binary_output_names:
	- MERRA2:2024-10-15_00
	- MERRA2:2024-10-15_06
	- MERRA2:2024-10-15_12
	- MERRA2:2024-10-15_18
```

## Requirements
The following packages must be available in your environment:
- numpy
- netCDF4
- pyyaml

Check package availability with:
```
python3 -c "import numpy, netCDF4, yaml; print('All packages available')"
```

## Version Control Best Practices
- Add all large or legacy files to `.gitignore`.
- Archive old files in a separate directory and ignore that directory.
- Only commit code, config, and small sample data to GitHub.

## Installation
Install required dependencies:
pip install numpy netCDF4
