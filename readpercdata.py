import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('percdata.txt', delimiter=',', skiprows=0)

size = data[:, 0]
p = data[:, 1]
numpercolated = data[:, 2]
avglargestchunk = data[:, 3]

sizes = np.unique(size)

for s in sizes:
    mask = (size == s)
    plt.plot(np.flip(p[mask]), numpercolated[mask])

plt.xlabel('P')
plt.xticks(np.arange(0, 1.1, 0.1))
plt.ylabel('Number Percolated')
plt.title(f'P vs. Average Number Percolated')
plt.savefig("percolation.png")
plt.show()

for s in sizes:
    mask = (size == s)
    plt.plot(np.flip(p[mask]), avglargestchunk[mask])

plt.xlabel('P')
plt.xticks(np.arange(0, 1.1, 0.1))
plt.ylabel('Average Largest Cluster')
plt.title(f'P vs. Average Largest Cluster')
plt.savefig("cluster.png")
plt.show()