import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('data.txt', delimiter=',', skiprows=0)

size = data[:, 0]
p = data[:, 1]
numpercolated = data[:, 2]
avglargestchunk = data[:, 3]

sizes = np.unique(size)

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)

for s in sizes:
    mask = (size == s)

    plt.plot(np.flip(p[mask]), numpercolated[mask])
    plt.xlabel('P')
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.ylabel('Number Percolated')
    plt.title(f'P vs. Average Number Percolated for Size = {s}')

plt.subplot(1, 2, 2)

for s in sizes:
    mask = (size == s)
    plt.plot(np.flip(p[mask]), avglargestchunk[mask])
    plt.xlabel('P')
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.ylabel('Average Largest Chunk')
    plt.title(f'P vs. Average Largest Chunk for Size = {s}')

plt.tight_layout()
plt.show()