import numpy as np
import time

# Create a large boolean array
size = 1000
array = np.random.choice([0, 1], size=(size, size, size)).astype(np.int8)

# Create a mask where values are 1
mask = array == 1

# Measure time for ~mask
start = time.time()
inverse_mask_tilde = ~mask
end = time.time()
print(f"Time for ~mask: {end - start:.6f} seconds")

# Measure time for array == 0
start = time.time()
inverse_mask_comparison = array == 0
end = time.time()
print(f"Time for array == 0: {end - start:.6f} seconds")