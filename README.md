

# MPAS-GOCART2G_MERRA_IC Python Workflow

This package provides modernized Python routines for processing satellite data, replacing legacy Fortran scripts. It supports flexible configuration via YAML and outputs MPAS-compatible binary files.

## Environment Setup (Derecho)
Activate the NCAR Python environment before running:
```
conda activate npl-2025b
```

## Usage: Full Processing Workflow
1. Edit `config.yaml` to specify input/output directories, file patterns, desired output names, and species mapping.
2. Run the main processing script:
```
python3 run_processing.py
```
This will:
- Subset provided NetCDF files by day and interval
- Combine files as needed
- Write MPAS binary files for all variables and levels, with missing fields as all zeros

## Configuration
Edit `config.yaml` to control all input/output paths and processing options. The base example file contains all of the relevant fields needed for running MPAS-GOCART2g 
Example:

```
control_params:
  start_year: 2024
  start_month: 10
  start_day: 15
  start_hour: 0
  num_days: 1
  interval_hr: 6
  prefix_in_1: "/glade/derecho/scratch/$USER/MPAS-GOCART2G_MERRA_IC/DATA/MERRA2_400.inst3_3d_aer_Nv."
  suffix_in_1: ".nc4"
  prefix_in_2: "/glade/derecho/scratch/$USER/MPAS-GOCART2G_MERRA_IC/DATA/MERRA2_GMI.inst0_3d_ovp_Nv."
  suffix_in_2: "_1200z.nc4"
  prefix_out: "/glade/derecho/scratch/$USER/MPAS-GOCART2G_MERRA_IC/MERRA2:"

species_map:
  - {source: "BCPHILIC", file: "prefix_in_1", target: "BCPHILIC", desc: "Hydrophilic Black Carbon Mixing Ratio", units: "kg kg^-1"}
  - {source: "BCPHOBIC", file: "prefix_in_1", target: "BCPHOBIC", desc: "Hydrophobic Black Carbon Mixing Ratio", units: "kg kg^-1"}
  - {source: "OCPHILIC", file: "prefix_in_1", target: "OCPHILIC", desc: "Hydrophilic Organic Carbon Mixing Ratio", units: "kg kg^-1"}
  - {source: "OCPHOBIC", file: "prefix_in_1", target: "OCPHOBIC", desc: "Hydrophobic Organic Carbon Mixing Ratio", units: "kg kg^-1"}
  - {source: "DU001",    file: "prefix_in_1", target: "DU001",    desc: "Dust Mixing Ratio in Bin 001", units: "kg kg^-1"}
  - {source: "DU002",    file: "prefix_in_1", target: "DU002",    desc: "Dust Mixing Ratio in Bin 002", units: "kg kg^-1"}
  - {source: "DU003",    file: "prefix_in_1", target: "DU003",    desc: "Dust Mixing Ratio in Bin 003", units: "kg kg^-1"}
  - {source: "DU004",    file: "prefix_in_1", target: "DU004",    desc: "Dust Mixing Ratio in Bin 004", units: "kg kg^-1"}
  - {source: "DU005",    file: "prefix_in_1", target: "DU005",    desc: "Dust Mixing Ratio in Bin 005", units: "kg kg^-1"}
  - {source: "NI001",    file: "prefix_in_1", target: "NI001",    desc: "Nitrate Mixing Ratio in Bin 001", units: "kg kg^-1"}
  - {source: "NI002",    file: "prefix_in_1", target: "NI002",    desc: "Nitrate Mixing Ratio in Bin 002", units: "kg kg^-1"}
  - {source: "NI003",    file: "prefix_in_1", target: "NI003",    desc: "Nitrate Mixing Ratio in Bin 003", units: "kg kg^-1"}
  - {source: "SO2",      file: "prefix_in_1", target: "SO2",      desc: "Sulphur Dioxide Mixing Ratio", units: "kg kg^-1"}
  - {source: "SO2v",     file: "prefix_in_1", target: "SO2V",     desc: "Sulphur Dioxide Mixing Ratio (volcanic)", units: "kg kg^-1"}
  - {source: "SO4",      file: "prefix_in_1", target: "SO4",      desc: "Sulfate Mixing Ratio", units: "kg kg^-1"}
  - {source: "SO4v",     file: "prefix_in_1", target: "SO4V",     desc: "Sulfate Mixing Ratio (volcanic)", units: "kg kg^-1"}
  - {source: "SS001",    file: "prefix_in_1", target: "SS001",    desc: "Seasalt Mixing Ratio in Bin 001", units: "kg kg^-1"}
  - {source: "SS002",    file: "prefix_in_1", target: "SS002",    desc: "Seasalt Mixing Ratio in Bin 002", units: "kg kg^-1"}
  - {source: "SS003",    file: "prefix_in_1", target: "SS003",    desc: "Seasalt Mixing Ratio in Bin 003", units: "kg kg^-1"}
  - {source: "SS004",    file: "prefix_in_1", target: "SS004",    desc: "Seasalt Mixing Ratio in Bin 004", units: "kg kg^-1"}
  - {source: "SS005",    file: "prefix_in_1", target: "SS005",    desc: "Seasalt Mixing Ratio in Bin 005", units: "kg kg^-1"}
  - {source: "DMS",      file: "prefix_in_1", target: "DMS",      desc: "Dimethylsulphide Mixing Ratio", units: "kg kg^-1"}
  - {source: "MSA",      file: "prefix_in_1", target: "MSA",      desc: "Methanesulphonic Acid Mixing Ratio", units: "kg kg^-1"}
  - {source: "AIRDENS",  file: "prefix_in_1", target: "AIRDENS",  desc: "Moist_Air_Density", units: "kg m^-3"}
  - {source: "RH",       file: "prefix_in_1", target: "RH",       desc: "Relative Humidity", units: "-"}
  - {source: "DELP",     file: "prefix_in_1", target: "DPRES",    desc: "Pressure Thickness", units: "Pa"}
  - {source: "PS",       file: "prefix_in_1", target: "PS",       desc: "Surface Pressure", units: "Pa"}
  - {source: "LWI",      file: "prefix_in_1", target: "LWI",      desc: "Land(1)_Water(0)_Ice(2)_Flag", units: "-"}
  - {source: "OVP14_HNO3",            file: "prefix_in_2", target: "HNO3",          desc: "Nitric Acid", units: "mole mole-1"}
  - {source: "OVP14_HNO3COND",        file: "prefix_in_2", target: "HNO3COND",      desc: "Condensed Nitric Acid", units: "mole mole-1"}
  - {source: "OVP14_GOCART_NH3_VAR",  file: "prefix_in_2", target: "NH3",           desc: "Ammonia", units: "mole mole-1"}
  - {source: "OVP14_CO",              file: "prefix_in_2", target: "CO",            desc: "Carboin Monoxide", units: "mole mole-1"}
  - {source: "OVP14_ISOP",            file: "prefix_in_2", target: "ISOPRENE",      desc: "Isoprene", units: "mole mole-1"}
```
## Output Processing
To view the header contents of the output intermediate file and ensure all necessary MPAS fields are there use the WPS read_intermediate utility:
https://github.com/wrf-model/WPS/blob/master/util/src/rd_intermediate.F


## Requirements
The following packages must be available in your environment:
- numpy
- netCDF4
- pyyaml

Check package availability with:
```
python3 -c "import numpy, netCDF4, yaml; print('All packages available')"
```
## Installation
For non-Derecho HPC install required dependencies:
pip install numpy netCDF4 pyyaml
