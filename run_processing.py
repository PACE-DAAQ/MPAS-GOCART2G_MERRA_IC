"""
Main processing script for MPAS-GOCART2G_MERRA_IC
"""
import yaml
import os
from mpas_gocart2g_merra_ic import file_ops

def check_packages():
    missing = []
    try:
        import numpy
    except ImportError:
        missing.append('numpy')
    try:
        import netCDF4
    except ImportError:
        missing.append('netCDF4')
    try:
        import yaml
    except ImportError:
        missing.append('pyyaml')
    if missing:
        print(f"Error: Missing required packages: {', '.join(missing)}")
        print("Please activate the correct environment (e.g., conda activate npl-2025b)")
        exit(1)

def main(config_path=None):
    if config_path is None:
        config_path = "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Subset time
    file_ops.subset_time(
        in_dir=config['in_dir'],
        out_dir=config['out_dir'],
        pattern=config.get('pattern', 'MERRA2_400.inst3_3d_ae*.nc4'),
        hours=config.get('hours', [0, 6, 12, 18])
    )

    # Automate combine_files: generate aer_files and out_files from subsetting output
    import glob
    aer_files = []
    out_files = []
    for hour in config.get('hours', [0, 6, 12, 18]):
        hh2 = f"{hour:02d}"
        pattern = f"*_{hh2}Z.nc4"
        files = [f for f in glob.glob(os.path.join(config['out_dir'], pattern)) if not os.path.basename(f).startswith('combined_')]
        aer_files.extend(files)
        for f in files:
            out_name = os.path.basename(f).replace('.nc4', '')
            out_files.append(os.path.join(config['out_dir'], f"{out_name}_with_ovp.nc4"))

    ovp_file = config['ovp_file']
    file_ops.combine_files(
        aer_files=aer_files,
        ovp_file=ovp_file,
        out_files=out_files
    )

    # Write MPAS binary files for each processed NetCDF file
    binary_names = config.get('binary_output_names', [])
    for ncfile, bin_name in zip(out_files, binary_names):
        bin_out = os.path.join(config['out_dir'], bin_name)
        print(f"Writing MPAS binary file: {bin_out} from {ncfile}")
        file_ops.process_and_write_mpas_binary(ncfile, bin_out)

if __name__ == "__main__":
    check_packages()
    import sys
    config_arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(config_arg)
