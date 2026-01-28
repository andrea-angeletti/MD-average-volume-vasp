import numpy as np
import matplotlib.pyplot as plt
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from py4vasp import Calculation

# Crea un oggetto Calculation dalla directory corrente
calc = Calculation.from_path(".")
volumes = calc.structure[:].volume()

volumes = np.array(volumes)

# Ottieni il numero totale di passaggi di calcolo dalla lunghezza dell'array volumes
num_steps = len(volumes)

# Crea un array di passaggi (0, 1, 2, ..., num_steps-1) limitato a 300,000
steps = np.arange(1, num_steps+1)

# Calcola la media dei volumi da 4000 a 300000
x1=1
x2=len(volumes)
average_volume = np.mean(volumes[x1:x2])

fs = 10

# Get the temperature data as a dictionary
temperature_dict = calc.energy[:].to_dict("temperature")

# Convert the dictionary values to a numpy array
temperature = np.array(list(temperature_dict.values()))

# Flatten the temperature array
temperature = temperature.flatten()
#necessary because NBLOCK might be different from 1 
#the new atomic positions are printed in XDATCAR only every NBLOCK steps
temperature = temperature[:len(volumes)]

# Create a new subplot sharing the same x-axis
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()
# Plot temp on the right y-axis
ax2.plot(steps, temperature, color='black',linewidth=1,  linestyle='--')
ax2.set_ylabel('Temperature (K)', fontsize=fs, color='black' )
ax2.tick_params(axis='y', labelcolor='black')


# Plot volumes on the left y-axis
ax1.plot(steps, volumes, color='red', linewidth=2)
ax1.axhline(y=average_volume, color='green', linestyle='--', linewidth=3 , label=f'Average Volume = {average_volume:.2f}')
ax1.axvline(x=x1, color='blue', linestyle='--',linewidth=3)
ax1.axvline(x=x2, color='blue', linestyle='--',linewidth=3)
ax1.set_xlabel('Time steps [fs]', fontsize=fs)
ax1.set_ylabel('Volume', fontsize=fs, color='red')
ax1.tick_params(axis='y', labelcolor='red')


# Combine legends for both plots
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines = lines1 + lines2
labels = labels1 + labels2
ax1.legend(lines, labels, loc='upper left', fontsize=fs)

# Set fontsize for tick labels
ax1.tick_params(axis='both', labelsize=fs)
ax2.tick_params(axis='both', labelsize=fs)



# Save the image in the current directory with the name "volume_temp_plot.png"
plt.savefig('./volume_temp_plot.png')

# Calculate the absolute differences between each element and 'average_volume'
differences = np.abs(volumes - average_volume)

# Find the index of the minimum difference
closest_index = differences.argmin()

# Get the value in 'volumes' corresponding to the closest index
closest_value = volumes[closest_index]


print("Closest value to average_volume:", closest_value)
print("Index in 'volumes' associated with the closest value:", closest_index)
print()

print(calc.structure[closest_index-1])
#save it to a file
# Get the structure data
structure_data = str(calc.structure[closest_index-1])

# Open the file in write mode
with open('POSCAR_avg_volume', 'w') as f:
    # Write the structure data to the file
    f.write(structure_data)

# Show the plot
plt.show()
