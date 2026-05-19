import argparse
import numpy as np
import xarray as xr


def summarize_array(arr):
    arrf = arr.astype(np.float64)
    return {
        "shape": arr.shape,
        "size": arr.size,
        "dtype": str(arr.dtype),
        "min": float(np.nanmin(arrf)) if arrf.size else None,
        "max": float(np.nanmax(arrf)) if arrf.size else None,
        "mean": float(np.nanmean(arrf)) if arrf.size else None,
        "sum": float(np.nansum(arrf)) if arrf.size else None,
    }


def compare_arrays(name, arr1, arr2):
    if arr1.shape != arr2.shape:
        print(f"MISMATCH: {name} shape differs: {arr1.shape} vs {arr2.shape}")
        if np.issubdtype(arr1.dtype, np.number) and np.issubdtype(arr2.dtype, np.number):
            s1 = summarize_array(arr1)
            s2 = summarize_array(arr2)
            print(f"  file1 summary: size={s1['size']}, min={s1['min']}, max={s1['max']}, mean={s1['mean']}, sum={s1['sum']}")
            print(f"  file2 summary: size={s2['size']}, min={s2['min']}, max={s2['max']}, mean={s2['mean']}, sum={s2['sum']}")
            if s1['sum'] is not None and s2['sum'] is not None:
                print(f"  sum diff: {s1['sum'] - s2['sum']}")
        return False

    if arr1.dtype != arr2.dtype:
        print(f"WARNING: {name} dtype differs: {arr1.dtype} vs {arr2.dtype}")

    if np.issubdtype(arr1.dtype, np.integer) or np.issubdtype(arr1.dtype, np.bool_):
        equal = np.array_equal(arr1, arr2)
    else:
        equal = np.allclose(arr1, arr2, atol=1e-12, rtol=1e-8, equal_nan=True)

    if equal:
        return True

    diff = arr1.astype(np.float64) - arr2.astype(np.float64)
    max_abs = np.nanmax(np.abs(diff))
    max_rel = np.nanmax(np.abs(diff / np.where(arr2 == 0, 1, arr2)))
    print(f"MISMATCH: {name} values differ")
    print(f"  max abs diff: {max_abs}")
    print(f"  max rel diff: {max_rel}")

    if arr1.size <= 20:
        print("  values 1:", arr1)
        print("  values 2:", arr2)
    return False


def compare_datasets(ds1, ds2):
    ok = True

    dims1 = ds1.dims
    dims2 = ds2.dims
    if dims1 != dims2:
        print("DIMENSIONS differ")
        print("  file1 dims:", dims1)
        print("  file2 dims:", dims2)
        ok = False

    print("\nComparing coordinates...")
    coords1 = set(ds1.coords)
    coords2 = set(ds2.coords)
    for name in sorted(coords1 | coords2):
        if name not in coords1:
            print(f"MISSING coordinate in file1: {name}")
            ok = False
            continue
        if name not in coords2:
            print(f"MISSING coordinate in file2: {name}")
            ok = False
            continue

        coord1 = ds1.coords[name].values
        coord2 = ds2.coords[name].values
        if not compare_arrays(f"coord {name}", coord1, coord2):
            ok = False

    print("\nComparing data variables...")
    vars1 = set(ds1.data_vars)
    vars2 = set(ds2.data_vars)
    for name in sorted(vars1 | vars2):
        if name not in vars1:
            print(f"MISSING variable in file1: {name}")
            ok = False
            continue
        if name not in vars2:
            print(f"MISSING variable in file2: {name}")
            ok = False
            continue

        var1 = ds1[name].values
        var2 = ds2[name].values
        if not compare_arrays(f"var {name}", var1, var2):
            ok = False

    return ok


def main():
    parser = argparse.ArgumentParser(
        description="Compare two netCDF files for data equality and report mismatches."
    )
    parser.add_argument(
        "file1",
        nargs="?",
        default="mas.nc",
        help="First netCDF file (default: mas.nc)",
    )
    parser.add_argument(
        "file2",
        nargs="?",
        default="dcd.nc",
        help="Second netCDF file (default: dcd.nc)",
    )
    args = parser.parse_args()

    ds1 = xr.open_dataset(args.file1)
    ds2 = xr.open_dataset(args.file2)

    print(f"Comparing {args.file1} and {args.file2}")
    result = compare_datasets(ds1, ds2)

    ds1.close()
    ds2.close()

    if result:
        print("\nRESULT: files match")
    else:
        print("\nRESULT: files differ")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
