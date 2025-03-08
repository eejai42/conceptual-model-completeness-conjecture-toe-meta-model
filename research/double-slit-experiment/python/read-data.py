import numpy as np

# Load the collapsed experiment data
data = np.load('raw_data_collapsed.npz', allow_pickle=True)
print("Keys in file:", data.files)

intensity = data['intensity']
norm_intensity = data['normalized_intensity']
field = data['field']
parameters = data['parameters'].item()  # use .item() to extract the dict

print("Intensity shape:", intensity.shape)
print("Field shape:", field.shape)
print("Parameters:", parameters)
