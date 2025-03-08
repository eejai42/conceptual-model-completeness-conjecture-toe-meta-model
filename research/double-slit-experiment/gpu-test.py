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

