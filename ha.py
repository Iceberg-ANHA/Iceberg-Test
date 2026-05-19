import argparse
from pathlib import Path

import numpy as np
import xarray as xr


def format_values(values: np.ndarray, max_items: int = 20) -> str:
    """Format array values for display, with truncation for large arrays."""
    if values.ndim == 0:
        return str(values.item())

    flat = values.ravel()
    size = flat.size
    if size == 0:
        return "[]"

    if size <= max_items:
        return np.array2string(flat, separator=", ")

    head = np.array2string(flat[: max_items // 2], separator=", ")
    tail = np.array2string(flat[-(max_items // 2) :], separator=", ")
    return f"{head[:-1]}, ..., {tail[1:]}"


def print_variable(name: str, var: xr.DataArray, max_items: int) -> None:
    values = var.values
    print(f"\n=== {name} ===")
    print(f"dims: {var.dims}")
    print(f"shape: {values.shape}")
    print(f"dtype: {values.dtype}")
    # if var.encoding:
    #     print(f"encoding: {var.encoding}")
    if var.attrs:
        print("attributes:")
        for key, value in var.attrs.items():
            print(f"  {key}: {value}")

    if values.size == 0:
        print("values: []")
    else:
        print(f"values (sample, {max_items} items max): {format_values(values, max_items)}")
    print()
    print("-" * 40)


def print_dataset(ds: xr.Dataset, target_var: str | None, max_items: int, show_coords: bool) -> None:
    print("Dataset summary:")
    print(ds)

    if target_var:
        if target_var in ds.variables:
            print_variable(target_var, ds[target_var], max_items)
        else:
            raise ValueError(f"Variable '{target_var}' not found in dataset")
        return

    if show_coords:
        print("\nCoordinates:")
        for coord_name in ds.coords:
            print_variable(coord_name, ds[coord_name], max_items)

    print("\nData variables:")
    for var_name in ds.data_vars:
        print_variable(var_name, ds[var_name], max_items)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Show netCDF variable contents similar to Java ArrayList output."
    )
    parser.add_argument(
        "file",
        nargs="?",
        default="dcd.nc",
        help="Path to the netCDF file to read",
    )
    parser.add_argument(
        "-v",
        "--variable",
        help="Show only this variable (coord or data variable)",
    )
    parser.add_argument(
        "-n",
        "--max-items",
        type=int,
        default=20,
        help="Maximum number of items to display for each array",
    )
    parser.add_argument(
        "--no-coords",
        action="store_true",
        help="Do not print coordinate variables",
    )

    args = parser.parse_args()
    path = Path(args.file)
    if not path.exists():
        raise FileNotFoundError(f"NetCDF file not found: {path}")

    ds = xr.open_dataset(path)
    print_dataset(ds, args.variable, args.max_items, not args.no_coords)
    ds.close()

if __name__ == "__main__":
    main()