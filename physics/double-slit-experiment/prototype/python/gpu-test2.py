import os
# Add CUDA bin directory before importing CuPy
os.add_dll_directory(r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2\bin")

import cupy as cp
print("CuPy version:", cp.__version__)
try:
    print("CUDA runtime version:", cp.cuda.runtime.runtimeGetVersion())
except AttributeError:
    print("The runtime version attribute is not available in this CuPy version.")