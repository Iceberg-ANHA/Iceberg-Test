# Iceberg-Test

A small data exploration repository for tracking iceberg properties from NetCDF datasets.

## Contents

- `sm.py` - Uses `xarray`, `numpy`, and `matplotlib` to inspect `jsh.nc`, print dataset details, and plot iceberg mass over time.
- `wh.py` - Uses `netCDF4` and `xarray` to inspect the same NetCDF dataset, print coordinate details, and display a longitude/latitude plot.
- `jsh.nc` - NetCDF iceberg dataset used by the scripts.
- `wh.nc` - Additional NetCDF file present in the workspace.
- `ncview.ps` - PostScript output file included in the repo.

## Requirements

- Python 3
- xarray
- numpy
- matplotlib
- netCDF4

## Usage

```bash
python sm.py
python wh.py
```

## Notes

This repository is oriented around exploratory scripts for inspecting NetCDF iceberg data and visualizing results.
