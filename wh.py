import xarray as xr
import numpy as np
import datetime as dt

import matplotlib.pyplot as plt

from netCDF4 import Dataset

ncfile = 'jsh.nc'

dd = Dataset(ncfile)

print(dd)

print(dd.variables.keys())

lon = dd.variables['lon'][:]

print(lon)

print(dd.variables['lon'].shape)

lat = dd.variables['lat'][:]

plt.plot(lon, lat, 'o')
plt.show()

ds = xr.open_dataset(ncfile)

print(ds)

sd = ds['lon']

print(sd)

# d = ds['mass'].attrs

# de = ds.data_vars['mass'].values

# df = ds['mass'].to_dataframe()


# print(d)


# print(df)

# print(type(de))

# # variable attributes
# print(ds["mass"].attrs)

# # dimensions
# print(ds["mass"].dims)

# # raw numpy data
# print(ds["mass"].values)

# # datatype
# print(ds["mass"].dtype)

# # shape
# print(ds["mass"].shape)
