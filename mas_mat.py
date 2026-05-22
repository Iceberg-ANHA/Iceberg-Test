# for mas.nc

import netCDF4 as nc
import numpy as np

# Open dataset
ds = nc.Dataset("mas.nc")

# Load mass array
mass = ds.variables["mass"][:]
print("Array shape:", mass.shape)
print()

# Find valid icebergs (non-empty rows)
valid_ids = [
    i for i in range(mass.shape[0])
    if not np.all(np.isnan(mass[i]))
]

if not valid_ids:
    print("No valid icebergs found in dataset.")
    ds.close()
    exit()

print(f"Available icebergs: {valid_ids[0]} to {valid_ids[-1]} "
      f"({len(valid_ids)} total with data)")
print()

# Prompt user for iceberg ID
while True:
    try:
        user_input = input(f"Enter iceberg ID [{valid_ids[0]}-{valid_ids[-1]}]: ").strip()
        particle_id = int(user_input)

        if particle_id not in valid_ids:
            print(f"  No data for iceberg {particle_id}. "
                  f"Choose from: {valid_ids[0]}–{valid_ids[-1]}\n")
            continue

        break

    except ValueError:
        print("  Invalid input. Please enter a whole number.\n")

# Display data for the chosen iceberg
iceberg_data = mass[particle_id]

print()
print("=" * 60)
print(f"ICEBERG {particle_id}")
print("=" * 60)

for timestep in range(mass.shape[1]):
    value = iceberg_data[timestep]
    if not np.isnan(value):
        print(f"mass[{particle_id}][{timestep}] = {value:.6e}")

        # mass[iceberg id in the dataset where the iceberg is located][timestep = day] = mass in that instance

print()

plot = input("Plot mass over time? (y/n): ").strip().lower()

if plot == 'y':
    import matplotlib.pyplot as plt

    time = np.arange(mass.shape[1])

    plt.figure(figsize=(10, 5))
    plt.plot(time, iceberg_data, marker='o')
    plt.title(f"Mass of Iceberg {particle_id} Over Time")
    plt.xlabel("Time (days)")
    plt.ylabel("Mass")
    plt.grid()
    plt.show()

# Close file
ds.close()


# runs all the icebergs

# import netCDF4 as nc
# import numpy as np

# # Open dataset
# ds = nc.Dataset("mas.nc")

# # Load mass array
# mass = ds.variables["mass"][:]

# print("Array shape:", mass.shape)
# print()

# # Loop through every iceberg (particle)
# for particle_id in range(mass.shape[0]):

#     # Get all timesteps for this iceberg
#     iceberg_data = mass[particle_id]

#     # Skip completely empty rows
#     if np.all(np.isnan(iceberg_data)):
#         continue

#     print("=" * 60)
#     print(f"ICEBERG {particle_id}")
#     print("=" * 60)

#     # Print every timestep value
#     for timestep in range(mass.shape[1]):

#         value = iceberg_data[timestep]

#         if not np.isnan(value):
#             print(f"mass[{particle_id}][{timestep}] = {value:.6e}")

#     print()

# # Close file
# ds.close()