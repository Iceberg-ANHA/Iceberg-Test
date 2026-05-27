# for the python post_process files 

import xarray as x
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import plotly.graph_objects as go


def plot_choice(indices, target_iceberg, lon, lat, mass, day, sst, uvel, vvel, ss):
    """Allow user to choose which plot to display."""
    print("\nAvailable plot types:")
    print("1. Trajectory (Longitude vs Latitude)")
    print("2. Mass over Time (Day vs Mass)")
    print("3. Velocity over Time (Day vs Speed)")
    print("4. Sea Ice Lock over Time (Day vs Sea Ice Lock)")
    while True:
        try:
            choice = int(input("\nEnter plot type (1-4): "))
            if choice in [1, 2, 3, 4]:
                plot_graph(choice, indices, target_iceberg, lon, lat, mass, day, sst, uvel, vvel, ss)
                return choice
            else:
                print("  Please choose a number between 1 and 4.")
        except ValueError:
            print("  Please enter a valid integer.")


def plot_graph(choice, indices, target_iceberg, lon, lat, mass, day, sst, uvel, vvel, ss):
    """Generate and display the selected plot."""
    if choice == 1:
        plt.plot(lon[indices], lat[indices], marker='o')
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title(f"Iceberg {target_iceberg} — Trajectory")
        plt.grid()
        plt.show()

    elif choice == 2:
        plt.plot(day[indices], mass[indices], marker='o')
        plt.xlabel("Day")
        plt.ylabel("Mass")
        plt.title(f"Iceberg {target_iceberg} — Mass Over Time")
        plt.grid()
        plt.show()

    elif choice == 3:
        speed = np.sqrt(uvel[indices]**2 + vvel[indices]**2)
        plt.plot(day[indices], speed, marker='o')
        plt.xlabel("Day")
        plt.ylabel("Speed")
        plt.title(f"Iceberg {target_iceberg} — Speed Over Time")
        plt.grid()
        plt.show()

    elif choice == 4:
        plt.plot(day[indices], ss[indices], marker='o')
        plt.xlabel("Day")
        plt.ylabel("Sea Ice Lock")
        plt.title(f"Iceberg {target_iceberg} — Sea Ice Lock Over Time")
        plt.grid()
        plt.show()


ds = x.open_dataset("b1.nc", decode_times=False)

print(ds)

iceberg_numbers = ds["iceberg_number"].values

# the icebergs are arranged by particle ID, then time step, so we check for valid data along the first dimension (particle ID)

# print("Iceberg numbers shape:", iceberg_numbers.shape)
# print("First 5 iceberg numbers:", iceberg_numbers[:])


# previosly used this code below which regardless of using [0] or [1] or [2] it would return the same result
# because the data is arranged by particle ID until we have data for it.
# target_iceberg = iceberg_numbers[0]

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

# Show available icebergs and prompt user to pick one
unique_icebergs = np.unique(iceberg_numbers)
print(f"\nAvailable iceberg IDs ({len(unique_icebergs)} total):")
print(unique_icebergs)

while True:
    try:
        choice = int(input("\nEnter iceberg ID to track: "))
        if choice in unique_icebergs:
            target_iceberg = choice
            break
        else:
            print(f"  '{choice}' not found. Please choose from the list above.")
    except ValueError:
        print("  Please enter a valid integer.")

print("Tracking iceberg:", target_iceberg)

matches = iceberg_numbers == target_iceberg

indices = np.where(matches)[0]
# time_order = np.argsort(year[indices] * 365 + day[indices])
# indices = indices[time_order]

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

# Call plot_choice to let user select a plot
plot_choice(indices, target_iceberg, lon, lat, mass, day, sst, uvel, vvel, ss)



# documnetation for plotly graphing the trajectory of the iceberg --- https://plotly.com/python/lines-on-maps/
# another way to plot 


#

# documnetation for plotly graphing the trajectory of the iceberg --- https://cartopy.readthedocs.io/stable/gallery/lines_and_polygons/global_map.html#sphx-glr-gallery-lines-and-polygons-global-map-py


projection = ccrs.Robinson()
data_transform = ccrs.PlateCarree() 

fig, ax = plt.subplots(figsize=(12, 7), subplot_kw={'projection': projection})

ax.add_feature(cfeature.NaturalEarthFeature('physical', 'ocean', '110m', facecolor='lightblue'))
ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '110m', facecolor='lightgrey'))
ax.add_feature(cfeature.COASTLINE, edgecolor='black', linewidth=0.5)

ax.set_global()  # Set the extent to global

ax.plot(lon[indices], lat[indices], 
        color='red', 
        linestyle='-', 
        marker='o', 
        markersize=4,
        label=f'Iceberg {target_iceberg}', 
        transform=data_transform)

ax.plot(lon[indices[0]], lat[indices[0]], 
        color='green', 
        marker='o', 
        markersize=10, 
        linestyle='None',
        label='Start', 
        transform=data_transform)

ax.plot(lon[indices[-1]], lat[indices[-1]], 
        color='black', 
        marker='o', 
        markersize=10, 
        linestyle='None',
        label='End', 
        transform=data_transform)

# ax.set_extent([-120, 40, 40, 90], crs=data_transform)

ax.set_title(f'Iceberg {target_iceberg} — Trajectory', fontsize=14, pad=15)
ax.legend(loc='lower left', framealpha=0.9)

ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, color='gray', alpha=0.3)

plt.show()

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




# iceberg_numbers = file.variable
# plt.plot(lon[indices], lat[indices], marker='o')

# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.title("Iceberg Trajectory")

# # plt.show()

# file.close()