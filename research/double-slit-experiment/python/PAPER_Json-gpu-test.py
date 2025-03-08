# RUN ON Colab.google.com with GPU Runtime Type enabled
# When cupy is operational, you should be able to run this and see output something like this:

# CuPy version: 13.3.0
# CUDA runtime version: 12060
# Test Array Operation (should output a cupy array): [ 0  2  4  6  8 10 12 14 16 18]

import cupy as cp

print("CuPy version:", cp.__version__)
print("CUDA runtime version:", cp.cuda.runtime.runtimeGetVersion())


try:
    a = cp.arange(10)
    b = cp.arange(10)
    c = a + b
    print("Test Array Operation (should output a cupy array):", c)
except Exception as e:
    print("Simple GPU array operation failed:", e)

