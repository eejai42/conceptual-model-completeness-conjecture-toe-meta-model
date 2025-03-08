import numpy as np
import matplotlib.pyplot as plt

# Load the NPZ file (set allow_pickle=True to load object arrays)
data = np.load('raw_data_interference.npz', allow_pickle=True)
print("Keys in file:", data.files)

# Extract arrays
intensity = data['intensity']
field = data['field']
parameters = data['parameters'].item()

print("Intensity shape:", intensity.shape)
print("Field shape:", field.shape)
print("Parameters:", parameters)

# Plot the 1D intensity profile (linear scale)
plt.figure(figsize=(8, 4))
plt.plot(intensity, label="Intensity")
plt.xlabel("Detector Position")
plt.ylabel("Intensity")
plt.title("Detector Intensity Profile")
plt.legend()
plt.show()

# Plot with a logarithmic y-axis to reveal lower intensities
plt.figure(figsize=(8, 4))
plt.plot(intensity, label="Intensity")
plt.xlabel("Detector Position")
plt.ylabel("Intensity (log scale)")
plt.yscale("log")
plt.title("Detector Intensity Profile (Log Scale)")
plt.legend()
plt.show()


import numpy as np
import matplotlib.pyplot as plt

# Load the NPZ file (set allow_pickle=True to load object arrays)
data = np.load('raw_data_collapsed.npz', allow_pickle=True)
print("Keys in file:", data.files)

# Extract arrays
intensity = data['intensity']
field = data['field']
parameters = data['parameters'].item()

print("Intensity shape:", intensity.shape)
print("Field shape:", field.shape)
print("Parameters:", parameters)

# Plot the 1D intensity profile (linear scale)
plt.figure(figsize=(8, 4))
plt.plot(intensity, label="Intensity")
plt.xlabel("Detector Position")
plt.ylabel("Intensity")
plt.title("Detector Intensity Profile")
plt.legend()
plt.show()

# Plot with a logarithmic y-axis to reveal lower intensities
plt.figure(figsize=(8, 4))
plt.plot(intensity, label="Intensity")
plt.xlabel("Detector Position")
plt.ylabel("Intensity (log scale)")
plt.yscale("log")
plt.title("Detector Intensity Profile (Log Scale)")
plt.legend()
plt.show()
