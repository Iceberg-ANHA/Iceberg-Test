# import numpy as np
# import matplotlib.pyplot as plt
# from xarray import Dataset



# # Open the netCDF file
# file = Dataset("jsh.nc")


# iceberg_numbers = file.variables['iceberg_number'][:]

# print("Iceberg numbers shape:", iceberg_numbers.shape)
# print("First 5 iceberg numbers:\n", iceberg_numbers[:5])

# lon = file.variables['lon'][:]
# lat = file.variables['lat'][:]
# mass = file.variables['mass'][:]
# sst = file.variables['sst'][:]
# uvel = file.variables['uvel'][:]
# vvel = file.variables['vvel'][:]
# year = file.variables['year'][:]
# day = file.variables['day'][:]



# target_iceberg = iceberg_numbers[0]

# print("Tracking iceberg:", target_iceberg)



# # iceberg_number is likely shape (N,3)
# # so we compare entire rows

# matches = np.all(iceberg_numbers == target_iceberg, axis=1)

# indices = np.where(matches)[0]

# print(f"Found {len(indices)} records")



# for i in indices:

#     print("\n----------------------")
#     print("Record:", i)

#     print("Iceberg ID:", iceberg_numbers[i])

#     print("Position:")
#     print("  Longitude:", lon[i])
#     print("  Latitude :", lat[i])

#     print("Velocity:")
#     print("  U velocity:", uvel[i])
#     print("  V velocity:", vvel[i])

#     # Speed magnitude
#     speed = np.sqrt(uvel[i]**2 + vvel[i]**2)

#     print("  Speed:", speed)

#     print("Environment:")
#     print("  SST:", sst[i])

#     print("Iceberg:")
#     print("  Mass:", mass[i])

#     print("Time:")
#     print("  Year:", year[i])
#     print("  Day :", day[i])



# plt.plot(lon[indices], lat[indices], marker='o')

# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.title("Iceberg Trajectory")

# # plt.show()



# file.close()



import xarray as x
import numpy as np
import matplotlib.pyplot as plt



ds = x.open_dataset("jsh.nc")

print(ds)

iceberg_numbers = ds["iceberg_number"].values

lon = ds["lon"].values
lat = ds["lat"].values

mass = ds["mass"].values

# Print shapes meaning how many dimensions are in that array and the data points in each dimension and sample values

print("Mass shape:", mass.shape)
print("First 5 mass values:", mass[:5])

sst = ds["sst"].values

uvel = ds["uvel"].values
vvel = ds["vvel"].values

ss = ds["seaice_lock"].values

year = ds["year"].values
day = ds["day"].values

print(ds["length"].attrs)



target_iceberg = iceberg_numbers[0]

print("Tracking iceberg:", target_iceberg)


matches = np.all(iceberg_numbers == target_iceberg, axis=1)

indices = np.where(matches)[0]

print(f"Found {len(indices)} records")



for i in indices:

    speed = np.sqrt(uvel[i]**2 + vvel[i]**2)

    print("\n----------------------")
    print("Record:", i)

    print("Iceberg ID:", iceberg_numbers[i])

    print("Position")
    print("  Lon:", lon[i])
    print("  Lat:", lat[i], "\n")

    print("Sea Ice Lock:", ss[i], "\n")

    print("Velocity")
    print("  U:", uvel[i])
    print("  V:", vvel[i])

    print("  Speed:", speed)

    print("Environment")
    print("  SST:", sst[i])

    print("Iceberg")
    print("  Mass:", mass[i])

    print("Time")
    print("  Year:", year[i])
    print("  Day:", day[i])

    


# plt.plot(lon[indices], lat[indices], marker='o')

# plt.grid()


# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.title("Iceberg Trajectory")

# plt.show()

plt.plot(day[indices], mass[indices], marker='o')

plt.grid()

plt.xlabel("Day")
plt.ylabel("Mass")
plt.title("Iceberg Mass Over Time")
plt.show()


ds.close()