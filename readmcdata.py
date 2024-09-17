import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('sorted82.txt', delimiter=',', skiprows=0)

size = data[:, 0]
chunk_size = data[:, 1]
p_value = data[:, 2]
temp = data[:, 3]
X = data[:, 4]
C = data[:, 5]
U_L = data[:, 6]

sizes = np.unique(size)
p_values = np.unique(p_value)

for s in sizes:
    for p in p_values:
        mask = (p_value == p) & (size == s)
        plt.plot(temp[mask], X[mask])

    plt.xlabel('Temp')
    plt.xticks(np.arange(0, 15.1, 1))
    plt.ylabel('X')
    plt.title(f'Temp vs. X for size {s}')
    plt.show()


    for p in p_values:
        mask = (p_value == p) & (size == s)
        plt.plot(temp[mask], C[mask])

    plt.xlabel('Temp')
    plt.xticks(np.arange(0, 15.1, 1))
    plt.ylabel('C')
    plt.title(f'Temp vs. C for size {s}')
    plt.show()

    for p in p_values:
        mask = (p_value == p) & (size == s)
        plt.plot(temp[mask], U_L[mask])

    plt.xlabel('Temp')
    plt.xticks(np.arange(0, 15.1, 1))
    plt.ylabel('U_L')
    plt.title(f'Temp vs. U_L for size {s}')
    plt.show()